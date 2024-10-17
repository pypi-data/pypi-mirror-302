from igx_api.l1 import openapi_client
from igx_api.l2.types.organization import OrganizationId
from igx_api.l2.types.user import UserId
from igx_api.l2.util.from_raw_model import FromRawModel


class WhoamiKey(FromRawModel[openapi_client.models.key.Key]):
    """Information about the API key."""

    label: str
    """A descriptive label assigned to the API key."""

    @classmethod
    def _build(cls, raw: openapi_client.models.key.Key) -> "WhoamiKey":
        return cls(label=raw.label)


class WhoamiOrganization(FromRawModel[openapi_client.models.organization.Organization]):
    """Information about the organization assigned to the API key."""

    id: OrganizationId
    """The unique identifier of the organization assigned to the API key."""

    @classmethod
    def _build(cls, raw: openapi_client.models.organization.Organization) -> "WhoamiOrganization":
        return cls(id=OrganizationId(int(raw.id)))


class WhoamiUser(FromRawModel[openapi_client.models.user.User]):
    """Information about the user assigned to the API key."""

    id: UserId
    """The unique identifier of the user assigned to the API key."""
    is_machine: bool
    """Indicates whether the user is a real user or a machine user without a login."""

    @classmethod
    def _build(cls, raw: openapi_client.models.user.User) -> "WhoamiUser":
        return cls(id=UserId(int(raw.id)), is_machine=raw.is_machine)


class Whoami(FromRawModel[openapi_client.models.whoami.Whoami]):
    """Information about the current user and organization assigned to the used API key."""

    key: WhoamiKey
    """Information about the API key."""
    organization: WhoamiOrganization
    """The organization assigned to this API key."""
    user: WhoamiUser
    """The user assigned to this API key."""

    @classmethod
    def _build(cls, raw: openapi_client.models.whoami.Whoami) -> "Whoami":
        return cls(
            key=WhoamiKey.from_raw(raw.key),
            organization=WhoamiOrganization.from_raw(raw.organization),
            user=WhoamiUser.from_raw(raw.user),
        )
