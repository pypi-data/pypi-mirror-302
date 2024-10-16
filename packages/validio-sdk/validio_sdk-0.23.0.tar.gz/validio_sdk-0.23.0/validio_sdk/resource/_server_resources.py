from typing import cast

# We need to import the validio_sdk module due to the `eval`
# ruff: noqa: F401
import validio_sdk
from validio_sdk.exception import ValidioError, ValidioGraphQLError
from validio_sdk.graphql_client.exceptions import GraphQLClientHttpError
from validio_sdk.graphql_client.fragments import ReferenceSourceConfigDetails
from validio_sdk.graphql_client.input_types import ResourceFilter
from validio_sdk.graphql_client.list_credentials import (
    ListCredentialsCredentialsListAwsAthenaCredential,
    ListCredentialsCredentialsListAwsCredential,
    ListCredentialsCredentialsListAwsRedshiftCredential,
    ListCredentialsCredentialsListAzureSynapseEntraIdCredential,
    ListCredentialsCredentialsListAzureSynapseSqlCredential,
    ListCredentialsCredentialsListClickHouseCredential,
    ListCredentialsCredentialsListDatabricksCredential,
    ListCredentialsCredentialsListDbtCloudCredential,
    ListCredentialsCredentialsListDbtCoreCredential,
    ListCredentialsCredentialsListKafkaSaslSslPlainCredential,
    ListCredentialsCredentialsListKafkaSslCredential,
    ListCredentialsCredentialsListLookerCredential,
    ListCredentialsCredentialsListMsPowerBiCredential,
    ListCredentialsCredentialsListPostgreSqlCredential,
    ListCredentialsCredentialsListSnowflakeCredential,
    ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair,
    ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword,
    ListCredentialsCredentialsListTableauConnectedAppCredential,
    ListCredentialsCredentialsListTableauPersonalAccessTokenCredential,
)
from validio_sdk.resource._diff import (
    DiffContext,
    GraphDiff,
    ResourceUpdates,
    expand_validator_field_selectors,
    infer_schema_for_source,
)
from validio_sdk.resource._diff_util import (
    must_find_channel,
    must_find_credential,
    must_find_segmentation,
    must_find_source,
    must_find_window,
)
from validio_sdk.resource._resource import Resource, ResourceGraph
from validio_sdk.resource._util import _sanitize_error
from validio_sdk.resource.credentials import (
    AwsAthenaCredential,
    AwsCredential,
    AwsRedshiftCredential,
    AzureSynapseEntraIdCredential,
    AzureSynapseSqlCredential,
    ClickHouseCredential,
    Credential,
    DatabricksCredential,
    DbtCloudCredential,
    DbtCoreCredential,
    DemoCredential,
    GcpCredential,
    KafkaSaslSslPlainCredential,
    KafkaSslCredential,
    LookerCredential,
    MsPowerBiCredential,
    MsPowerBiCredentialAuth,
    MsPowerBiCredentialEntraId,
    PostgreSqlCredential,
    SnowflakeCredential,
    SnowflakeCredentialAuth,
    SnowflakeCredentialKeyPair,
    SnowflakeCredentialUserPassword,
    TableauConnectedAppCredential,
    TableauPersonalAccessTokenCredential,
)
from validio_sdk.resource.notification_rules import Conditions
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.thresholds import THRESHOLD_CLASSES, Threshold
from validio_sdk.resource.validators import (
    VALIDATOR_CLASSES,
    Reference,
    VolumeValidator,
)
from validio_sdk.resource.windows import WINDOW_CLASSES
from validio_sdk.scalars import CredentialId
from validio_sdk.validio_client import ValidioAPIClient

# Some credentials depend on other credentials, i.e. wrapping credentials. This
# list contains all of those and can be used when sorting to ensure they always
# end up where you want them.
CREDENTIALS_WITH_DEPENDENCIES = {"DbtCoreCredential", "DbtCloudCredential"}


