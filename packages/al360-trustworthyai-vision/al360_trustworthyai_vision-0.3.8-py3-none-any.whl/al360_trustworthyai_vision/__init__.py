# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""AL360° Trustworthy AI Vision SDK package."""

from al360_trustworthyai_vision.common.constants import ModelTask
from al360_trustworthyai_vision.al360_tai_vision_insights import RAIVisionInsights

from .version import name, version

__name__ = name
__version__ = version

__all__ = ['ModelTask', 'RAIVisionInsights']
