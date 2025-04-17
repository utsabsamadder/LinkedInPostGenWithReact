# LinkedIn Post Generator

A full-stack application that generates engaging LinkedIn posts using AI. The application allows users to select different AI models, languages, post lengths, and topics to create customized LinkedIn content.

## Project Structure

The project consists of two main parts:

- Backend: A FastAPI application that handles post generation using various LLM models
- Frontend: A React application that provides a user-friendly interface

## Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- Groq API key (for LLM access)


## Installation and Setup

### Backend Setup

1. Clone the repository:

```bash

git clone https://github.com/utsabsamadder/LinkedInPostGenWithReact.git
cd <repository-name>
git branch <branch_name>
git checkout<branch_name>
```
2. Create and activate a virtual environment:

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```
3. Install backend dependencies:
```BASH

cd backend
pip install -r requirements.txt
```
4. Create a .env file in the backend directory with your Groq API key:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
5. Ensure the data directory contains the processed_posts.json file with sample LinkedIn posts.

### Frontend Setup
1. Navigate to the frontend directory:
```BASH

cd frontend
```
2. Install frontend dependencies:
```BASH

npm install
```


## Running the Application
### Start the Backend Server
1. From the backend directory:
```BASH

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload 
```

2. The API will be available at http://localhost:8000
3. You can access the API documentation at http://localhost:8000/docs

### Start the Frontend Development Server
1. From the frontend directory:
```BASH

npm run dev
```
2. The frontend application will be available at http://localhost:5173


### Using the Application
1. Select an AI model from the available options
2. Choose your preferred language (English or Hinglish)
3. Select the desired post length (Short, Medium, or Long)
4. Choose a topic/tag or enter a custom one
5. Optionally, add additional context for your post
6. Click "Generate LinkedIn Post" to create your content
7. View similar posts for inspiration
8. Copy the generated post to your clipboard with a single click


### API Endpoints
- GET /: Check if the API is running
- GET /tags: Get all available tags from processed posts
- POST /generate-post: Generate a LinkedIn post based on parameters
- POST /similar-posts: Retrieve posts similar to the query with filters
- GET /models: Get all available LLM models
- GET /languages: Get all available languages
- GET /lengths: Get all available post lengths


### Features
- Multiple AI model options with different capabilities
- Support for English and Hinglish languages
- Customizable post length
- Topic-based generation
- RAG (Retrieval-Augmented Generation) for better context
- Similar post suggestions for inspiration
- Copy-to-clipboard functionality


## Technologies Used
### Backend
- FastAPI
- LangChain
- Groq API
- FAISS for vector search
- HuggingFace Embeddings
### Frontend
- React
- Vite
- Axios for API requests
- CSS for styling


## Troubleshooting
### Backend Issues
- Missing API Key: Ensure your Groq API key is correctly set in the .env file
- Missing Data: Verify that processed_posts.json exists in the data directory
- Dependency Issues: Make sure all required packages are installed with pip install -r requirements.txt

### Frontend Issues
- Connection Errors: Ensure the backend server is running and accessible
- Display Problems: If the UI looks broken, try clearing your browser cache
- Slow Response: Large post generations may take time, especially with more complex models
