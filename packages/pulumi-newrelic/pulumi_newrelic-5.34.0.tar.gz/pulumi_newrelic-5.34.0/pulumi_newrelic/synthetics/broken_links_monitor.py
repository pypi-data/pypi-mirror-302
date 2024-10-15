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
from . import outputs
from ._inputs import *

__all__ = ['BrokenLinksMonitorArgs', 'BrokenLinksMonitor']

@pulumi.input_type
class BrokenLinksMonitorArgs:
    def __init__(__self__, *,
                 period: pulumi.Input[str],
                 status: pulumi.Input[str],
                 uri: pulumi.Input[str],
                 account_id: Optional[pulumi.Input[str]] = None,
                 locations_privates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 locations_publics: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 runtime_type: Optional[pulumi.Input[str]] = None,
                 runtime_type_version: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]] = None,
                 use_unsupported_legacy_runtime: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a BrokenLinksMonitor resource.
        :param pulumi.Input[str] period: The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        :param pulumi.Input[str] status: The monitor status (ENABLED or DISABLED).
        :param pulumi.Input[str] uri: The URI the monitor runs against.
        :param pulumi.Input[str] account_id: The account in which the Synthetics monitor will be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_privates: The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_publics: The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        :param pulumi.Input[str] name: The name for the monitor.
        :param pulumi.Input[str] runtime_type: The runtime that the monitor will use to run jobs.
        :param pulumi.Input[str] runtime_type_version: The specific semver version of the runtime type.
        :param pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]] tags: The tags that will be associated with the monitor. See Nested tag blocks below for details
        """
        pulumi.set(__self__, "period", period)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "uri", uri)
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if locations_privates is not None:
            pulumi.set(__self__, "locations_privates", locations_privates)
        if locations_publics is not None:
            pulumi.set(__self__, "locations_publics", locations_publics)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if runtime_type is not None:
            pulumi.set(__self__, "runtime_type", runtime_type)
        if runtime_type_version is not None:
            pulumi.set(__self__, "runtime_type_version", runtime_type_version)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if use_unsupported_legacy_runtime is not None:
            pulumi.set(__self__, "use_unsupported_legacy_runtime", use_unsupported_legacy_runtime)

    @property
    @pulumi.getter
    def period(self) -> pulumi.Input[str]:
        """
        The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        """
        return pulumi.get(self, "period")

    @period.setter
    def period(self, value: pulumi.Input[str]):
        pulumi.set(self, "period", value)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[str]:
        """
        The monitor status (ENABLED or DISABLED).
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[str]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Input[str]:
        """
        The URI the monitor runs against.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account in which the Synthetics monitor will be created.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter(name="locationsPrivates")
    def locations_privates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        """
        return pulumi.get(self, "locations_privates")

    @locations_privates.setter
    def locations_privates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "locations_privates", value)

    @property
    @pulumi.getter(name="locationsPublics")
    def locations_publics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        """
        return pulumi.get(self, "locations_publics")

    @locations_publics.setter
    def locations_publics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "locations_publics", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the monitor.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="runtimeType")
    def runtime_type(self) -> Optional[pulumi.Input[str]]:
        """
        The runtime that the monitor will use to run jobs.
        """
        return pulumi.get(self, "runtime_type")

    @runtime_type.setter
    def runtime_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_type", value)

    @property
    @pulumi.getter(name="runtimeTypeVersion")
    def runtime_type_version(self) -> Optional[pulumi.Input[str]]:
        """
        The specific semver version of the runtime type.
        """
        return pulumi.get(self, "runtime_type_version")

    @runtime_type_version.setter
    def runtime_type_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_type_version", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]]:
        """
        The tags that will be associated with the monitor. See Nested tag blocks below for details
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="useUnsupportedLegacyRuntime")
    def use_unsupported_legacy_runtime(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "use_unsupported_legacy_runtime")

    @use_unsupported_legacy_runtime.setter
    def use_unsupported_legacy_runtime(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_unsupported_legacy_runtime", value)


@pulumi.input_type
class _BrokenLinksMonitorState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[str]] = None,
                 guid: Optional[pulumi.Input[str]] = None,
                 locations_privates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 locations_publics: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[str]] = None,
                 period_in_minutes: Optional[pulumi.Input[int]] = None,
                 runtime_type: Optional[pulumi.Input[str]] = None,
                 runtime_type_version: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 use_unsupported_legacy_runtime: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering BrokenLinksMonitor resources.
        :param pulumi.Input[str] account_id: The account in which the Synthetics monitor will be created.
        :param pulumi.Input[str] guid: The unique entity identifier of the monitor in New Relic.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_privates: The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_publics: The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        :param pulumi.Input[str] name: The name for the monitor.
        :param pulumi.Input[str] period: The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        :param pulumi.Input[int] period_in_minutes: The interval in minutes at which Synthetic monitor should run.
        :param pulumi.Input[str] runtime_type: The runtime that the monitor will use to run jobs.
        :param pulumi.Input[str] runtime_type_version: The specific semver version of the runtime type.
        :param pulumi.Input[str] status: The monitor status (ENABLED or DISABLED).
        :param pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]] tags: The tags that will be associated with the monitor. See Nested tag blocks below for details
        :param pulumi.Input[str] uri: The URI the monitor runs against.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if guid is not None:
            pulumi.set(__self__, "guid", guid)
        if locations_privates is not None:
            pulumi.set(__self__, "locations_privates", locations_privates)
        if locations_publics is not None:
            pulumi.set(__self__, "locations_publics", locations_publics)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if period is not None:
            pulumi.set(__self__, "period", period)
        if period_in_minutes is not None:
            pulumi.set(__self__, "period_in_minutes", period_in_minutes)
        if runtime_type is not None:
            pulumi.set(__self__, "runtime_type", runtime_type)
        if runtime_type_version is not None:
            pulumi.set(__self__, "runtime_type_version", runtime_type_version)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)
        if use_unsupported_legacy_runtime is not None:
            pulumi.set(__self__, "use_unsupported_legacy_runtime", use_unsupported_legacy_runtime)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[str]]:
        """
        The account in which the Synthetics monitor will be created.
        """
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def guid(self) -> Optional[pulumi.Input[str]]:
        """
        The unique entity identifier of the monitor in New Relic.
        """
        return pulumi.get(self, "guid")

    @guid.setter
    def guid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "guid", value)

    @property
    @pulumi.getter(name="locationsPrivates")
    def locations_privates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        """
        return pulumi.get(self, "locations_privates")

    @locations_privates.setter
    def locations_privates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "locations_privates", value)

    @property
    @pulumi.getter(name="locationsPublics")
    def locations_publics(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        """
        return pulumi.get(self, "locations_publics")

    @locations_publics.setter
    def locations_publics(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "locations_publics", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the monitor.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def period(self) -> Optional[pulumi.Input[str]]:
        """
        The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        """
        return pulumi.get(self, "period")

    @period.setter
    def period(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "period", value)

    @property
    @pulumi.getter(name="periodInMinutes")
    def period_in_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        The interval in minutes at which Synthetic monitor should run.
        """
        return pulumi.get(self, "period_in_minutes")

    @period_in_minutes.setter
    def period_in_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "period_in_minutes", value)

    @property
    @pulumi.getter(name="runtimeType")
    def runtime_type(self) -> Optional[pulumi.Input[str]]:
        """
        The runtime that the monitor will use to run jobs.
        """
        return pulumi.get(self, "runtime_type")

    @runtime_type.setter
    def runtime_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_type", value)

    @property
    @pulumi.getter(name="runtimeTypeVersion")
    def runtime_type_version(self) -> Optional[pulumi.Input[str]]:
        """
        The specific semver version of the runtime type.
        """
        return pulumi.get(self, "runtime_type_version")

    @runtime_type_version.setter
    def runtime_type_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "runtime_type_version", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The monitor status (ENABLED or DISABLED).
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]]:
        """
        The tags that will be associated with the monitor. See Nested tag blocks below for details
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BrokenLinksMonitorTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI the monitor runs against.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter(name="useUnsupportedLegacyRuntime")
    def use_unsupported_legacy_runtime(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "use_unsupported_legacy_runtime")

    @use_unsupported_legacy_runtime.setter
    def use_unsupported_legacy_runtime(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_unsupported_legacy_runtime", value)


class BrokenLinksMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 locations_privates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 locations_publics: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[str]] = None,
                 runtime_type: Optional[pulumi.Input[str]] = None,
                 runtime_type_version: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BrokenLinksMonitorTagArgs', 'BrokenLinksMonitorTagArgsDict']]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 use_unsupported_legacy_runtime: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.synthetics.BrokenLinksMonitor("foo",
            name="Sample Broken Links Monitor",
            uri="https://www.one.example.com",
            locations_publics=["AP_SOUTH_1"],
            period="EVERY_6_HOURS",
            status="ENABLED",
            runtime_type="NODE_API",
            runtime_type_version="16.10",
            tags=[{
                "key": "some_key",
                "values": ["some_value"],
            }])
        ```
        See additional examples.

        ## Additional Examples

        ### Create a monitor with a private location

        The below example shows how you can define a private location and attach it to a monitor.

        > **NOTE:** It can take up to 10 minutes for a private location to become available.

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.synthetics.PrivateLocation("foo",
            name="Sample Private Location",
            description="Sample Private Location Description",
            verified_script_execution=False)
        foo_broken_links_monitor = newrelic.synthetics.BrokenLinksMonitor("foo",
            name="Sample Broken Links Monitor",
            uri="https://www.one.example.com",
            locations_privates=[foo.id],
            period="EVERY_6_HOURS",
            status="ENABLED",
            tags=[{
                "key": "some_key",
                "values": ["some_value"],
            }])
        ```

        ## Import

        A broken links monitor can be imported using its GUID, using the following command.

        bash

        ```sh
        $ pulumi import newrelic:synthetics/brokenLinksMonitor:BrokenLinksMonitor monitor <guid>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account in which the Synthetics monitor will be created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_privates: The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_publics: The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        :param pulumi.Input[str] name: The name for the monitor.
        :param pulumi.Input[str] period: The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        :param pulumi.Input[str] runtime_type: The runtime that the monitor will use to run jobs.
        :param pulumi.Input[str] runtime_type_version: The specific semver version of the runtime type.
        :param pulumi.Input[str] status: The monitor status (ENABLED or DISABLED).
        :param pulumi.Input[Sequence[pulumi.Input[Union['BrokenLinksMonitorTagArgs', 'BrokenLinksMonitorTagArgsDict']]]] tags: The tags that will be associated with the monitor. See Nested tag blocks below for details
        :param pulumi.Input[str] uri: The URI the monitor runs against.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BrokenLinksMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.synthetics.BrokenLinksMonitor("foo",
            name="Sample Broken Links Monitor",
            uri="https://www.one.example.com",
            locations_publics=["AP_SOUTH_1"],
            period="EVERY_6_HOURS",
            status="ENABLED",
            runtime_type="NODE_API",
            runtime_type_version="16.10",
            tags=[{
                "key": "some_key",
                "values": ["some_value"],
            }])
        ```
        See additional examples.

        ## Additional Examples

        ### Create a monitor with a private location

        The below example shows how you can define a private location and attach it to a monitor.

        > **NOTE:** It can take up to 10 minutes for a private location to become available.

        ```python
        import pulumi
        import pulumi_newrelic as newrelic

        foo = newrelic.synthetics.PrivateLocation("foo",
            name="Sample Private Location",
            description="Sample Private Location Description",
            verified_script_execution=False)
        foo_broken_links_monitor = newrelic.synthetics.BrokenLinksMonitor("foo",
            name="Sample Broken Links Monitor",
            uri="https://www.one.example.com",
            locations_privates=[foo.id],
            period="EVERY_6_HOURS",
            status="ENABLED",
            tags=[{
                "key": "some_key",
                "values": ["some_value"],
            }])
        ```

        ## Import

        A broken links monitor can be imported using its GUID, using the following command.

        bash

        ```sh
        $ pulumi import newrelic:synthetics/brokenLinksMonitor:BrokenLinksMonitor monitor <guid>
        ```

        :param str resource_name: The name of the resource.
        :param BrokenLinksMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BrokenLinksMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_id: Optional[pulumi.Input[str]] = None,
                 locations_privates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 locations_publics: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 period: Optional[pulumi.Input[str]] = None,
                 runtime_type: Optional[pulumi.Input[str]] = None,
                 runtime_type_version: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BrokenLinksMonitorTagArgs', 'BrokenLinksMonitorTagArgsDict']]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 use_unsupported_legacy_runtime: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BrokenLinksMonitorArgs.__new__(BrokenLinksMonitorArgs)

            __props__.__dict__["account_id"] = account_id
            __props__.__dict__["locations_privates"] = locations_privates
            __props__.__dict__["locations_publics"] = locations_publics
            __props__.__dict__["name"] = name
            if period is None and not opts.urn:
                raise TypeError("Missing required property 'period'")
            __props__.__dict__["period"] = period
            __props__.__dict__["runtime_type"] = runtime_type
            __props__.__dict__["runtime_type_version"] = runtime_type_version
            if status is None and not opts.urn:
                raise TypeError("Missing required property 'status'")
            __props__.__dict__["status"] = status
            __props__.__dict__["tags"] = tags
            if uri is None and not opts.urn:
                raise TypeError("Missing required property 'uri'")
            __props__.__dict__["uri"] = uri
            __props__.__dict__["use_unsupported_legacy_runtime"] = use_unsupported_legacy_runtime
            __props__.__dict__["guid"] = None
            __props__.__dict__["period_in_minutes"] = None
        super(BrokenLinksMonitor, __self__).__init__(
            'newrelic:synthetics/brokenLinksMonitor:BrokenLinksMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[str]] = None,
            guid: Optional[pulumi.Input[str]] = None,
            locations_privates: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            locations_publics: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            period: Optional[pulumi.Input[str]] = None,
            period_in_minutes: Optional[pulumi.Input[int]] = None,
            runtime_type: Optional[pulumi.Input[str]] = None,
            runtime_type_version: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[Union['BrokenLinksMonitorTagArgs', 'BrokenLinksMonitorTagArgsDict']]]]] = None,
            uri: Optional[pulumi.Input[str]] = None,
            use_unsupported_legacy_runtime: Optional[pulumi.Input[bool]] = None) -> 'BrokenLinksMonitor':
        """
        Get an existing BrokenLinksMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_id: The account in which the Synthetics monitor will be created.
        :param pulumi.Input[str] guid: The unique entity identifier of the monitor in New Relic.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_privates: The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] locations_publics: The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        :param pulumi.Input[str] name: The name for the monitor.
        :param pulumi.Input[str] period: The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        :param pulumi.Input[int] period_in_minutes: The interval in minutes at which Synthetic monitor should run.
        :param pulumi.Input[str] runtime_type: The runtime that the monitor will use to run jobs.
        :param pulumi.Input[str] runtime_type_version: The specific semver version of the runtime type.
        :param pulumi.Input[str] status: The monitor status (ENABLED or DISABLED).
        :param pulumi.Input[Sequence[pulumi.Input[Union['BrokenLinksMonitorTagArgs', 'BrokenLinksMonitorTagArgsDict']]]] tags: The tags that will be associated with the monitor. See Nested tag blocks below for details
        :param pulumi.Input[str] uri: The URI the monitor runs against.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BrokenLinksMonitorState.__new__(_BrokenLinksMonitorState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["guid"] = guid
        __props__.__dict__["locations_privates"] = locations_privates
        __props__.__dict__["locations_publics"] = locations_publics
        __props__.__dict__["name"] = name
        __props__.__dict__["period"] = period
        __props__.__dict__["period_in_minutes"] = period_in_minutes
        __props__.__dict__["runtime_type"] = runtime_type
        __props__.__dict__["runtime_type_version"] = runtime_type_version
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["uri"] = uri
        __props__.__dict__["use_unsupported_legacy_runtime"] = use_unsupported_legacy_runtime
        return BrokenLinksMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[str]:
        """
        The account in which the Synthetics monitor will be created.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def guid(self) -> pulumi.Output[str]:
        """
        The unique entity identifier of the monitor in New Relic.
        """
        return pulumi.get(self, "guid")

    @property
    @pulumi.getter(name="locationsPrivates")
    def locations_privates(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The location the monitor will run from. Accepts a list of private location GUIDs. At least one of either `locations_public` or `locations_private` is required.
        """
        return pulumi.get(self, "locations_privates")

    @property
    @pulumi.getter(name="locationsPublics")
    def locations_publics(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The location the monitor will run from. Check out [this page](https://docs.newrelic.com/docs/synthetics/synthetic-monitoring/administration/synthetic-public-minion-ips/) for a list of valid public locations. You don't need the `AWS_` prefix as the provider uses NerdGraph. At least one of either `locations_public` or `location_private` is required.
        """
        return pulumi.get(self, "locations_publics")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name for the monitor.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def period(self) -> pulumi.Output[str]:
        """
        The interval at which this monitor should run. Valid values are `EVERY_MINUTE`, `EVERY_5_MINUTES`, `EVERY_10_MINUTES`, `EVERY_15_MINUTES`, `EVERY_30_MINUTES`, `EVERY_HOUR`, `EVERY_6_HOURS`, `EVERY_12_HOURS`, or `EVERY_DAY`.
        """
        return pulumi.get(self, "period")

    @property
    @pulumi.getter(name="periodInMinutes")
    def period_in_minutes(self) -> pulumi.Output[int]:
        """
        The interval in minutes at which Synthetic monitor should run.
        """
        return pulumi.get(self, "period_in_minutes")

    @property
    @pulumi.getter(name="runtimeType")
    def runtime_type(self) -> pulumi.Output[Optional[str]]:
        """
        The runtime that the monitor will use to run jobs.
        """
        return pulumi.get(self, "runtime_type")

    @property
    @pulumi.getter(name="runtimeTypeVersion")
    def runtime_type_version(self) -> pulumi.Output[Optional[str]]:
        """
        The specific semver version of the runtime type.
        """
        return pulumi.get(self, "runtime_type_version")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The monitor status (ENABLED or DISABLED).
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.BrokenLinksMonitorTag']]]:
        """
        The tags that will be associated with the monitor. See Nested tag blocks below for details
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        """
        The URI the monitor runs against.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="useUnsupportedLegacyRuntime")
    def use_unsupported_legacy_runtime(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "use_unsupported_legacy_runtime")

