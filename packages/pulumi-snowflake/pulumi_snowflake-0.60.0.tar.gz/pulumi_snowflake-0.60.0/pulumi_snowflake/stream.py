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

__all__ = ['StreamArgs', 'Stream']

@pulumi.input_type
class StreamArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 schema: pulumi.Input[str],
                 append_only: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 insert_only: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on_stage: Optional[pulumi.Input[str]] = None,
                 on_table: Optional[pulumi.Input[str]] = None,
                 on_view: Optional[pulumi.Input[str]] = None,
                 show_initial_rows: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Stream resource.
        :param pulumi.Input[str] database: The database in which to create the stream.
        :param pulumi.Input[str] schema: The schema in which to create the stream.
        :param pulumi.Input[bool] append_only: Type of the stream that will be created.
        :param pulumi.Input[str] comment: Specifies a comment for the stream.
        :param pulumi.Input[bool] insert_only: Create an insert only stream type.
        :param pulumi.Input[str] name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        :param pulumi.Input[str] on_stage: Specifies an identifier for the stage the stream will monitor.
        :param pulumi.Input[str] on_table: Specifies an identifier for the table the stream will monitor.
        :param pulumi.Input[str] on_view: Specifies an identifier for the view the stream will monitor.
        :param pulumi.Input[bool] show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "schema", schema)
        if append_only is not None:
            pulumi.set(__self__, "append_only", append_only)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if insert_only is not None:
            pulumi.set(__self__, "insert_only", insert_only)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if on_stage is not None:
            pulumi.set(__self__, "on_stage", on_stage)
        if on_table is not None:
            pulumi.set(__self__, "on_table", on_table)
        if on_view is not None:
            pulumi.set(__self__, "on_view", on_view)
        if show_initial_rows is not None:
            pulumi.set(__self__, "show_initial_rows", show_initial_rows)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        The database in which to create the stream.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Input[str]:
        """
        The schema in which to create the stream.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter(name="appendOnly")
    def append_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Type of the stream that will be created.
        """
        return pulumi.get(self, "append_only")

    @append_only.setter
    def append_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "append_only", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the stream.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter(name="insertOnly")
    def insert_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Create an insert only stream type.
        """
        return pulumi.get(self, "insert_only")

    @insert_only.setter
    def insert_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "insert_only", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="onStage")
    def on_stage(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the stage the stream will monitor.
        """
        return pulumi.get(self, "on_stage")

    @on_stage.setter
    def on_stage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_stage", value)

    @property
    @pulumi.getter(name="onTable")
    def on_table(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the table the stream will monitor.
        """
        return pulumi.get(self, "on_table")

    @on_table.setter
    def on_table(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_table", value)

    @property
    @pulumi.getter(name="onView")
    def on_view(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the view the stream will monitor.
        """
        return pulumi.get(self, "on_view")

    @on_view.setter
    def on_view(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_view", value)

    @property
    @pulumi.getter(name="showInitialRows")
    def show_initial_rows(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        return pulumi.get(self, "show_initial_rows")

    @show_initial_rows.setter
    def show_initial_rows(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "show_initial_rows", value)


@pulumi.input_type
class _StreamState:
    def __init__(__self__, *,
                 append_only: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 fully_qualified_name: Optional[pulumi.Input[str]] = None,
                 insert_only: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on_stage: Optional[pulumi.Input[str]] = None,
                 on_table: Optional[pulumi.Input[str]] = None,
                 on_view: Optional[pulumi.Input[str]] = None,
                 owner: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 show_initial_rows: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Stream resources.
        :param pulumi.Input[bool] append_only: Type of the stream that will be created.
        :param pulumi.Input[str] comment: Specifies a comment for the stream.
        :param pulumi.Input[str] database: The database in which to create the stream.
        :param pulumi.Input[str] fully_qualified_name: Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        :param pulumi.Input[bool] insert_only: Create an insert only stream type.
        :param pulumi.Input[str] name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        :param pulumi.Input[str] on_stage: Specifies an identifier for the stage the stream will monitor.
        :param pulumi.Input[str] on_table: Specifies an identifier for the table the stream will monitor.
        :param pulumi.Input[str] on_view: Specifies an identifier for the view the stream will monitor.
        :param pulumi.Input[str] owner: Name of the role that owns the stream.
        :param pulumi.Input[str] schema: The schema in which to create the stream.
        :param pulumi.Input[bool] show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        if append_only is not None:
            pulumi.set(__self__, "append_only", append_only)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if fully_qualified_name is not None:
            pulumi.set(__self__, "fully_qualified_name", fully_qualified_name)
        if insert_only is not None:
            pulumi.set(__self__, "insert_only", insert_only)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if on_stage is not None:
            pulumi.set(__self__, "on_stage", on_stage)
        if on_table is not None:
            pulumi.set(__self__, "on_table", on_table)
        if on_view is not None:
            pulumi.set(__self__, "on_view", on_view)
        if owner is not None:
            pulumi.set(__self__, "owner", owner)
        if schema is not None:
            pulumi.set(__self__, "schema", schema)
        if show_initial_rows is not None:
            pulumi.set(__self__, "show_initial_rows", show_initial_rows)

    @property
    @pulumi.getter(name="appendOnly")
    def append_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Type of the stream that will be created.
        """
        return pulumi.get(self, "append_only")

    @append_only.setter
    def append_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "append_only", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies a comment for the stream.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        The database in which to create the stream.
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
    @pulumi.getter(name="insertOnly")
    def insert_only(self) -> Optional[pulumi.Input[bool]]:
        """
        Create an insert only stream type.
        """
        return pulumi.get(self, "insert_only")

    @insert_only.setter
    def insert_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "insert_only", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="onStage")
    def on_stage(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the stage the stream will monitor.
        """
        return pulumi.get(self, "on_stage")

    @on_stage.setter
    def on_stage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_stage", value)

    @property
    @pulumi.getter(name="onTable")
    def on_table(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the table the stream will monitor.
        """
        return pulumi.get(self, "on_table")

    @on_table.setter
    def on_table(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_table", value)

    @property
    @pulumi.getter(name="onView")
    def on_view(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies an identifier for the view the stream will monitor.
        """
        return pulumi.get(self, "on_view")

    @on_view.setter
    def on_view(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "on_view", value)

    @property
    @pulumi.getter
    def owner(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the role that owns the stream.
        """
        return pulumi.get(self, "owner")

    @owner.setter
    def owner(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner", value)

    @property
    @pulumi.getter
    def schema(self) -> Optional[pulumi.Input[str]]:
        """
        The schema in which to create the stream.
        """
        return pulumi.get(self, "schema")

    @schema.setter
    def schema(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "schema", value)

    @property
    @pulumi.getter(name="showInitialRows")
    def show_initial_rows(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        return pulumi.get(self, "show_initial_rows")

    @show_initial_rows.setter
    def show_initial_rows(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "show_initial_rows", value)


class Stream(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 append_only: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 insert_only: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on_stage: Optional[pulumi.Input[str]] = None,
                 on_table: Optional[pulumi.Input[str]] = None,
                 on_view: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 show_initial_rows: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        ## Import

        format is database name | schema name | stream name

        ```sh
        $ pulumi import snowflake:index/stream:Stream example 'dbName|schemaName|streamName'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] append_only: Type of the stream that will be created.
        :param pulumi.Input[str] comment: Specifies a comment for the stream.
        :param pulumi.Input[str] database: The database in which to create the stream.
        :param pulumi.Input[bool] insert_only: Create an insert only stream type.
        :param pulumi.Input[str] name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        :param pulumi.Input[str] on_stage: Specifies an identifier for the stage the stream will monitor.
        :param pulumi.Input[str] on_table: Specifies an identifier for the table the stream will monitor.
        :param pulumi.Input[str] on_view: Specifies an identifier for the view the stream will monitor.
        :param pulumi.Input[str] schema: The schema in which to create the stream.
        :param pulumi.Input[bool] show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StreamArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        format is database name | schema name | stream name

        ```sh
        $ pulumi import snowflake:index/stream:Stream example 'dbName|schemaName|streamName'
        ```

        :param str resource_name: The name of the resource.
        :param StreamArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StreamArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 append_only: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 insert_only: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 on_stage: Optional[pulumi.Input[str]] = None,
                 on_table: Optional[pulumi.Input[str]] = None,
                 on_view: Optional[pulumi.Input[str]] = None,
                 schema: Optional[pulumi.Input[str]] = None,
                 show_initial_rows: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = StreamArgs.__new__(StreamArgs)

            __props__.__dict__["append_only"] = append_only
            __props__.__dict__["comment"] = comment
            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            __props__.__dict__["insert_only"] = insert_only
            __props__.__dict__["name"] = name
            __props__.__dict__["on_stage"] = on_stage
            __props__.__dict__["on_table"] = on_table
            __props__.__dict__["on_view"] = on_view
            if schema is None and not opts.urn:
                raise TypeError("Missing required property 'schema'")
            __props__.__dict__["schema"] = schema
            __props__.__dict__["show_initial_rows"] = show_initial_rows
            __props__.__dict__["fully_qualified_name"] = None
            __props__.__dict__["owner"] = None
        super(Stream, __self__).__init__(
            'snowflake:index/stream:Stream',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            append_only: Optional[pulumi.Input[bool]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            database: Optional[pulumi.Input[str]] = None,
            fully_qualified_name: Optional[pulumi.Input[str]] = None,
            insert_only: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            on_stage: Optional[pulumi.Input[str]] = None,
            on_table: Optional[pulumi.Input[str]] = None,
            on_view: Optional[pulumi.Input[str]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            schema: Optional[pulumi.Input[str]] = None,
            show_initial_rows: Optional[pulumi.Input[bool]] = None) -> 'Stream':
        """
        Get an existing Stream resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] append_only: Type of the stream that will be created.
        :param pulumi.Input[str] comment: Specifies a comment for the stream.
        :param pulumi.Input[str] database: The database in which to create the stream.
        :param pulumi.Input[str] fully_qualified_name: Fully qualified name of the resource. For more information, see [object name resolution](https://docs.snowflake.com/en/sql-reference/name-resolution).
        :param pulumi.Input[bool] insert_only: Create an insert only stream type.
        :param pulumi.Input[str] name: Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        :param pulumi.Input[str] on_stage: Specifies an identifier for the stage the stream will monitor.
        :param pulumi.Input[str] on_table: Specifies an identifier for the table the stream will monitor.
        :param pulumi.Input[str] on_view: Specifies an identifier for the view the stream will monitor.
        :param pulumi.Input[str] owner: Name of the role that owns the stream.
        :param pulumi.Input[str] schema: The schema in which to create the stream.
        :param pulumi.Input[bool] show_initial_rows: Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StreamState.__new__(_StreamState)

        __props__.__dict__["append_only"] = append_only
        __props__.__dict__["comment"] = comment
        __props__.__dict__["database"] = database
        __props__.__dict__["fully_qualified_name"] = fully_qualified_name
        __props__.__dict__["insert_only"] = insert_only
        __props__.__dict__["name"] = name
        __props__.__dict__["on_stage"] = on_stage
        __props__.__dict__["on_table"] = on_table
        __props__.__dict__["on_view"] = on_view
        __props__.__dict__["owner"] = owner
        __props__.__dict__["schema"] = schema
        __props__.__dict__["show_initial_rows"] = show_initial_rows
        return Stream(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appendOnly")
    def append_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Type of the stream that will be created.
        """
        return pulumi.get(self, "append_only")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a comment for the stream.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        The database in which to create the stream.
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
    @pulumi.getter(name="insertOnly")
    def insert_only(self) -> pulumi.Output[Optional[bool]]:
        """
        Create an insert only stream type.
        """
        return pulumi.get(self, "insert_only")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the identifier for the stream; must be unique for the database and schema in which the stream is created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="onStage")
    def on_stage(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies an identifier for the stage the stream will monitor.
        """
        return pulumi.get(self, "on_stage")

    @property
    @pulumi.getter(name="onTable")
    def on_table(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies an identifier for the table the stream will monitor.
        """
        return pulumi.get(self, "on_table")

    @property
    @pulumi.getter(name="onView")
    def on_view(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies an identifier for the view the stream will monitor.
        """
        return pulumi.get(self, "on_view")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        """
        Name of the role that owns the stream.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Output[str]:
        """
        The schema in which to create the stream.
        """
        return pulumi.get(self, "schema")

    @property
    @pulumi.getter(name="showInitialRows")
    def show_initial_rows(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to return all existing rows in the source table as row inserts the first time the stream is consumed.
        """
        return pulumi.get(self, "show_initial_rows")