async def load_resources(namespace: str, client: ValidioAPIClient) -> DiffContext:
    g = ResourceGraph()
    ctx = DiffContext()

    # Ordering matters here - we need to load parent resources before children
    await load_credentials(namespace, client, g, ctx)
    await load_channels(namespace, client, g, ctx)
    await load_sources(namespace, client, ctx)
    await load_segmentations(namespace, client, ctx)
    await load_windows(namespace, client, ctx)
    await load_validators(namespace, client, ctx)
    await load_notification_rules(namespace, client, ctx)

    return ctx


# ruff: noqa: PLR0915
async def load_credentials(
    # ruff: noqa: ARG001
    namespace: str,
    client: ValidioAPIClient,
    g: ResourceGraph,
    ctx: DiffContext,
) -> None:
    credentials = await client.list_credentials(
        filter=ResourceFilter(namespace_id=namespace)
    )

    # Ensure we sort the credentials so the ones that depend on other
    # credentials (wrapping credentials) always comes last.
    credentials.sort(key=lambda c: c.typename__ in CREDENTIALS_WITH_DEPENDENCIES)

    for c in credentials:
        name = c.resource_name
        display_name = c.name

        # The 'secret' parts of a credential are left unset since they are not
        # provided by the API. We check for changes to them specially.
        match c.typename__:
            case "DemoCredential":
                credential: Credential = DemoCredential(
                    name=name,
                    display_name=display_name,
                    __internal__=g,
                )
            case "DbtCoreCredential":
                c = cast(ListCredentialsCredentialsListDbtCoreCredential, c)
                credential = DbtCoreCredential(
                    name=name,
                    warehouse_credential=must_find_credential(
                        ctx,
                        c.config.warehouse_credential.resource_name,
                    ),
                    display_name=display_name,
                    __internal__=g,
                )
            case "DbtCloudCredential":
                c = cast(ListCredentialsCredentialsListDbtCloudCredential, c)
                credential = DbtCloudCredential(
                    name=name,
                    account_id=c.config.account_id,
                    api_base_url=c.config.api_base_url,
                    token="UNSET",
                    warehouse_credential=must_find_credential(
                        ctx,
                        c.config.warehouse_credential.resource_name,
                    ),
                    display_name=display_name,
                    __internal__=g,
                )
            case "GcpCredential":
                credential = GcpCredential(
                    name=name,
                    credential="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsCredential":
                c = cast(ListCredentialsCredentialsListAwsCredential, c)
                credential = AwsCredential(
                    name=name,
                    access_key=c.config.access_key,
                    secret_key="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "PostgreSqlCredential":
                c = cast(ListCredentialsCredentialsListPostgreSqlCredential, c)
                credential = PostgreSqlCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    user=c.config.user,
                    password="UNSET",
                    default_database=c.config.default_database,
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsRedshiftCredential":
                c = cast(ListCredentialsCredentialsListAwsRedshiftCredential, c)
                credential = AwsRedshiftCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    user=c.config.user,
                    password="UNSET",
                    default_database=c.config.default_database,
                    display_name=display_name,
                    __internal__=g,
                )
            case "AwsAthenaCredential":
                c = cast(ListCredentialsCredentialsListAwsAthenaCredential, c)
                credential = AwsAthenaCredential(
                    name=name,
                    access_key=c.config.access_key,
                    secret_key="UNSET",
                    region=c.config.region,
                    query_result_location=c.config.query_result_location,
                    display_name=display_name,
                    __internal__=g,
                )
            case "AzureSynapseEntraIdCredential":
                c = cast(ListCredentialsCredentialsListAzureSynapseEntraIdCredential, c)
                credential = AzureSynapseEntraIdCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    backend_type=c.config.backend_type,
                    client_id=c.config.client_id,
                    client_secret="UNSET",
                    database=c.config.database,
                    display_name=display_name,
                    __internal__=g,
                )
            case "AzureSynapseSqlCredential":
                c = cast(ListCredentialsCredentialsListAzureSynapseSqlCredential, c)
                credential = AzureSynapseSqlCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    backend_type=c.config.backend_type,
                    username=c.config.username,
                    password="UNSET",
                    database=c.config.database,
                    display_name=display_name,
                    __internal__=g,
                )
            case "ClickHouseCredential":
                c = cast(ListCredentialsCredentialsListClickHouseCredential, c)
                credential = ClickHouseCredential(
                    name=name,
                    protocol=c.config.protocol,
                    host=c.config.host,
                    port=int(c.config.port),
                    username=c.config.username,
                    password="UNSET",
                    default_database=c.config.default_database,
                    display_name=display_name,
                    __internal__=g,
                )
            case "DatabricksCredential":
                c = cast(ListCredentialsCredentialsListDatabricksCredential, c)
                credential = DatabricksCredential(
                    name=name,
                    host=c.config.host,
                    port=c.config.port,
                    access_token="UNSET",
                    http_path=c.config.http_path,
                    display_name=display_name,
                    __internal__=g,
                )
            case "SnowflakeCredential":
                c = cast(ListCredentialsCredentialsListSnowflakeCredential, c)

                auth: SnowflakeCredentialAuth | None = None
                if isinstance(
                    c.config.auth,
                    ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword,
                ):
                    auth = SnowflakeCredentialUserPassword(
                        user=c.config.auth.user,
                        password="UNSET",
                    )
                elif isinstance(
                    c.config.auth,
                    ListCredentialsCredentialsListSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair,
                ):
                    auth = SnowflakeCredentialKeyPair(
                        user=c.config.auth.user,
                        private_key="UNSET",
                        private_key_passphrase="UNSET",
                    )

                # If we get the auth object back then we set the deprecated
                # fields to None to avoid getting a diff on something that
                # is not used.
                user = c.config.user if not auth else None
                password = "UNSET" if not auth else None

                credential = SnowflakeCredential(
                    name=name,
                    account=c.config.account,
                    user=user,
                    password=password,
                    auth=auth,
                    warehouse=c.config.warehouse,
                    role=c.config.role,
                    display_name=display_name,
                    __internal__=g,
                )
            case "KafkaSslCredential":
                c = cast(ListCredentialsCredentialsListKafkaSslCredential, c)
                credential = KafkaSslCredential(
                    name=name,
                    bootstrap_servers=c.config.bootstrap_servers,
                    ca_certificate=c.config.ca_certificate,
                    client_certificate="UNSET",
                    client_private_key="UNSET",
                    client_private_key_password="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "KafkaSaslSslPlainCredential":
                c = cast(ListCredentialsCredentialsListKafkaSaslSslPlainCredential, c)
                credential = KafkaSaslSslPlainCredential(
                    name=name,
                    bootstrap_servers=c.config.bootstrap_servers,
                    username="UNSET",
                    password="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "LookerCredential":
                c = cast(ListCredentialsCredentialsListLookerCredential, c)
                credential = LookerCredential(
                    name=name,
                    base_url=c.config.base_url,
                    client_id=c.config.client_id,
                    client_secret="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "MsPowerBiCredential":
                c = cast(ListCredentialsCredentialsListMsPowerBiCredential, c)
                entra_id_auth = MsPowerBiCredentialEntraId(
                    client_id=c.config.auth.client_id,
                    client_secret="UNSET",
                    tenant_id=c.config.auth.tenant_id,
                )
                credential = MsPowerBiCredential(
                    name=name,
                    auth=entra_id_auth,
                    display_name=display_name,
                    __internal__=g,
                )
            case "TableauConnectedAppCredential":
                c = cast(ListCredentialsCredentialsListTableauConnectedAppCredential, c)
                credential = TableauConnectedAppCredential(
                    name=name,
                    host=c.config.host,
                    site=c.config.site,
                    user=c.config.user,
                    client_id=c.config.client_id,
                    secret_id=c.config.secret_id,
                    secret_value="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case "TableauPersonalAccessTokenCredential":
                c = cast(
                    ListCredentialsCredentialsListTableauPersonalAccessTokenCredential,
                    c,
                )
                credential = TableauPersonalAccessTokenCredential(
                    name=name,
                    host=c.config.host,
                    site=c.config.site,
                    token_name=c.config.token_name,
                    token_value="UNSET",
                    display_name=display_name,
                    __internal__=g,
                )
            case _:
                raise ValidioError(
                    f"unsupported credential '{name}' of type '{type(c)}'"
                )

        credential._id.value = c.id
        credential._namespace = c.namespace_id

        ctx.credentials[name] = credential


async def load_channels(
    namespace: str,
    client: ValidioAPIClient,
    g: ResourceGraph,
    ctx: DiffContext,
) -> None:
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import channels

    server_channels = await client.list_channels()

    for ch in server_channels:
        if ch.namespace_id != namespace:
            continue

        name = ch.resource_name

        cls = eval(f"validio_sdk.resource.channels.{ch.typename__}")
        channel = cls(
            **{
                **ch.config.__dict__,  # type: ignore
                "name": name,
                "display_name": ch.name,
                "__internal__": g,
            }
        )
        channel._id.value = ch.id
        channel._namespace = ch.namespace_id
        ctx.channels[name] = channel


async def load_notification_rules(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
) -> None:
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import notification_rules

    rules = await client.list_notification_rules()

    for r in rules:
        if r.namespace_id != namespace:
            continue

        name = r.resource_name

        cls = eval(f"validio_sdk.resource.notification_rules.{r.typename__}")

        rule = cls(
            name=name,
            channel=must_find_channel(ctx, r.channel.resource_name),
            conditions=Conditions._new_from_api(ctx, r.conditions),
            display_name=r.name,
        )
        rule._id.value = r.id
        rule._namespace = r.namespace_id
        ctx.notification_rules[name] = rule


async def load_sources(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
) -> None:
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import sources

    server_sources = await client.list_sources(
        filter=ResourceFilter(namespace_id=namespace)
    )

    for s in server_sources:
        name = s.resource_name

        cls = eval(f"validio_sdk.resource.sources.{s.typename__}")
        params = s.config.__dict__ if hasattr(s, "config") else {}
        source = cls(
            **{
                **params,
                "name": name,
                "display_name": s.name,
                "credential": must_find_credential(ctx, s.credential.resource_name),
                "jtd_schema": s.jtd_schema,
            }
        )
        source._id.value = s.id
        source._namespace = s.namespace_id
        ctx.sources[name] = source


async def load_segmentations(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
) -> None:
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import segmentations

    server_segmentations = await client.list_segmentations(
        filter=ResourceFilter(namespace_id=namespace)
    )

    for s in server_segmentations:
        name = s.resource_name

        # TODO: Pass display name when surface adds support
        #  https://linear.app/validio/issue/UI-3882
        segmentation = Segmentation(
            name=name,
            source=must_find_source(ctx, s.source.resource_name),
            fields=s.fields,
        )

        segmentation._id.value = s.id
        segmentation._namespace = s.namespace_id
        ctx.segmentations[name] = segmentation


async def load_windows(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
) -> None:
    # We need to import the module due to the `eval`
    # ruff: noqa: F401
    from validio_sdk.resource import windows

    server_windows = await client.list_windows(
        filter=ResourceFilter(namespace_id=namespace)
    )

    for w in server_windows:
        name = w.resource_name

        cls = None
        for c in WINDOW_CLASSES:
            if w.typename__ == c.__name__:
                cls = c
                break

        if cls is None:
            raise ValidioError(
                f"missing implementation for Window type {w.__class__.__name__}"
            )

        data_time_field = (
            {"data_time_field": getattr(w, "data_time_field")}
            if hasattr(w, "data_time_field")
            else {}
        )

        window = cls(
            # TODO: Pass display name when surface adds support
            #  https://linear.app/validio/issue/UI-3882
            **{
                **(w.config.__dict__ if hasattr(w, "config") else {}),  # type:ignore
                "name": name,
                "source": must_find_source(ctx, w.source.resource_name),
                **data_time_field,
            }
        )

        window._id.value = w.id
        window._namespace = w.namespace_id
        ctx.windows[name] = window


# Takes in a graphql Threshold type
def convert_threshold(t: object) -> Threshold:
    graphql_class_name: str = t.__class__.__name__
    cls = None
    for c in THRESHOLD_CLASSES:
        if graphql_class_name.endswith(c.__name__):
            cls = c
            break

    if cls is None:
        raise ValidioError(
            f"missing implementation for threshold type {graphql_class_name}"
        )

    # Threshold parameters map 1-1 with resources, so
    # we call the constructor directly.
    return cls(**{k: v for k, v in t.__dict__.items() if k != "typename__"})


# Takes in a graphql ReferenceSourceConfig type
def convert_reference(ctx: DiffContext, r: ReferenceSourceConfigDetails) -> Reference:
    source = must_find_source(ctx, r.source.resource_name)
    window = must_find_window(ctx, r.window.resource_name)

    return Reference(
        source=source,
        window=window,
        history=r.history,
        offset=r.offset,
        filter=r.filter,
    )


async def load_validators(
    namespace: str,
    client: ValidioAPIClient,
    ctx: DiffContext,
) -> None:
    for source in ctx.sources.values():
        validators = await client.list_validators(
            id=source._must_id(), filter=ResourceFilter(namespace_id=namespace)
        )

        for v in validators:
            name = v.resource_name
            display_name = v.name

            cls = None
            for c in VALIDATOR_CLASSES:
                if v.typename__ == c.__name__:
                    cls = c
                    break

            if cls is None:
                raise ValidioError(
                    f"missing implementation for Validator type {v.typename__}"
                )

            window = must_find_window(ctx, v.source_config.window.resource_name)
            segmentation = must_find_segmentation(
                ctx, v.source_config.segmentation.resource_name
            )

            threshold = convert_threshold(v.config.threshold)  # type:ignore
            maybe_reference = (
                {
                    "reference": convert_reference(
                        ctx,
                        v.reference_source_config,  # type: ignore
                    )
                }
                if hasattr(v, "reference_source_config")
                else {}
            )
            maybe_filter = (
                {"filter": v.source_config.filter}
                if hasattr(v.source_config, "filter")
                and v.source_config.filter is not None
                else {}
            )

            config = {k: v for k, v in v.config.__dict__.items() if k != "threshold"}  # type: ignore

            if cls == VolumeValidator and "source_field" in config:
                config["optional_source_field"] = config["source_field"]
                del config["source_field"]

            validator = cls(
                **{
                    **config,
                    **maybe_reference,
                    **maybe_filter,
                    "threshold": threshold,
                    "name": name,
                    "window": window,
                    "segmentation": segmentation,
                    "display_name": display_name,
                }
            )
            validator._id.value = v.id
            validator._namespace = v.namespace_id
            ctx.validators[name] = validator


async def apply_updates_on_server(
    namespace: str,
    ctx: DiffContext,
    diff: GraphDiff,
    client: ValidioAPIClient,
    show_secrets: bool,
) -> None:
    try:
        await apply_deletes(namespace=namespace, deletes=diff.to_delete, client=client)

        # We perform create operations in two batches. First here creates top
        # level resources, then after performing updates, we create any remaining
        # resources. We do this due to a couple scenarios
        # - A resource potentially depends on the parent to be created first before
        #   it can be updated. Example is a notification rule that is being
        #   updated to reference a Source that is to be created. In such cases,
        #   we need to apply the create on parent resource before the update on
        #   child resource.
        # - Conversely, in some cases, a parent resource needs to be updated before
        #   the child resource can be created. e.g a validator that is referencing a
        #   new field in a schema needs the source to be updated first otherwise diver
        #   will reject the validator as invalid because the field does not yet exist.
        #
        # So, here we create the top level resources first - ensuring that any child
        # resource that relies on them are resolved properly.
        # We start with creating credentials only. Since sources need them to infer
        # schema.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=DiffContext(
                credentials=diff.to_create.credentials,
            ),
            client=client,
            show_secrets=show_secrets,
        )

        # Resolve any pending source schemas now that we have their credential.
        for source in diff.to_create.sources.values():
            if source.jtd_schema is None:
                await infer_schema_for_source(
                    manifest_ctx=ctx, source=source, client=client
                )

        # Create the remaining top level resources.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=DiffContext(
                sources=diff.to_create.sources,
                channels=diff.to_create.channels,
            ),
            client=client,
            show_secrets=show_secrets,
        )

        # Now we should have all source schemas available. We can expand
        # field selectors.
        expand_validator_field_selectors(ctx)

        # Then apply updates.
        await apply_updates(
            namespace=namespace, manifest_ctx=ctx, updates=diff.to_update, client=client
        )

        # Then apply remaining creates. Resources that have been created in
        # the previous steps are marked as _applied, so they will be skipped this
        # time around.
        await apply_creates(
            namespace=namespace,
            manifest_ctx=ctx,
            creates=diff.to_create,
            client=client,
            show_secrets=show_secrets,
        )
    except GraphQLClientHttpError as e:
        raise ValidioGraphQLError(e, "Error applying updates")


