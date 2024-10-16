"""Segmentation configuration."""

from typing import TYPE_CHECKING, Any

from validio_sdk.resource._resource import Resource
from validio_sdk.resource._serde import (
    _api_create_input_params,
    _encode_resource,
    get_config_node,
)
from validio_sdk.resource.sources import Source

if TYPE_CHECKING:
    from validio_sdk.resource._diff import DiffContext


class Segmentation(Resource):
    """A segmentation resource.

    https://docs.validio.io/docs/segmentation
    """

    def __init__(
        self,
        name: str,
        source: Source,
        fields: list[str] | None = None,
        ignore_changes: bool = False,
    ):
        """
        Constructor.

        :param name: Unique resource name assigned to the segmentation.
        :param source: The source to attach the segmentation to. (immutable)
        :param fields: Fields to segment on. (immutable)
        :param ignore_changes: If set to true, changes to the resource will be ignored
        """
        super().__init__(
            name=name,
            # TODO: Expose and set this when surface adds support
            #  https://linear.app/validio/issue/UI-3882
            display_name=None,
            ignore_changes=ignore_changes,
            __internal__=source._resource_graph,
        )
        self.source_name: str = source.name
        self.fields: list[str] = fields if fields else []

        source.add(self.name, self)

    def _immutable_fields(self) -> set[str]:
        return {"source_name", "fields"}

    def _mutable_fields(self) -> set[str]:
        # TODO: Remove this when surface adds support
        #  https://linear.app/validio/issue/UI-3882
        return {v for v in super()._mutable_fields() if v != "display_name"}

    def resource_class_name(self) -> str:
        """Returns the class name."""
        return "Segmentation"

    def _encode(self) -> dict[str, object]:
        # Drop fields here that are not part of the constructor for when
        # we deserialize back. They will be reinitialized by the constructor.
        return _encode_resource(self, skip_fields={"source_name"})

    @staticmethod
    def _decode(obj: dict[str, Any], source: Source) -> "Segmentation":
        args = get_config_node(obj)
        # TODO: Remove this when surface adds support
        #  https://linear.app/validio/issue/UI-3882
        del args["display_name"]

        return Segmentation(**{**args, "source": source})  # type:ignore

    def _api_create_input(self, namespace: str, ctx: "DiffContext") -> Any:
        return _api_create_input_params(
            self,
            namespace=namespace,
            overrides={"source_id": ctx.sources[self.source_name]._must_id()},
        )
