# This file is shared between the following (using symlinks):
# - egp-api-backend
# - egp-py (SDK, CLI)
# - model code (dockerized models under packages/egp-api-backend/model_images)
# This generally applies to files under packages/egp-api-backend/egp_api_backend/server/utils/model_schemas
# we do this because they're mostly pydantic models describing the contract between
# SDK / CLI <------ API backend ------> Launch models running in docker containers
# Since these files are using in so many places, you have to be careful what you import:
# - Use relative imports for other files in this directory, since you can't assume to know the full model name.
# - If importing backend / sdk specific classes, wrap the import in a try: ... except ImportError and defined a fallback
#   implementation to use for the imported symbol in other contexts.
from enum import Enum
from typing import Any, Dict, Literal, Optional, Union

import pydantic

from .model_enums import ModelVendor

PYDANTIC_V2 = hasattr(pydantic, "VERSION") and pydantic.VERSION.startswith("2.")

if PYDANTIC_V2:
    from pydantic.v1 import Field
else:
    from pydantic import Field

try:
    from egp_api_backend.server.api.utils.model_utils import BaseModel, RootModel
except ImportError:
    if PYDANTIC_V2:
        from pydantic.v1 import BaseModel
    else:
        from pydantic import BaseModel

    RootModel = BaseModel


class LaunchFineTuningJobConfiguration(BaseModel):
    vendor: Literal[ModelVendor.LAUNCH] = Field(ModelVendor.LAUNCH)
    hyperparameters: Optional[Dict[str, Any]]
    wandb_config: Optional[Dict[str, Any]]
    suffix: Optional[str]
    output: Optional[str]


class LLMEngineFineTuningJobConfiguration(BaseModel):
    vendor: Literal[ModelVendor.LLMENGINE] = Field(ModelVendor.LLMENGINE)
    hyperparameters: Optional[Dict[str, Any]]
    wandb_config: Optional[Dict[str, Any]]
    suffix: Optional[str]
    output: Optional[str]


class OpenAIFineTuningJobConfiguration(BaseModel):
    vendor: Literal[ModelVendor.OPENAI] = Field(ModelVendor.OPENAI)
    hyperparameters: Optional[Dict[str, Any]]
    suffix: Optional[str]


class FineTuningJobVendorConfiguration(RootModel):
    __root__: Union[
        LaunchFineTuningJobConfiguration,
        LLMEngineFineTuningJobConfiguration,
        OpenAIFineTuningJobConfiguration,
    ] = Field(..., discriminator="vendor")


class FineTuningJobEvent(BaseModel):
    timestamp: Optional[float]
    message: str
    level: str


class FineTuningJobStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    CANCELED = "CANCELED"


class RerankingDatasetItem(BaseModel):
    question: str = Field(...)
    chunk: str = Field(...)
    # True if positive example, False otherwise
    positive: bool = Field(...)


class TrainingDatasetORMSchemaTypeEnum(str, Enum):
    GENERATION = "GENERATION"
    RERANKING_QUESTIONS = "RERANKING_QUESTIONS"
