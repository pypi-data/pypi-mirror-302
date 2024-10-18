from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Union, List, Literal, Dict, Any

import pydantic

PYDANTIC_V2 = hasattr(pydantic, "VERSION") and pydantic.VERSION.startswith("2.")

if PYDANTIC_V2:
    from pydantic.v1 import Field
else:
    from pydantic import Field


from scale_egp.sdk.enums import (
    UploadJobStatus,
    DataSource,
    DeduplicationStrategy,
    ChunkingStrategy,
    UploadScheduleStatus,
)
from scale_egp.sdk.types.knowledge_base_artifacts import KnowledgeBaseArtifact
from scale_egp.utils.model_utils import Entity, RootModel, BaseModel


class KnowledgeBaseUploadResponse(BaseModel):
    upload_id: str = Field(..., description="ID of the created knowledge base upload job.")


class CancelKnowledgeBaseUploadResponse(BaseModel):
    upload_id: str = Field(
        ..., description="ID of the knowledge base upload job that was cancelled."
    )
    canceled: bool = Field(..., description="Whether cancellation was successful.")


class ArtifactsStatus(BaseModel):
    """
    A data model representing the status of the artifacts in a knowledge base.

    Attributes:
        artifacts_completed: Number of artifacts uploaded successfully.
        artifacts_pending: Number of artifacts awaiting upload.
        artifacts_uploading: Number of artifacts with upload in progress.
        artifacts_failed: Number of artifacts that failed upload.
    """

    artifacts_completed: int
    artifacts_pending: int
    artifacts_uploading: int
    artifacts_failed: int


class S3DataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a S3 data source.

    Attributes:
        source: The data source type. Must be 's3'.
        s3_bucket: The name of the S3 bucket where the data is stored
        s3_prefix: The prefix of the S3 bucket where the data is stored
        aws_region: The AWS region where the S3 bucket is located
        aws_account_id: The AWS account ID that owns the S3 bucket
    """

    source: Literal[DataSource.S3] = DataSource.S3.value
    s3_bucket: str
    aws_region: str
    aws_account_id: str
    s3_prefix: Optional[str] = None


class SharePointDataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a SharePoint data source.

    Attributes:
        source: The data source type. Must be 'sharepoint'.
        client_id: The client ID associated with this SharePoint site
        tenant_id: The tenant ID that the SharePoint site is within
        site_id: The site ID for this SharePoint site
        folder_path: The nested folder path to read files from the root of the site
        recursive: Whether to recurse through the folder contents
    """

    source: Literal[DataSource.SHAREPOINT] = DataSource.SHAREPOINT.value
    client_id: str
    tenant_id: str
    site_id: str
    folder_path: Optional[str] = ""
    recursive: Optional[bool] = True


class GoogleDriveDataSourceConfig(BaseModel):
    """
    A data model representing the configuration of a Google Drive data source.

    Attributes:
        source: The data source type. Must be 'google_drive'.
        drive_id: The ID of the Google Drive to retrieve contents from
    """

    source: Literal[DataSource.GOOGLE_DRIVE] = DataSource.GOOGLE_DRIVE.value
    drive_id: str


class LocalChunksSourceConfig(BaseModel):
    """
    A data model representing the configuration of a local chunks data source.

    Attributes:
        source: The data source type. Must be 'local_chunks'.
        artifact_name: The file name assigned to the artifact, containing a file extension.
            Adding an extension is mandatory, to allow detecting file types for text extraction.
        artifact_uri: A unique identifier for an artifact within the knowledge base, such as full
            path in a directory or file system.
        deduplication_strategy: Action to take if an artifact with the same name already exists
            in the knowledge base. Can be either Overwrite (default) or Fail.
    """

    source: Literal[DataSource.LOCAL_CHUNKS] = DataSource.LOCAL_CHUNKS.value
    artifact_name: str
    artifact_uri: str
    deduplication_strategy: Optional[DeduplicationStrategy] = DeduplicationStrategy.OVERWRITE


class GoogleDriveDataSourceAuthConfig(BaseModel):
    """
    A data model representing the configuration of a Google Drive service account.

    Attributes:
        source: The data source type. Must be 'GoogleDrive'.
        client_email: The service account's client email
        private_key: The service account's private_key
        token_uri: The service account's token_uri
        client_id: The service account's client_id
    """

    source: Literal[DataSource.GOOGLE_DRIVE] = DataSource.GOOGLE_DRIVE.value
    client_email: str
    private_key: str
    token_uri: str
    client_id: str


class SharePointDataSourceAuthConfig(BaseModel):
    """
    A data model representing the configuration of a SharePoint data source.

    Attributes:
        source: The data source type. Must be 'sharepoint'.
        client_secret: The secret for the app registration associated with this SharePoint site
    """

    source: Literal[DataSource.SHAREPOINT] = DataSource.SHAREPOINT.value
    client_secret: str


