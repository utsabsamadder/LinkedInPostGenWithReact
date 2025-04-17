import json
import os
from typing import List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


class RAGService:
    def __init__(self, processed_posts_path="data/processed_posts.json"):
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None
        self.load_and_index_posts(processed_posts_path)

    def load_and_index_posts(self, file_path):
        """Load posts and create a vector store for semantic search"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Posts file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            posts = json.load(f)

        # Convert posts to documents for vector store
        documents = []
        for post in posts:
            # Store the full post data in metadata for retrieval
            metadata = {
                "engagement": post.get("engagement", 0),
                "line_count": post.get("line_count", 0),
                "language": post.get("language", "English"),
                "tags": post.get("tags", [])
            }
            doc = Document(page_content=post["text"], metadata=metadata)
            documents.append(doc)

        # Create vector store
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        print(f"Indexed {len(documents)} posts in the vector store")

    def categorize_length(self, line_count):
        """Categorize post length based on line count"""
        if line_count <= 5:
            return "Short"
        elif 6 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def retrieve_similar_posts(self, query: str, length: str, language: str, tag: str, k=3) -> List[Dict[str, Any]]:
        """
        Retrieve posts similar to the query with specified filters

        Args:
            query: User's input for the post
            length: Desired length (Short, Medium, Long)
            language: Desired language (English, Hinglish)
            tag: Desired tag/topic
            k: Number of results to return

        Returns:
            List of relevant posts with their text and metadata
        """
        # Combine query with filters for better semantic search
        enhanced_query = f"{query} {tag} {language}"

        # Get similar documents
        docs = self.vector_store.similarity_search(enhanced_query, k=k * 3)  # Get more than needed for filtering

        # Filter by length and language
        filtered_docs = []
        for doc in docs:
            doc_length = self.categorize_length(doc.metadata.get("line_count", 0))
            doc_language = doc.metadata.get("language", "English")
            doc_tags = doc.metadata.get("tags", [])

            # Check if document matches filters
            if (doc_length == length and
                    doc_language == language and
                    (tag in doc_tags or any(t.lower() == tag.lower() for t in doc_tags))):
                filtered_docs.append({
                    "text": doc.page_content,
                    "engagement": doc.metadata.get("engagement", 0),
                    "line_count": doc.metadata.get("line_count", 0),
                    "language": doc_language,
                    "tags": doc_tags
                })

        # Sort by engagement (higher first) and take top k
        filtered_docs.sort(key=lambda x: x["engagement"], reverse=True)
        return filtered_docs[:k]