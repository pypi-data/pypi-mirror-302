from pydantic import BaseModel

from kubiya_sdk.tools.models import Tool


class BundleModel(BaseModel):
    tools: list[Tool]
    errors: list[str]
    python_bundle_version: str
