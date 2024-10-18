from typing import Type
from collections import OrderedDict
from langchain.schema import Document
from langchain_community.document_loaders.pdf import BasePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from weaviate.client import WeaviateClient


class DocumentInfo(BaseModel):
    source: str
    filename: str
    metadata: dict


def format_documents(
    documents: list[Document], document_info: DocumentInfo
) -> list[dict]:
    """
    Documents are extracted via Langchain and contains document specific metadata (page, filename ...).
    Whereas DocumentInfo contains metadata that is common to all documents (company, entity_uid ...) that WE specify.
    Python starts indexing at 0, but we want to start at 1 for the page number.
    """

    formatted_documents = []

    for doc in documents:
        doc_metadata = {k: v for k, v in doc.metadata.items() if k != "source"}
        if "page" in doc_metadata:
            doc_metadata["page"] = int(doc_metadata["page"]) + 1

        formatted_documents.append(
            {
                "content": doc.page_content,
                "filename": document_info.filename,
                **document_info.metadata,
                **doc_metadata,
            }
        )
    return formatted_documents


class DataIngestor:
    """
    Class to ingest PDF documents into Weaviate.
    """

    def __init__(
        self,
        weaviate_client: WeaviateClient,
        text_splitter: RecursiveCharacterTextSplitter,
        document_loader: Type[BasePDFLoader],
    ):
        self.client: WeaviateClient = weaviate_client
        self.text_splitter: RecursiveCharacterTextSplitter = text_splitter
        self.document_loader: Type[BasePDFLoader] = document_loader

    def ingest_documents_with_references(
        self,
        parent_class_name: str,
        child_class_name: str,
        refererence_name: str,
        document_info: DocumentInfo,
    ):
        """Ingests a list of documents into Weaviate and creates a reference between the parent and child class."""

        """
        Using this method in a multi threading environment will likely generate warnings and errors in Weaviate due to gRPC
        which are likely not to be a problem but are annoying.
        """

        from weaviate.util import generate_uuid5

        print("Starting to ingest documents.")

        parent_collection = self.client.collections.get(parent_class_name)

        child_docs_len = 0
        child_docs_with_parent_uuid: OrderedDict[str, list[dict]] = OrderedDict()

        with parent_collection.batch.dynamic() as batch:
            parent_docs: list[Document] = self.document_loader(
                document_info.source
            ).load()
            parent_docs_formatted: list[dict] = format_documents(
                parent_docs, document_info
            )

            print(f"Ingesting {document_info.filename}")

            print(
                f"A total of {len(parent_docs_formatted)} documents to ingest for the Parent class."
            )

            for idx, doc in enumerate(parent_docs_formatted, start=1):
                if idx % 50 == 0 or idx == len(parent_docs_formatted):
                    print(f"Ingesting {idx} of {len(parent_docs_formatted)}")

                parent_uuid: str = generate_uuid5(doc)
                batch.add_object(doc, uuid=parent_uuid)

                new_doc: dict = {k: v for k, v in doc.items() if k != "content"}
                new_doc[
                    "page"
                ] -= 1  # Substract 1 since the parent already has the page number incremented by 1 and the format will add 1 again.

                child_docs: list[Document] = self.text_splitter.split_documents(
                    [Document(page_content=doc["content"], metadata=new_doc)]
                )
                child_docs_formatted: list[dict] = format_documents(
                    child_docs, document_info
                )

                child_docs_len += len(child_docs_formatted)

                child_docs_with_parent_uuid[parent_uuid] = child_docs_formatted

        parent_failed_objects = self.client.batch.failed_objects

        print(f"parent failed_objects: {parent_failed_objects}")

        if parent_failed_objects:
            print(
                f"Failed to ingest {len(parent_failed_objects)} objects in Parent class.",
            )
            for obj in parent_failed_objects:
                print(obj)

        print(f"Creating {child_docs_len} documents for the Child class.")

        print(f"len(child_docs_with_parent_uuid): {len(child_docs_with_parent_uuid)}")

        child_collection = self.client.collections.get(child_class_name)

        with child_collection.batch.dynamic() as batch:
            for parent_uuid, docs in child_docs_with_parent_uuid.items():
                for doc in docs:
                    batch.add_object(
                        properties=doc, references={refererence_name: parent_uuid}
                    )

        child_failed_objects = self.client.batch.failed_objects
        child_failed_references = self.client.batch.failed_references

        if child_failed_objects:
            print(f"Failed to ingest {len(child_failed_objects)} objects.")
            for obj in child_failed_objects:
                print(obj)
                print(obj.object_.collection)
                print(obj.object_.properties)

        if child_failed_references:
            print(
                f"Failed to create {len(child_failed_references)} references.",
            )
            for ref in child_failed_references:
                print(ref)

        if not child_failed_objects and not child_failed_references:
            print("All documents and references were successfully ingested.")
