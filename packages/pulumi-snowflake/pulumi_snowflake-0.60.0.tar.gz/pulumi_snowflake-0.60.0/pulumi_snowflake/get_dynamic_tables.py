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
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetDynamicTablesResult',
    'AwaitableGetDynamicTablesResult',
    'get_dynamic_tables',
    'get_dynamic_tables_output',
]

@pulumi.output_type
class GetDynamicTablesResult:
    """
    A collection of values returned by getDynamicTables.
    """
    def __init__(__self__, id=None, in_=None, like=None, limit=None, records=None, starts_with=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if in_ and not isinstance(in_, dict):
            raise TypeError("Expected argument 'in_' to be a dict")
        pulumi.set(__self__, "in_", in_)
        if like and not isinstance(like, dict):
            raise TypeError("Expected argument 'like' to be a dict")
        pulumi.set(__self__, "like", like)
        if limit and not isinstance(limit, dict):
            raise TypeError("Expected argument 'limit' to be a dict")
        pulumi.set(__self__, "limit", limit)
        if records and not isinstance(records, list):
            raise TypeError("Expected argument 'records' to be a list")
        pulumi.set(__self__, "records", records)
        if starts_with and not isinstance(starts_with, str):
            raise TypeError("Expected argument 'starts_with' to be a str")
        pulumi.set(__self__, "starts_with", starts_with)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="in")
    def in_(self) -> Optional['outputs.GetDynamicTablesInResult']:
        """
        IN clause to filter the list of dynamic tables.
        """
        return pulumi.get(self, "in_")

    @property
    @pulumi.getter
    def like(self) -> Optional['outputs.GetDynamicTablesLikeResult']:
        """
        LIKE clause to filter the list of dynamic tables.
        """
        return pulumi.get(self, "like")

    @property
    @pulumi.getter
    def limit(self) -> Optional['outputs.GetDynamicTablesLimitResult']:
        """
        Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. Note that the actual number of rows returned might be less than the specified limit (e.g. the number of existing objects is less than the specified limit).
        """
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def records(self) -> Sequence['outputs.GetDynamicTablesRecordResult']:
        """
        The list of dynamic tables.
        """
        return pulumi.get(self, "records")

    @property
    @pulumi.getter(name="startsWith")
    def starts_with(self) -> Optional[str]:
        """
        Optionally filters the command output based on the characters that appear at the beginning of the object name. The string is case-sensitive.
        """
        return pulumi.get(self, "starts_with")


class AwaitableGetDynamicTablesResult(GetDynamicTablesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDynamicTablesResult(
            id=self.id,
            in_=self.in_,
            like=self.like,
            limit=self.limit,
            records=self.records,
            starts_with=self.starts_with)


def get_dynamic_tables(in_: Optional[Union['GetDynamicTablesInArgs', 'GetDynamicTablesInArgsDict']] = None,
                       like: Optional[Union['GetDynamicTablesLikeArgs', 'GetDynamicTablesLikeArgsDict']] = None,
                       limit: Optional[Union['GetDynamicTablesLimitArgs', 'GetDynamicTablesLimitArgsDict']] = None,
                       starts_with: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDynamicTablesResult:
    """
    Use this data source to access information about an existing resource.

    :param Union['GetDynamicTablesInArgs', 'GetDynamicTablesInArgsDict'] in_: IN clause to filter the list of dynamic tables.
    :param Union['GetDynamicTablesLikeArgs', 'GetDynamicTablesLikeArgsDict'] like: LIKE clause to filter the list of dynamic tables.
    :param Union['GetDynamicTablesLimitArgs', 'GetDynamicTablesLimitArgsDict'] limit: Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. Note that the actual number of rows returned might be less than the specified limit (e.g. the number of existing objects is less than the specified limit).
    :param str starts_with: Optionally filters the command output based on the characters that appear at the beginning of the object name. The string is case-sensitive.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getDynamicTables:getDynamicTables', __args__, opts=opts, typ=GetDynamicTablesResult).value

    return AwaitableGetDynamicTablesResult(
        id=pulumi.get(__ret__, 'id'),
        in_=pulumi.get(__ret__, 'in_'),
        like=pulumi.get(__ret__, 'like'),
        limit=pulumi.get(__ret__, 'limit'),
        records=pulumi.get(__ret__, 'records'),
        starts_with=pulumi.get(__ret__, 'starts_with'))
def get_dynamic_tables_output(in_: Optional[pulumi.Input[Optional[Union['GetDynamicTablesInArgs', 'GetDynamicTablesInArgsDict']]]] = None,
                              like: Optional[pulumi.Input[Optional[Union['GetDynamicTablesLikeArgs', 'GetDynamicTablesLikeArgsDict']]]] = None,
                              limit: Optional[pulumi.Input[Optional[Union['GetDynamicTablesLimitArgs', 'GetDynamicTablesLimitArgsDict']]]] = None,
                              starts_with: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDynamicTablesResult]:
    """
    Use this data source to access information about an existing resource.

    :param Union['GetDynamicTablesInArgs', 'GetDynamicTablesInArgsDict'] in_: IN clause to filter the list of dynamic tables.
    :param Union['GetDynamicTablesLikeArgs', 'GetDynamicTablesLikeArgsDict'] like: LIKE clause to filter the list of dynamic tables.
    :param Union['GetDynamicTablesLimitArgs', 'GetDynamicTablesLimitArgsDict'] limit: Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. Note that the actual number of rows returned might be less than the specified limit (e.g. the number of existing objects is less than the specified limit).
    :param str starts_with: Optionally filters the command output based on the characters that appear at the beginning of the object name. The string is case-sensitive.
    """
    __args__ = dict()
    __args__['in'] = in_
    __args__['like'] = like
    __args__['limit'] = limit
    __args__['startsWith'] = starts_with
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getDynamicTables:getDynamicTables', __args__, opts=opts, typ=GetDynamicTablesResult)
    return __ret__.apply(lambda __response__: GetDynamicTablesResult(
        id=pulumi.get(__response__, 'id'),
        in_=pulumi.get(__response__, 'in_'),
        like=pulumi.get(__response__, 'like'),
        limit=pulumi.get(__response__, 'limit'),
        records=pulumi.get(__response__, 'records'),
        starts_with=pulumi.get(__response__, 'starts_with')))
