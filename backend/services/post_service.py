from typing import List, Dict, Any
from .llm_service import LLMService
from .rag_service import RAGService


class PostService:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()

    def get_length_str(self, length: str) -> str:
        """Convert length category to descriptive string."""
        if length == "Short":
            return "1 to 5 lines"
        if length == "Medium":
            return "6 to 10 lines"
        if length == "Long":
            return "11 to 15 lines"
        return "any length"

    def create_prompt(self, length: str, language: str, tag: str, custom_input: str,
                      similar_posts: List[Dict[str, Any]]) -> str:
        """Create a prompt for the LLM to generate a LinkedIn post."""
        length_str = self.get_length_str(length)

        prompt = f'''
        Generate a LinkedIn post using the below information. No preamble.

        1) Topic: {tag}
        2) Length: {length_str}
        3) Language: {language}
        '''

        if custom_input:
            prompt += f"4) Additional Context: {custom_input}\n"

        prompt += "If Language is Hinglish then it means it is a mix of Hindi and English. The script for the generated post should always be English."

        if len(similar_posts) > 0:
            prompt += "\n5) Use the writing style as per the following examples."
            for i, post in enumerate(similar_posts):
                post_text = post['text']
                engagement = post.get('engagement', 0)
                prompt += f"\n\nExample {i + 1} (Engagement: {engagement})\n\n {post_text}\n\n"

                if i == 2:
                    break

        return prompt

    def generate_post(self, length: str, language: str, tag: str, custom_input: str, model_name: str) -> Dict[str, Any]:
        """Generate a LinkedIn post with the specified parameters."""
        # Retrieve similar posts using RAG
        similar_posts = self.rag_service.retrieve_similar_posts(
            query=custom_input,
            length=length,
            language=language,
            tag=tag,
            k=3
        )

        # Create prompt for the LLM
        prompt = self.create_prompt(length, language, tag, custom_input, similar_posts)

        # Generate post using LLM
        generated_post = self.llm_service.generate_response(prompt, model_name)

        return {
            "post": generated_post,
            "similar_posts": similar_posts
        }