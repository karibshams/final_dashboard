# app.py - Main AI Engine for Social Media Comment Management

import os
from typing import Dict, Tuple
import openai
from dotenv import load_dotenv
from prompt import (
    CLASSIFICATION_PROMPT, 
    REPLY_GENERATION_PROMPTS, 
    SYSTEM_PROMPT
)

# Load environment variables from .env file
load_dotenv()

class SocialMediaAI:
    """
    AI-powered system for classifying and responding to social media comments.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AI system with OpenAI API key.
        
        Args:
            api_key: OpenAI API key. If not provided, looks for OPENAI_API_KEY env variable.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Initialize OpenAI client with the new client pattern
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
    
    def classify_comment(self, comment: str) -> str:
        """
        Classify a social media comment into one of the predefined categories.
        
        Args:
            comment: The social media comment to classify
            
        Returns:
            Category: LEAD, PRAISE, SPAM, QUESTION, or COMPLAINT
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": CLASSIFICATION_PROMPT.format(comment=comment)}
                ],
                temperature=0.3,  # Lower temperature for more consistent classification
                max_tokens=10
            )
            
            classification = response.choices[0].message.content.strip().upper()
            
            # Validate classification
            valid_categories = ["LEAD", "PRAISE", "SPAM", "QUESTION", "COMPLAINT"]
            if classification not in valid_categories:
                # Fallback to QUESTION if classification is unclear
                classification = "QUESTION"
            
            return classification
            
        except Exception as e:
            print(f"Error in classification: {str(e)}")
            return "QUESTION"  # Default fallback
    
    def generate_reply(self, comment: str, category: str) -> str:
        """
        Generate an appropriate reply based on the comment and its category.
        
        Args:
            comment: The original comment
            category: The classified category
            
        Returns:
            Generated reply text
        """
        try:
            # Get the appropriate prompt for this category
            prompt = REPLY_GENERATION_PROMPTS.get(
                category, 
                REPLY_GENERATION_PROMPTS["QUESTION"]  # Default to question prompt
            )
            
            # Format the prompt with the comment
            formatted_prompt = prompt.format(comment=comment)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=0.7,  # Balanced temperature for natural responses
                max_tokens=100
            )
            
            reply = response.choices[0].message.content.strip()
            return reply
            
        except Exception as e:
            print(f"Error in reply generation: {str(e)}")
            # Fallback replies
            fallback_replies = {
                "LEAD": "Thank you for your interest! Please send us a direct message for more information.",
                "PRAISE": "Thank you so much for your kind words! We really appreciate your support.",
                "SPAM": "Thank you for your comment. Please feel free to reach out if you have questions about our services.",
                "QUESTION": "Thanks for reaching out! Please send us a direct message and we'll be happy to help.",
                "COMPLAINT": "We're sorry to hear about your experience. Please DM us so we can help resolve this."
            }
            return fallback_replies.get(category, fallback_replies["QUESTION"])
    
    def process_comment(self, comment: str) -> Dict[str, str]:
        """
        Process a comment: classify it and generate an appropriate reply.
        
        Args:
            comment: The social media comment to process
            
        Returns:
            Dictionary with 'category' and 'reply' keys
        """
        # Step 1: Classify the comment
        category = self.classify_comment(comment)
        
        # Step 2: Generate a reply
        reply = self.generate_reply(comment, category)
        
        return {
            "comment": comment,
            "category": category,
            "reply": reply
        }
    
    def batch_process(self, comments: list) -> list:
        """
        Process multiple comments at once.
        
        Args:
            comments: List of comment strings
            
        Returns:
            List of processed results
        """
        results = []
        for comment in comments:
            result = self.process_comment(comment)
            results.append(result)
        return results


# Convenience function for backend integration
def analyze_comment(comment: str, api_key: str = None) -> Dict[str, str]:
    """
    Simple function that backends can call to analyze a single comment.
    
    Args:
        comment: The comment text
        api_key: Optional API key (uses env variable if not provided)
        
    Returns:
        Dict with 'category' and 'reply' keys
    """
    ai = SocialMediaAI(api_key)
    return ai.process_comment(comment)