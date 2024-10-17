from typing import Annotated, Any

from pydantic import AnyUrl, BaseModel, Field, UrlConstraints


class ReplicaConfig(BaseModel):
    """Mongodb replica config model."""

    uri: Annotated[
        AnyUrl,
        UrlConstraints(allowed_schemes=["mongodb", "mongodb+srv"]),
        Field(..., description="Mongodb connection URI."),
    ]
    client_options: dict[str, Any] = Field(
        default_factory=dict,
        description="Mongodb client options.",
    )