class S3DataSourceAuthConfig(BaseModel):
    """
    A data model representing the configuration of a S3 data source.

    Attributes:
        source: The data source type. Must be 'S3'.
        s3_role: Name of the role that a client will be initialized via AssumeRole of AWS sts
        external_id: External ID defined by the customer for the IAM role
    """

    source: Literal[DataSource.S3] = DataSource.S3.value
    s3_role: Optional[str]
    external_id: Optional[str]

    class Config(BaseModel.Config):
        title = "S3 DataSource Auth Config"


class AzureBlobStorageDataSourceConfig(BaseModel):
    """
    A data model representing the configuration of an Azure Blob Storage data source.

    Attributes:
        source: The data source type. Must be 'azure_blob_storage'.
        container_url: The SAS URL for the Azure Blob Storage container (a.k.a. Blob SAS URL)
    """

    source: Literal[DataSource.AZURE_BLOB_STORAGE] = DataSource.AZURE_BLOB_STORAGE.value
    container_url: str


class AzureBlobStorageDataSourceAuthConfig(BaseModel):
    """
    A data model representing the configuration of an Azure Blob Storage data source.

    Attributes:
        source: The data source type. Must be 'azure_blob_storage'.
        blob_sas_token: The SAS token for the Azure Blob Storage container
    """

    source: Literal[DataSource.AZURE_BLOB_STORAGE] = DataSource.AZURE_BLOB_STORAGE.value
    blob_sas_token: str


class DataSourceAuthConfig(RootModel):
    __root__: Union[
        GoogleDriveDataSourceAuthConfig,
        SharePointDataSourceAuthConfig,
        S3DataSourceAuthConfig,
        AzureBlobStorageDataSourceAuthConfig,
    ] = Field(..., discriminator="source")


class CharacterChunkingStrategyConfig(BaseModel):
    """
    A data model representing the configuration of a character chunking strategy.

    Attributes:
        strategy: The chunking strategy type. Must be 'character'.
        separator: Character designating breaks in input data. Text data will first be split
            into sections by this separator, then each section will be split into chunks
            of size `chunk_size`.
        chunk_size: Maximum number of characters in each chunk. If not specified, a chunk size
            of 1000 will be used.
        chunk_overlap: Number of characters to overlap between chunks. If not specified, an overlap
            of 200 will be used. For example if the chunk size is 3 and the overlap size
            is 1, and the text to chunk is 'abcde', the chunks will be 'abc', 'cde'.
    """

    strategy: Literal[ChunkingStrategy.CHARACTER] = ChunkingStrategy.CHARACTER.value
    separator: Optional[str] = "\n\n"
    chunk_size: Optional[int] = 1000
    chunk_overlap: Optional[int] = 200


class TokenChunkingStrategyConfig(BaseModel):
    """
    A data model representing the configuration of a token chunking strategy.

    Attributes:
        strategy: The chunking strategy type. Must be 'token'.
        separator: Character designating breaks in input data. Text data will first be split
            into sections by this separator, then each section will be split into chunks
            of size `chunk_size`.
        target_chunk_size: Target number of tokens in each chunk. If not specified, a target chunk
            size of 200 will be used.
        max_chunk_size: Maximum number of tokens in each chunk. If not specified, a maximum chunk
            size of 200 will be used.
        chunk_overlap: Number of tokens to overlap between chunks. If not specified, an overlap
            of 0 will be used. Note this is only followed approximately.
    """

    strategy: Literal[ChunkingStrategy.TOKEN] = ChunkingStrategy.TOKEN.value
    separator: Optional[str] = "\n\n"
    target_chunk_size: Optional[int] = 200
    max_chunk_size: Optional[int] = 600
    chunk_overlap: Optional[int] = 0


class ChunkToUpload(BaseModel):
    """
    A data model representing a local chunk.

    Attributes:
        text: The text associated with the chunk
        chunk_position: The position of the chunk in the artifact
        metadata: Any additional key value pairs of information stored with the chunk
    """

    text: str
    chunk_position: int
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DataSourceConfig(RootModel):
    """
    A type alias for a Union of all data source types.

    Attributes:
        __root__: Instead of directly using this class, please use the appropriate data source type
            for your use case.
    """

    __root__: Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        GoogleDriveDataSourceConfig,
        AzureBlobStorageDataSourceConfig,
        LocalChunksSourceConfig,
    ] = Field(
        ...,
        discriminator="source",
    )


class RemoteDataSourceConfig(RootModel):
    """
    A type alias for a Union of all remote data source types.

    Attributes:
        __root__: Instead of directly using this class, please use the appropriate data source type
            for your use case.
    """

    __root__: Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        GoogleDriveDataSourceConfig,
        AzureBlobStorageDataSourceConfig,
    ] = Field(
        ...,
        discriminator="source",
    )


