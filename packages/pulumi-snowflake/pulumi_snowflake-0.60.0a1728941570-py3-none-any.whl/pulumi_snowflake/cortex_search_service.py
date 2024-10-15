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

__all__ = ['CortexSearchServiceArgs', 'CortexSearchService']

@pulumi.input_type
class CortexSearchServiceArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 on: pulumi.Input[str],
                 query: pulumi.Input[str],
                 schema: pulumi.Input[str],
                 target_lag: pulumi.Input[str],
                 warehouse: pulumi.Input[str],
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CortexSearchService resource.
        :param pulumi.Input[str] database: The database in which to create the Cortex search service.
        :param pulumi.Input[str] on: Specifies the column to use as the search column for the Cortex search service; must be a text value.
        :param pulumi.Input[str] query: Specifies the query to use to populate the Cortex search service.
        :param pulumi.Input[str] schema: The schema in which to create the Cortex search service.
        :param pulumi.Input[str] target_lag: Specifies the maximum target lag time for the Cortex search service.
        :param pulumi.Input[str] warehouse: The warehouse in which to create the Cortex search service.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attributes: Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        :param pulumi.Input[str] comment: Specifies a comment for the Cortex search service.
        :param pulumi.Input[str] name: Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "on", on)
        pulumi.set(__self__, "query", query)
        pulumi.set(__self__, "schema", schema)
        pulumi.set(__self__, "target_lag", target_lag)
        pulumi.set(__self__, "warehouse", warehouse)
        if attributes is not None:
            pulumi.set(__self__, "attributes", attributes)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        The database in which to create the Cortex search service.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def on(self) -> pulumi.Input[str]:
        """
        Specifies the column to use as the search column for the Cortex search service; must be a text value.
        """
        return pulumi.get(self, "on")

    @on.setter
    def on(self, value: pulumi.Input[str]):
        pulumi.set(self, "on", value)

    @property
    @pulumi.getter
    def query(self) -> pulumi.Input[str]:
        """
        Specifies the query to use to populate the Cortex search service.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: pulumi.Input[str]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Input[str]:
        """
        The schema in which to create the Cortex search service.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter(name="targetLag")
    def target_lag(self) -> pulumi.Input[str]:
        """
        Specifies the maximum target lag time for the Cortex search service.
        """
        return pulumi.get(self, "target_lag")

    @target_lag.setter
    def target_lag(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_lag", value)

    @property
    @pulumi.getter
    def warehouse(self) -> pulumi.Input[str]:
        """
        The warehouse in which to create the Cortex search service.
        """
        return pulumi.get(self, "warehouse")

    @warehouse.setter
    def warehouse(self, value: pulumi.Input[str]):
        pulumi.set(self, "warehouse", value)

    @property
    @pulumi.getter
    def attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the Cortex search service.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _CortexSearchServiceState:
    def __init__(__self__, *,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 created_on: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 fully_qualified_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 target_lag: Optional[pulumi.Input[str]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CortexSearchService resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attributes: Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        :param pulumi.Input[str] comment: Specifies a comment for the Cortex search service.
        :param pulumi.Input[str] created_on: Creation date for the given Cortex search service.
        :param pulumi.Input[str] database: The database in which to create the Cortex search service.
        :param pulumi.Input[str] fully_qualified_name: Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        :param pulumi.Input[str] name: Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        :param pulumi.Input[str] on: Specifies the column to use as the search column for the Cortex search service; must be a text value.
        :param pulumi.Input[str] query: Specifies the query to use to populate the Cortex search service.
        :param pulumi.Input[str] schema: The schema in which to create the Cortex search service.
        :param pulumi.Input[str] target_lag: Specifies the maximum target lag time for the Cortex search service.
        :param pulumi.Input[str] warehouse: The warehouse in which to create the Cortex search service.
        """
        if attributes is not None:
            pulumi.set(__self__, "attributes", attributes)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if created_on is not None:
            pulumi.set(__self__, "created_on", created_on)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if fully_qualified_name is not None:
            pulumi.set(__self__, "fully_qualified_name", fully_qualified_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if on is not None:
            pulumi.set(__self__, "on", on)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if schema is not None:
            pulumi.set(__self__, "schema", schema)
        if target_lag is not None:
            pulumi.set(__self__, "target_lag", target_lag)
        if warehouse is not None:
            pulumi.set(__self__, "warehouse", warehouse)

    @property
    @pulumi.getter
    def attributes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        """
        return pulumi.get(self, "attributes")

    @attributes.setter
    def attributes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "attributes", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the Cortex search service.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> Optional[pulumi.Input[str]]:
        """
        Creation date for the given Cortex search service.
        """
        return pulumi.get(self, "created_on")

    @created_on.setter
    def created_on(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_on", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        The database in which to create the Cortex search service.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter(name="fullyQualifiedName")
    def fully_qualified_name(self) -> Optional[pulumi.Input[str]]:
        """
        Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        """
        return pulumi.get(self, "fully_qualified_name")

    @fully_qualified_name.setter
    def fully_qualified_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fully_qualified_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def on(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the column to use as the search column for the Cortex search service; must be a text value.
        """
        return pulumi.get(self, "on")

    @on.setter
    def on(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on", value)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the query to use to populate the Cortex search service.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter
    def schema(self) -> Optional[pulumi.Input[str]]:
        """
        The schema in which to create the Cortex search service.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter(name="targetLag")
    def target_lag(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the maximum target lag time for the Cortex search service.
        """
        return pulumi.get(self, "target_lag")

    @target_lag.setter
    def target_lag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_lag", value)

    @property
    @pulumi.getter
    def warehouse(self) -> Optional[pulumi.Input[str]]:
        """
        The warehouse in which to create the Cortex search service.
        """
        return pulumi.get(self, "warehouse")

    @warehouse.setter
    def warehouse(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "warehouse", value)


class CortexSearchService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 target_lag: Optional[pulumi.Input[str]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        ```sh
        $ pulumi import snowflake:index/cortexSearchService:CortexSearchService example 'dbName|schemaName|fileFormatName'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attributes: Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        :param pulumi.Input[str] comment: Specifies a comment for the Cortex search service.
        :param pulumi.Input[str] database: The database in which to create the Cortex search service.
        :param pulumi.Input[str] name: Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        :param pulumi.Input[str] on: Specifies the column to use as the search column for the Cortex search service; must be a text value.
        :param pulumi.Input[str] query: Specifies the query to use to populate the Cortex search service.
        :param pulumi.Input[str] schema: The schema in which to create the Cortex search service.
        :param pulumi.Input[str] target_lag: Specifies the maximum target lag time for the Cortex search service.
        :param pulumi.Input[str] warehouse: The warehouse in which to create the Cortex search service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CortexSearchServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        ```sh
        $ pulumi import snowflake:index/cortexSearchService:CortexSearchService example 'dbName|schemaName|fileFormatName'
        ```

        :param str resource_name: The name of the resource.
        :param CortexSearchServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CortexSearchServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 target_lag: Optional[pulumi.Input[str]] = None,
                 warehouse: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CortexSearchServiceArgs.__new__(CortexSearchServiceArgs)

            __props__.__dict__["attributes"] = attributes
            __props__.__dict__["comment"] = comment
            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            __props__.__dict__["name"] = name
            if on is None and not opts.urn:
                raise TypeError("Missing required property 'on'")
            __props__.__dict__["on"] = on
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__.__dict__["query"] = query
            if schema is None and not opts.urn:
                raise TypeError("Missing required property 'schema'")
            __props__.__dict__["schema"] = schema
            if target_lag is None and not opts.urn:
                raise TypeError("Missing required property 'target_lag'")
            __props__.__dict__["target_lag"] = target_lag
            if warehouse is None and not opts.urn:
                raise TypeError("Missing required property 'warehouse'")
            __props__.__dict__["warehouse"] = warehouse
            __props__.__dict__["created_on"] = None
            __props__.__dict__["fully_qualified_name"] = None
        super(CortexSearchService, __self__).__init__(
            'snowflake:index/cortexSearchService:CortexSearchService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attributes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            created_on: Optional[pulumi.Input[str]] = None,
            database: Optional[pulumi.Input[str]] = None,
            fully_qualified_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            on: Optional[pulumi.Input[str]] = None,
            query: Optional[pulumi.Input[str]] = None,
            schema: Optional[pulumi.Input[str]] = None,
            target_lag: Optional[pulumi.Input[str]] = None,
            warehouse: Optional[pulumi.Input[str]] = None) -> 'CortexSearchService':
        """
        Get an existing CortexSearchService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attributes: Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        :param pulumi.Input[str] comment: Specifies a comment for the Cortex search service.
        :param pulumi.Input[str] created_on: Creation date for the given Cortex search service.
        :param pulumi.Input[str] database: The database in which to create the Cortex search service.
        :param pulumi.Input[str] fully_qualified_name: Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        :param pulumi.Input[str] name: Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        :param pulumi.Input[str] on: Specifies the column to use as the search column for the Cortex search service; must be a text value.
        :param pulumi.Input[str] query: Specifies the query to use to populate the Cortex search service.
        :param pulumi.Input[str] schema: The schema in which to create the Cortex search service.
        :param pulumi.Input[str] target_lag: Specifies the maximum target lag time for the Cortex search service.
        :param pulumi.Input[str] warehouse: The warehouse in which to create the Cortex search service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CortexSearchServiceState.__new__(_CortexSearchServiceState)

        __props__.__dict__["attributes"] = attributes
        __props__.__dict__["comment"] = comment
        __props__.__dict__["created_on"] = created_on
        __props__.__dict__["database"] = database
        __props__.__dict__["fully_qualified_name"] = fully_qualified_name
        __props__.__dict__["name"] = name
        __props__.__dict__["on"] = on
        __props__.__dict__["query"] = query
        __props__.__dict__["schema"] = schema
        __props__.__dict__["target_lag"] = target_lag
        __props__.__dict__["warehouse"] = warehouse
        return CortexSearchService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies the list of columns in the base table to enable filtering on when issuing queries to the service.
        """
        return pulumi.get(self, "attributes")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the Cortex search service.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> pulumi.Output[str]:
        """
        Creation date for the given Cortex search service.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The database in which to create the Cortex search service.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter(name="fullyQualifiedName")
    def fully_qualified_name(self) -> pulumi.Output[str]:
        """
        Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        """
        return pulumi.get(self, "fully_qualified_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Cortex search service. The name must be unique for the schema in which the service is created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def on(self) -> pulumi.Output[str]:
        """
        Specifies the column to use as the search column for the Cortex search service; must be a text value.
        """
        return pulumi.get(self, "on")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        Specifies the query to use to populate the Cortex search service.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Output[str]:
        """
        The schema in which to create the Cortex search service.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter(name="targetLag")
    def target_lag(self) -> pulumi.Output[str]:
        """
        Specifies the maximum target lag time for the Cortex search service.
        """
        return pulumi.get(self, "target_lag")

    @property
    @pulumi.getter
    def warehouse(self) -> pulumi.Output[str]:
        """
        The warehouse in which to create the Cortex search service.
        """
        return pulumi.get(self, "warehouse")

