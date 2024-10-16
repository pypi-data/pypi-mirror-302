import deeplake.types

__all__ = [
    "TextDocuments",
]

def TextDocuments(embedding_size: int) -> dict[str, any]:
    """
    A schema for storing text documents.

    - id (uint64)
    - timestamp (uint64)
    - source (text)
    - text (text)
    - embedding (dtype=float32, size=embedding_size)

    Parameters:
         embedding_size: Size of the embeddings

    Examples:
        >>> # Create a dataset with the standard schema
        >>> ds = deeplake.create("ds_path", schema=deeplake.schemas.TextDocuments(768))

        >>> # Customize the schema before creating the dataset
        >>> schema = deeplake.schemas.TextDocuments(768)
        >>>
        >>> # Rename a column in the generated schema
        >>> schema["text_embed"] = my_dict.pop("embedding")
        >>> # Add a custom column
        >>> schema["author"] = deeplake.types.Text()
        >>>
        >>> ds = deeplake.create("ds_path", schema=schema)

    """
    return {
        "id": deeplake.types.UInt64(),
        "source": deeplake.types.Text(),
        "timestamp": deeplake.types.Int64(),
        "text": deeplake.types.Text(),
        "embedding": deeplake.types.Embedding(embedding_size),

    }
