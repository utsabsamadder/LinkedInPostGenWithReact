from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from typing import List, Dict, Any

from models.request_models import GeneratePostRequest, SimilarPostsRequest
from services.post_service import PostService
from services.rag_service import RAGService

app = FastAPI(title="LinkedIn Post Generator API")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
post_service = PostService()
rag_service = RAGService()

@app.get("/")
def read_root():
    return {"message": "LinkedIn Post Generator API is running"}

@app.get("/tags")
def get_tags():
    """Get all available tags from processed posts."""
    try:
        # Load tags directly from the processed posts file
        with open("data/processed_posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
            # Extract all tags and flatten the list
            all_tags = []
            for post in posts:
                if "tags" in post and isinstance(post["tags"], list):
                    all_tags.extend(post["tags"])
            # Remove duplicates and sort
            unique_tags = sorted(list(set(all_tags)))
            return {"tags": unique_tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading tags: {str(e)}")

@app.post("/generate-post")
def generate_post(request: GeneratePostRequest):
    """Generate a LinkedIn post based on the provided parameters."""
    try:
        result = post_service.generate_post(
            length=request.length,
            language=request.language,
            tag=request.tag,
            custom_input=request.custom_input or "",
            model_name=request.model_name
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating post: {str(e)}")

@app.post("/similar-posts")
def get_similar_posts(request: SimilarPostsRequest):
    """Retrieve posts similar to the query with specified filters."""
    try:
        similar_posts = rag_service.retrieve_similar_posts(
            query=request.query,
            length=request.length,
            language=request.language,
            tag=request.tag,
            k=request.k
        )
        return {"similar_posts": similar_posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving similar posts: {str(e)}")

@app.get("/models")
def get_available_models():
    """Get all available LLM models."""
    try:
        models = [
            {
                "id": "llama-3.3-70b-versatile",
                "name": "Llama 3.3 70B Versatile",
                "description": "High-performance model with strong capabilities across various tasks"
            },
            {
                "id": "llama-3.1-8b-instant",
                "name": "Llama 3.1 8B Instant",
                "description": "Faster, lighter model for quick responses"
            },
            {
                "id": "deepseek-r1-distill-llama-70b",
                "name": "Deepseek R1 Distill Llama 70B",
                "description": "Specialized model with strong reasoning capabilities"
            }
        ]
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving models: {str(e)}")

@app.get("/languages")
def get_available_languages():
    """Get all available languages."""
    return {
        "languages": [
            {"id": "English", "name": "English"},
            {"id": "Hinglish", "name": "Hinglish (Hindi + English)"}
        ]
    }

@app.get("/lengths")
def get_available_lengths():
    """Get all available post lengths."""
    return {
        "lengths": [
            {"id": "Short", "name": "Short (1-5 lines)"},
            {"id": "Medium", "name": "Medium (6-10 lines)"},
            {"id": "Long", "name": "Long (11-15 lines)"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)