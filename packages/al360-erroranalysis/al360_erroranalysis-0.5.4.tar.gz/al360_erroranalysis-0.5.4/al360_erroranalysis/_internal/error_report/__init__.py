# Copyright (c) AffectLog SAS
# Licensed under the MIT License.

"""Init file, used for backwards compatibility."""
from al360_erroranalysis.report import ErrorReport, as_error_report, json_converter

__all__ = ['ErrorReport',
           'as_error_report',
           'json_converter']
