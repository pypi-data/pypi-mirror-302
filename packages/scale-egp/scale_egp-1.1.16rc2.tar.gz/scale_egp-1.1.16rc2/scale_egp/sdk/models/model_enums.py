from enum import Enum


class ModelState(str, Enum):
    """
    An enum representing the different types of model states supported.

    Attributes:
        ENABLED: Denotes that the model is enabled.
        PENDING: Denotes that the model is pending.
        DISABLED: Denotes that the model is disabled.
    """

    ENABLED = "ENABLED"
    PENDING = "PENDING"
    DISABLED = "DISABLED"


class ModelVendor(str, Enum):
    """
    An enum representing the different types of model vendors supported.

    Attributes:
        OPENAI: Denotes that the model vendor is OpenAI.
        COHERE: Denotes that the model vendor is Cohere.
        GOOGLE: Denotes that the model vendor is Google.
        ANTHROPIC: Denotes that the model vendor is Anthropic.
        LLMENGINE: Denotes that the model vendor is LLM Engine.
        OTHER: Denotes that the model vendor is Other.
    """

    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GOOGLE = "GOOGLE"
    ANTHROPIC = "ANTHROPIC"
    LAUNCH = "LAUNCH"
    LLMENGINE = "LLMENGINE"
    BEDROCK = "BEDROCK"
    OTHER = "OTHER"

    @classmethod
    def from_str(cls, label: str):
        return cls[label.upper()]


class ModelEndpointType(str, Enum):
    """
    An enum representing the different types of model endpoint types supported.

    Attributes:
        SYNC: Denotes that the model endpoint type is sync.
        ASYNC: Denotes that the model endpoint type is async.
        STREAMING: Denotes that the model endpoint type is streaming.
        BATCH: Denotes that the model endpoint type is batch.
    """

    SYNC = "SYNC"
    ASYNC = "ASYNC"
    STREAMING = "STREAMING"
    BATCH = "BATCH"


class ModelType(str, Enum):
    """
    An enum representing the different types of models supported.

    Attributes:
        COMPLETION: Denotes that the model type is completion.
        CHAT_COMPLETION: Denotes that the model type is chat completion.
        AGENT: Denotes that the model type is agent.
        EMBEDDING: Denotes that the model type is embedding.
        RERANKING: Denotes that the model type is reranking.
        GENERIC: Denotes that the model type is generic.
    """

    COMPLETION = "COMPLETION"
    CHAT_COMPLETION = "CHAT_COMPLETION"
    AGENT = "AGENT"
    EMBEDDING = "EMBEDDING"
    RERANKING = "RERANKING"
    GENERIC = "GENERIC"
