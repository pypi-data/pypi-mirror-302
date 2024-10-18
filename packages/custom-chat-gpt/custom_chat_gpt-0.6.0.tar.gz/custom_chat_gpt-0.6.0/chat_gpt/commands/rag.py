import os
import weaviate
import weaviate.classes
from chat_gpt.config import Config


def get_weaviate_client(settings: Config) -> weaviate.WeaviateClient:
    return weaviate.connect_to_custom(
        http_host=settings.WEAVIATE_HOST,
        http_port=settings.WEAVIATE_PORT,
        http_secure=False,
        grpc_host=settings.WEAVIATE_GRPC_HOST,
        grpc_port=settings.WEAVIATE_GRPC_PORT,
        grpc_secure=False,
        headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
    )
