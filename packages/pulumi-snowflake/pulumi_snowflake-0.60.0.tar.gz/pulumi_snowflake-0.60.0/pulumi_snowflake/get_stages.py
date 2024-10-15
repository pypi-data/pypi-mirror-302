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

__all__ = [
    'GetStagesResult',
    'AwaitableGetStagesResult',
    'get_stages',
    'get_stages_output',
]

@pulumi.output_type
class GetStagesResult:
    """
    A collection of values returned by getStages.
    """
    def __init__(__self__, database=None, id=None, schema=None, stages=None):
        if database and not isinstance(database, str):
            raise TypeError("Expected argument 'database' to be a str")
        pulumi.set(__self__, "database", database)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if schema and not isinstance(schema, str):
            raise TypeError("Expected argument 'schema' to be a str")
        pulumi.set(__self__, "schema", schema)
        if stages and not isinstance(stages, list):
            raise TypeError("Expected argument 'stages' to be a list")
        pulumi.set(__self__, "stages", stages)

    @property
    @pulumi.getter
    def database(self) -> str:
        """
        The database from which to return the schemas from.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def schema(self) -> str:
        """
        The schema from which to return the stages from.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter
    def stages(self) -> Sequence['outputs.GetStagesStageResult']:
        """
        The stages in the schema
        """
        return pulumi.get(self, "stages")


class AwaitableGetStagesResult(GetStagesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStagesResult(
            database=self.database,
            id=self.id,
            schema=self.schema,
            stages=self.stages)


def get_stages(database: Optional[str] = None,
               schema: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStagesResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_stages(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the schemas from.
    :param str schema: The schema from which to return the stages from.
    """
    __args__ = dict()
    __args__['database'] = database
    __args__['schema'] = schema
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('snowflake:index/getStages:getStages', __args__, opts=opts, typ=GetStagesResult).value

    return AwaitableGetStagesResult(
        database=pulumi.get(__ret__, 'database'),
        id=pulumi.get(__ret__, 'id'),
        schema=pulumi.get(__ret__, 'schema'),
        stages=pulumi.get(__ret__, 'stages'))
def get_stages_output(database: Optional[pulumi.Input[str]] = None,
                      schema: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStagesResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_stages(database="MYDB",
        schema="MYSCHEMA")
    ```


    :param str database: The database from which to return the schemas from.
    :param str schema: The schema from which to return the stages from.
    """
    __args__ = dict()
    __args__['database'] = database
    __args__['schema'] = schema
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke_output('snowflake:index/getStages:getStages', __args__, opts=opts, typ=GetStagesResult)
    return __ret__.apply(lambda __response__: GetStagesResult(
        database=pulumi.get(__response__, 'database'),
        id=pulumi.get(__response__, 'id'),
        schema=pulumi.get(__response__, 'schema'),
        stages=pulumi.get(__response__, 'stages')))