class ChunkingStrategyConfig(RootModel):
    """
    A type alias for a Union of all chunking strategy types.

    Attributes:
        __root__: Instead of directly using this class, please use the appropriate chunking strategy
            type for your use case.
    """

    __root__: Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
    ] = Field(
        ...,
        discriminator="strategy",
    )


class KnowledgeBaseUpload(Entity):
    """
    A data model representing a knowledge base upload.

    Attributes:
        upload_id: Unique ID of the upload job
        data_source_config: Configuration for downloading data from source
        chunking_strategy_config: Configuration for chunking the text content of each artifact
        created_at: The timestamp at which the upload job started
        updated_at: The timestamp at which the upload job was last updated
        status: Sync status
        status_reason: Reason for the upload job's status
        artifacts_status: Number of artifacts pending, completed, and failed
        artifacts: List of info for each artifacts
    """

    upload_id: str
    data_source_config: DataSourceConfig
    chunking_strategy_config: Optional[ChunkingStrategyConfig]
    created_at: str
    updated_at: str
    status: UploadJobStatus
    status_reason: Optional[str] = None
    artifacts_status: Optional[ArtifactsStatus]
    artifacts: Optional[List[KnowledgeBaseArtifact]]


class KnowledgeBaseRemoteUploadRequest(BaseModel):
    upload_type: Literal["remote"] = "remote"
    data_source_config: RemoteDataSourceConfig
    data_source_auth_config: Optional[DataSourceAuthConfig] = Field(
        None,
        description="Configuration for the data source which describes how to "
        "authenticate to the data source.",
    )
    chunking_strategy_config: ChunkingStrategyConfig = Field(
        None,
        description="Configuration for the chunking strategy which describes how to chunk the "
        "data.",
    )


class KnowledgeBaseDataSourceUploadRequest(BaseModel):
    upload_type: Literal["data_source"] = "data_source"
    data_source_id: str = Field(description="The ID of the data source to upload from.")
    chunking_strategy_config: ChunkingStrategyConfig = Field(
        None,
        description="Configuration for the chunking strategy which describes how to chunk the "
        "data.",
    )


class ListKnowledgeBaseUploadsResponse(BaseModel):
    uploads: List[KnowledgeBaseUpload] = Field(..., description="List of knowledge base uploads.")


class KnowledgeBaseLocalChunkUploadRequest(BaseModel):
    upload_type: Literal["local_chunks"] = "local_chunks"
    data_source_config: LocalChunksSourceConfig = Field(
        ...,
        description="Configuration for the data source which describes where to find the data.",
    )
    chunks: List[ChunkToUpload] = Field(..., description="List of chunks.")


class KnowledgeBaseUploadRequest(RootModel):
    __root__: Union[
        KnowledgeBaseRemoteUploadRequest,
        KnowledgeBaseLocalChunkUploadRequest,
        KnowledgeBaseDataSourceUploadRequest,
    ] = Field(
        ...,
        discriminator="upload_type",
    )


class KnowledgeBaseDataSourceRequest(BaseModel):
    name: str = Field(..., description="A unique name for the data source.")
    description: Optional[str] = Field(None, description="A description of the data source.")
    data_source_config: RemoteDataSourceConfig
    data_source_auth_config: Optional[DataSourceAuthConfig] = Field(
        None,
        description="Configuration for the data source which describes how to "
        "authenticate to the data source.",
    )
    account_id: str = Field(..., description="The ID of the account that owns the data source.")


class KnowledgeBaseDataSource(Entity):
    id: str
    name: str
    description: Optional[str]
    data_source_config: RemoteDataSourceConfig
    created_at: datetime
    updated_at: datetime
    created_by_user_id: str
    account_id: str


class KnowledgeBaseUploadScheduleRequest(BaseModel):
    knowledge_base_data_source_id: str = Field(
        ..., description="The ID of the knowledge base data source to upload from."
    )
    chunking_strategy_config: ChunkingStrategyConfig = Field(
        None,
        description="Configuration for the chunking strategy which describes how to chunk the "
        "data.",
    )
    interval: float = Field(
        ..., description="The interval at which to run uploads from the data source."
    )
    next_run_at: Optional[str] = Field(
        None, description="The time at which the next upload will run."
    )
    account_id: str = Field(..., description="The ID of the account that owns the upload schedule.")


class KnowledgeBaseUploadSchedulePauseRequest(BaseModel):
    next_run_at: None = None


class KnowledgeBaseUploadSchedule(Entity):
    id: str
    knowledge_base_id: str
    knowledge_base_data_source_id: str
    chunking_strategy_config: ChunkingStrategyConfig
    status: UploadScheduleStatus
    status_reason: Optional[str]
    interval: timedelta
    next_run_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    created_by_user_id: str
    account_id: str