# ruff: noqa: PLR0912
async def apply_deletes(
    namespace: str, deletes: DiffContext, client: ValidioAPIClient
) -> None:
    # Delete notification rules first These reference sources so we
    # remove them before removing the sources they reference.
    for r in deletes.notification_rules.values():
        await _delete_resource(r, client)

    # For pipeline resources, start with sources (This cascades deletes,
    # so we don't have to individually delete child resources).
    for s in deletes.sources.values():
        await _delete_resource(s, client)

    # For child resources, we only need to delete them if their parent
    # haven't been deleted.
    for w in deletes.windows.values():
        if w.source_name not in deletes.sources:
            await _delete_resource(w, client)

    for sg in deletes.segmentations.values():
        if sg.source_name not in deletes.sources:
            await _delete_resource(sg, client)

    for v in deletes.validators.values():
        if v.source_name not in deletes.sources:
            await _delete_resource(v, client)

    # Finally delete credentials - these do not cascade so the api rejects any
    # delete requests if there are existing child resources attached to a credential.
    for c in deletes.credentials.values():
        await _delete_resource(c, client)

    for ch in deletes.channels.values():
        await _delete_resource(ch, client)


async def _delete_resource(resource: Resource, client: ValidioAPIClient) -> None:
    if resource._applied:
        return
    resource._applied = True
    await resource._api_delete(client)


