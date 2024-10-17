# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""AL360° Trustworthy AI Text SDK package."""

from al360_trustworthyai_text.common.constants import ModelTask
from al360_trustworthyai_text.al360_tai_text_insights import RAITextInsights

from .version import name, version

__name__ = name
__version__ = version

__all__ = ['ModelTask', 'RAITextInsights']
