import chromadb
from sentence_transformers import SentenceTransformer
import os

# Create ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="customer_support"
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():

    data_folder = "data"

    all_chunks = []
    all_ids = []

    if not os.path.exists(data_folder):
        print("ERROR: data folder not found.")
        return

    for filename in os.listdir(data_folder):

        if filename.endswith(".txt"):

            filepath = os.path.join(
                data_folder,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

            # Split knowledge into sections
            chunks = [
                chunk.strip()
                for chunk in text.split("\n\n")
                if chunk.strip()
            ]

            for i, chunk in enumerate(chunks):

                all_chunks.append(chunk)

                all_ids.append(
                    f"{filename}_{i}"
                )

            print(
                f"Loaded {filename}: "
                f"{len(chunks)} sections"
            )

    if not all_chunks:

        print(
            "No documents found in data folder."
        )

        return

    # Create embeddings
    embeddings = model.encode(
        all_chunks,
        show_progress_bar=True
    ).tolist()

    # Store/update documents
    collection.upsert(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings
    )

    print()
    print(
        f"Total sections loaded: "
        f"{len(all_chunks)}"
    )

    print(
        "All documents stored successfully!"
    )


def search_documents(
    query,
    n_results=12
):

    # Convert question into embedding
    query_embedding = model.encode(
        [query]
    ).tolist()

    # Search database
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    # Remove duplicates
    unique_documents = []

    for document in documents:

        if document not in unique_documents:

            unique_documents.append(
                document
            )

    return unique_documents


if __name__ == "__main__":

    load_documents()