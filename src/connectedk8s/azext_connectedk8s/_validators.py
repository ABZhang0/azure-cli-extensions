# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import azext_connectedk8s._constants as consts


from azure.cli.core.azclierror import ArgumentUsageError


def example_name_or_id_validator(cmd, namespace):
    # Example of a storage account name or ID validator.
    from azure.cli.core.commands.client_factory import get_subscription_id
    from azure.mgmt.core.tools import is_valid_resource_id, resource_id

    if namespace.storage_account:
        if not is_valid_resource_id(namespace.RESOURCE):
            namespace.storage_account = resource_id(
                subscription=get_subscription_id(cmd.cli_ctx),
                resource_group=namespace.resource_group_name,
                namespace="Microsoft.Storage",
                type="storageAccounts",
                name=namespace.storage_account,
            )


def validate_private_link_properties(namespace):
    if not namespace.enable_private_link and namespace.private_link_scope_resource_id:
        err_msg = (
            "Conflicting private link parameters received. The parameter '--private-link-scope-resource-id' "
            "should not be set if '--enable-private-link' is passed as null or False."
        )
        raise ArgumentUsageError(err_msg)
    if (
        namespace.enable_private_link is True
        and not namespace.private_link_scope_resource_id
    ):
        err_msg = (
            "The parameter '--private-link-scope-resource-id' was not provided. It is mandatory to pass this "
            "parameter for enabling private link on the connected cluster resource."
        )
        raise ArgumentUsageError(err_msg)


def override_client_request_id_header(cmd, namespace):
    if namespace.correlation_id is not None:
        cmd.cli_ctx.data["headers"][consts.Client_Request_Id_Header] = (
            namespace.correlation_id
        )
    else:
        cmd.cli_ctx.data["headers"][consts.Client_Request_Id_Header] = (
            consts.Default_Onboarding_Source_Tracking_Guid
        )


def validate_gateway_updates(namespace):
    if namespace.gateway_resource_id != "" and namespace.disable_gateway:
        raise ArgumentUsageError(
            "Cannot specify both --gateway-resource-id and --disable-gateway simultaneously."
        )


def validate_enable_oidc_issuer_updates(namespace):
    if namespace.enable_oidc_issuer is False:
        raise ArgumentUsageError("Disabling OIDC issuer is not supported.")


def validate_self_hosted_issuer(namespace):
    if namespace.self_hosted_issuer != "" and not namespace.enable_oidc_issuer:
        raise ArgumentUsageError(
            "Cannot specify a value for --self-hosted-issuer without --enable-oidc-issuer."
        )


def validate_workload_identity_updates(namespace):
    if (
        namespace.enable_workload_identity is True
        and namespace.disable_workload_identity is True
    ):
        raise ArgumentUsageError(
            "Cannot specify both --enable-workload-identity and --disable-workload-identity simultaneously."
        )
