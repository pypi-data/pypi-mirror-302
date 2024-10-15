# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import sys
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
if sys.version_info >= (3, 11):
    from typing import NotRequired, TypedDict, TypeAlias
else:
    from typing_extensions import NotRequired, TypedDict, TypeAlias
from .. import _utilities

import types

__config__ = pulumi.Config('datarobot')


class _ExportableConfig(types.ModuleType):
    @property
    def apikey(self) -> Optional[str]:
        """
        Key to access DataRobot API
        """
        return __config__.get('apikey')

    @property
    def endpoint(self) -> Optional[str]:
        """
        Endpoint for the DataRobot API
        """
        return __config__.get('endpoint')

