# preprocess.py (in the root directory)

import json
from typing import Dict, List, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from services.llm_service import LLMService

load_dotenv()

def extract_metadata(post: str, llm) -> Dict[str, Any]:
    """Extract metadata from a post using LLM."""
    template = '''
    You are given a LinkedIn Post. You need to extract the number of lines, language of the post, and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly 3 keys: line_count, language and tags.
    3. tags is an array of text tags. Extract minimum 2 tags.
    4. Language should be English or Hinglish (Hinglish means Hindi + English)

    Here is the actual post on which you need to perform the task: {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = chain.invoke(input={'post': post})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        return res
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse metadata")

def get_unified_tags(posts_with_metadata: List[Dict[str, Any]], llm) -> Dict[str, str]:
    """Unify tags across all posts using LLM."""
    # Collect all unique tags
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    tag_list = ', '.join(unique_tags)

    template = '''
    I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should follow title case convention. Example: "Motivation", "Job Search"
    3. Output should be a JSON object, no preamble.
    4. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}

    Here is the list of tags: 
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = chain.invoke(input={'tags': tag_list})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
        return res
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse tags")

def process_posts(raw_file_path: str, processed_file_path: str = "data/processed_posts.json"):
    """Process raw posts to extract metadata and unify tags."""
    llm_service = LLMService()
    enriched_posts = []

    # Load raw posts
    with open(raw_file_path, encoding="utf-8") as file:
        posts = json.load(file)

        # Extract metadata for each post
        for post in posts:
            llm = llm_service.initialize_llm("llama-3.3-70b-versatile")
            metadata = extract_metadata(post['text'], llm)
            post_with_metadata = {**post, **metadata}  # Merge dictionaries
            enriched_posts.append(post_with_metadata)

    # Unify tags across all posts
    llm = llm_service.initialize_llm("llama-3.3-70b-versatile")
    unified_tags = get_unified_tags(enriched_posts, llm)

    # Update tags in each post
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # fallback to original tag
        post['tags'] = list(new_tags)

    # Save processed posts
    with open(processed_file_path, encoding="utf-8", mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

    return enriched_posts

if __name__ == "__main__":
    print("Starting preprocessing of posts...")
    processed_posts = process_posts("data/raw_posts.json", "data/processed_posts.json")
    print(f"Successfully processed {len(processed_posts)} posts")
    print(f"Processed data saved to data/processed_posts.json")