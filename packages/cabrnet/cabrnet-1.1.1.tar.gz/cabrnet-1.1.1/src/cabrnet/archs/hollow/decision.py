from __future__ import annotations

from typing import Any
from torch import Tensor
from cabrnet.archs.generic.decision import CaBRNetClassifier


class HollowClassifier(CaBRNetClassifier):
    r"""Dummy classifier."""

    def __init__(
        self,
        similarity_config: dict[str, Any],
        num_classes: int,
        num_features: int,
        proto_init_mode: str = "SHIFTED_NORMAL",
        **kwargs,
    ) -> None:
        r"""Initializes a ProtoPool classifier.

        Args:
            similarity_config (dict): Configuration of the layer used to compute similarity scores between the
                prototypes and the convolutional features.
            num_classes (int): Number of classes.
            num_features (int): Number of features (size of each prototype).
            proto_init_mode (str, optional): Init mode for prototypes. Default: UNIFORM.
        """
        super().__init__(num_classes=num_classes, num_features=num_features)

    def prototype_is_active(self, proto_idx: int) -> bool:
        r"""Is the prototype *proto_idx* active or disabled?

        Args:
            proto_idx (int): Prototype index.
        """
        return False

    def forward(self, features: Tensor, **kwargs) -> Tensor:
        r"""Returns the features unchanged.

        Args:
            features (tensor): Input features.
        """
        return features
