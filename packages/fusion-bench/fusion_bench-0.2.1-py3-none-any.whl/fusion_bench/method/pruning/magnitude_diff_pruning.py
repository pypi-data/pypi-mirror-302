import logging
import re
from copy import deepcopy
from typing import Dict, List  # noqa: F401

import torch
from torch import Tensor, nn
from tqdm.auto import tqdm

from fusion_bench.method import BaseModelFusionAlgorithm
from fusion_bench.mixins.simple_profiler import SimpleProfilerMixin
from fusion_bench.modelpool import BaseModelPool

log = logging.getLogger(__name__)


def _magnitude_prune(weight: Tensor, prune_ratio: float) -> Tensor:
    """
    Prune the weights by setting values below a certain quantile to zero.

    Args:
        weight (Tensor): The weight tensor to be pruned.
        prune_ratio (float): The ratio of weights to prune.

    Returns:
        Tensor: The pruned weight tensor.
    """
    weight_abs = weight.abs()
    mask = weight_abs > weight_abs.quantile(prune_ratio)
    weight = weight * mask
    return weight


def _is_name_matched(name: str, extract_names: List[str]):
    """
    Check if the parameter name matches any of the provided regular expressions.

    Args:
        name (str): The name of the parameter.
        extract_names (List[str]): List of regular expressions to match the parameter names.

    Returns:
        bool: True if the name matches any of the regular expressions, False otherwise.
    """
    for extract_name in extract_names:
        # extract_name is a regular expression
        if re.match(extract_name, name):
            return True
    return False


class MagnitudeDiffPruningAlgorithm(
    BaseModelFusionAlgorithm,
    SimpleProfilerMixin,
):
    _config_mapping = BaseModelFusionAlgorithm._config_mapping | {
        "prune_ratio": "prune_ratio",
        "extract_names": "extract_names",
    }

    def __init__(
        self,
        prune_ratio: float,
        extract_names: List[str] = None,
        **kwargs,
    ):
        self.prune_ratio = prune_ratio
        self.extract_names = extract_names
        super().__init__(**kwargs)

    @torch.no_grad()
    def run(self, modelpool: BaseModelPool):
        if not isinstance(modelpool, BaseModelPool):
            modelpool = BaseModelPool(modelpool)

        assert (
            len(modelpool.model_names) == 1
        ), "Only one fine-tuned model is allowed in the model pool."
        with self.profile("load pretrained model"):
            pretrained_model = modelpool.load_model("_pretrained_")
        with self.profile("load fine-tuned model"):
            finetuned_model = modelpool.load_model(modelpool.model_names[0])

        with self.profile("prune model"):
            model = self.magnitude_prune(pretrained_model, finetuned_model)

        self.print_profile_summary()
        return model

    def magnitude_prune(
        self,
        pretrained_model: nn.Module,
        finetuned_model: nn.Module,
        in_place: bool = True,
    ):
        if in_place:
            model = pretrained_model
        else:
            model = deepcopy(pretrained_model)

        if self.extract_names is not None:
            extract_names: List[str] = (
                self.extract_names
            )  # regular expressions for the names of the parameters
        else:
            # extract the weight matrix of each linear layer
            extract_names = []
            for name, module in model.named_modules():
                if isinstance(module, nn.Linear):
                    extract_names.append(f"{name}.weight")

        ft_state_dict = finetuned_model.state_dict()
        for name, param in tqdm(
            model.named_parameters(),
            "Magnitude Pruning On Parameter Difference",
            total=len(tuple(model.named_parameters())),
        ):
            if not param.requires_grad:
                continue

            # Prune the diff parameter if its name matches
            if _is_name_matched(name, extract_names):
                w_diff = ft_state_dict[name] - param
                w_diff = _magnitude_prune(w_diff, prune_ratio=self.prune_ratio)
                param.data = param + w_diff

        return model
