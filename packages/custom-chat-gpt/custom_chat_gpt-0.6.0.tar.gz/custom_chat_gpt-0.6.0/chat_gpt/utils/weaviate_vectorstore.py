from typing import Any, Literal

from langchain.schema import Document
from langchain_weaviate import WeaviateVectorStore


class WeaviateVectorStoreWrapper(WeaviateVectorStore):
    """Wrapper around WeaviateVectorStore to handle Parent/Child indexes.
    We perform the search on the child index and return the parent index for the LLM.
    """

    import weaviate
    import weaviate.classes as wvc

    def __init__(
        self,
        client: weaviate.WeaviateClient,
        index_name: str,
        text_key: str,
        attributes: list[str] | None = None,
        references: list[wvc.query.QueryReference] | None = None,
        ref_attributes: list[str] | None = None,
    ):
        """Initialize with Weaviate client and search_kwargs."""
        super().__init__(
            client=client,
            index_name=index_name,
            text_key=text_key,
            attributes=attributes,
        )

        self.references = references
        self.parent_attributes = ref_attributes

    def _perform_search(
        self,
        query: str,
        k: int,
        return_score=False,
        search_method: Literal[
            "similarity_search", "hybrid", "near_vector"
        ] = "similarity_search",
        tenant: str | None = None,
        **kwargs: Any,
    ) -> list[Document]:
        """
        Perform a similarity search.

        Parameters:
        query (str): The query string to search for.
        k (int): The number of results to return.
        return_score (bool, optional): Whether to return the score along with the
          document. Defaults to False.
        search_method (Literal['hybrid', 'near_vector'], optional): The search method
          to use. Can be 'hybrid' or 'near_vector'. Defaults to 'hybrid'.
        tenant (Optional[str], optional): The tenant name. Defaults to None.
        **kwargs: Additional parameters to pass to the search method. These parameters
          will be directly passed to the underlying Weaviate client's search method.

        Returns:
        List[Union[Document, Tuple[Document, float]]]: A list of documents that match
          the query. If return_score is True, each document is returned as a tuple
          with the document and its score.

        Raises:
        ValueError: If _embedding is None or an invalid search method is provided.
        """
        import weaviate

        with self._tenant_context(tenant) as collection:
            try:
                if search_method == "similarity_search":
                    result = collection.query.near_text(query=query, limit=k, **kwargs)
                elif search_method == "hybrid":
                    result = collection.query.hybrid(query=query, limit=k, **kwargs)
                elif search_method == "near_vector":
                    result = collection.query.near_vector(limit=k, **kwargs)
                else:
                    raise ValueError(f"Invalid search method: {search_method}")
            except weaviate.exceptions.WeaviateQueryException as e:
                raise ValueError(f"Error during query: {e}")

        assert len(result.objects) > 0, "The search did not return any results."

        docs = []
        for obj in result.objects:
            text = obj.properties.pop(self._text_key)
            filtered_metadata = {
                k: v
                for k, v in obj.metadata.__dict__.items()
                if v is not None and k != "score"
            }
            merged_props = {
                "id": str(obj.uuid),
                **obj.properties,
                **filtered_metadata,
                **({"vector": obj.vector["default"]} if obj.vector else {}),
            }

            if obj.references:
                for ref in obj.references:
                    merged_props[ref] = obj.references[ref].objects[
                        0
                    ]  # HACK: we suppose only links to one object for a given ref

            doc = Document(page_content=text, metadata=merged_props)
            if not return_score:
                docs.append(doc)
            else:
                score = obj.metadata.score
                docs.append((doc, score))

        return docs

    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Document]:
        """Return docs most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.

        Returns:
            List of Documents most similar to the query.
        """

        if self.references is None:
            ########################################################################################
            # Perform similarity search on a single index
            ########################################################################################

            return self._perform_search(query, k, **kwargs)

        else:
            ########################################################################################
            # Perform similarity search on a child index, but return parent index for the LLM
            ########################################################################################

            if not self.parent_attributes:
                raise ValueError(
                    "You must provide parent attributes when using references"
                )

            if len(self.references) > 1:
                raise ValueError(
                    "WeaviateWithFilter can only perform similarity search with one reference at the moment"
                )

            # used by the similarity search method to return the references (here the parent document of the child document)
            kwargs |= {"return_references": self.references}

            # We perform the search on the child index. We add 20 to the k to make sure we get enough documents
            child_docs = self._perform_search(query, k + 20, **kwargs)

            ########################################################################################
            # We retrieve the parent documents from the child documents (and format it for langchain)
            ########################################################################################

            # We retrieve the parent documents from the child documents
            # We only keep the first k documents of the parent documents and avoid duplicates
            # Each retrieved document has a single parent document, hence the [0] index
            parent_index_name = self.references[0].link_on
            unique_pages = set()
            parent_docs = []

            for doc in child_docs:
                ########################################################################################
                # Store unique pages to avoid duplicates
                ########################################################################################

                if doc.metadata["page"] in unique_pages:
                    continue
                unique_pages.add(doc.metadata["page"])

                ########################################################################################
                # Create metadata
                ########################################################################################

                properties = doc.metadata[parent_index_name].properties
                metadata = {}

                for field in self.parent_attributes:
                    if field == "content":
                        continue
                    elif field == "id":
                        metadata[field] = str(doc.metadata[parent_index_name].uuid)
                    else:
                        metadata[field] = properties[field]

                ########################################################################################
                # Create new Parent document
                ########################################################################################

                new_doc = Document(
                    page_content=properties["content"], metadata=metadata
                )

                ########################################################################################
                # Ensures we don't return more than k documents
                ########################################################################################

                parent_docs.append(new_doc)

                if len(parent_docs) == k:
                    break

            return parent_docs