async def apply_creates(
    namespace: str,
    manifest_ctx: DiffContext,
    creates: DiffContext,
    client: ValidioAPIClient,
    show_secrets: bool,
) -> None:
    # Creates must be applied top-down, parent first before child resources
    credentials = list(creates.credentials.values())

    # Ensure we sort the credentials so the ones that depend on other
    # credentials (wrapping credentials) always comes last.
    credentials.sort(key=lambda c: type(c) in CREDENTIALS_WITH_DEPENDENCIES)

    all_resources: list[list[Resource]] = [
        list(credentials),
        list(creates.sources.values()),
        list(creates.segmentations.values()),
        list(creates.windows.values()),
        list(creates.validators.values()),
        list(creates.channels.values()),
        list(creates.notification_rules.values()),
    ]
    for resources in all_resources:
        for r in resources:
            if r._applied:
                continue

            try:
                await r._api_create(namespace, client, manifest_ctx)
                r._applied = True
            except GraphQLClientHttpError as e:
                raise (
                    _sanitize_error(e, show_secrets) if isinstance(r, Credential) else e
                )


async def apply_updates(
    namespace: str,
    manifest_ctx: DiffContext,
    updates: ResourceUpdates,
    client: ValidioAPIClient,
) -> None:
    all_updates = [
        list(updates.credentials.values()),
        list(updates.sources.values()),
        list(updates.segmentations.values()),
        list(updates.windows.values()),
        list(updates.validators.values()),
        list(updates.channels.values()),
        list(updates.notification_rules.values()),
    ]

    for up in all_updates:
        for u in up:
            if u.manifest._applied:
                continue
            u.manifest._applied = True

            await u.manifest._api_update(namespace, client, manifest_ctx)
