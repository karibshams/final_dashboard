# main.py - Production Integration Example for Social Media AI + GHL

import os
import json
import logging
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

from app import SocialMediaAI
from ghl_integration import GHLIntegration

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SocialMediaAutomationSystem:
    """
    Main integration class that combines AI responses with GHL automation.
    This is what your client's backend would use.
    """
    
    def __init__(self):
        """Initialize both AI and GHL systems."""
        # Initialize AI
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OpenAI API key is required")
        
        self.ai = SocialMediaAI(openai_key)
        
        # Initialize GHL (optional - only if credentials provided)
        ghl_api_key = os.getenv('GHL_API_KEY')
        ghl_location_id = os.getenv('GHL_LOCATION_ID')
        
        self.ghl = None
        if ghl_api_key and ghl_location_id:
            self.ghl = GHLIntegration(ghl_api_key, ghl_location_id)
            logger.info("GHL integration initialized")
        else:
            logger.warning("GHL credentials not found - running without GHL integration")
    
    def process_social_media_comment(
        self,
        comment: str,
        platform: str,
        user_info: Dict,
        post_id: Optional[str] = None
    ) -> Dict:
        """
        Main method to process a social media comment with full automation.
        
        Args:
            comment: The social media comment text
            platform: Platform name (facebook, instagram, youtube, twitter)
            user_info: Dictionary with user details (name, username, email if available)
            post_id: Optional post/video ID for context
            
        Returns:
            Dictionary with AI response and automation results
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "comment": comment,
            "user_info": user_info,
            "post_id": post_id
        }
        
        try:
            # Step 1: AI Processing
            logger.info(f"Processing comment from {user_info.get('username', 'Unknown')}")
            ai_result = self.ai.process_comment(comment)
            
            result.update({
                "ai_category": ai_result['category'],
                "ai_reply": ai_result['reply'],
                "ai_success": True
            })
            
            # Step 2: GHL Integration (if enabled)
            if self.ghl:
                # Prepare contact info for GHL
                contact_info = {
                    "email": user_info.get('email', f"{user_info.get('username', 'user')}@{platform}.social"),
                    "firstName": user_info.get('first_name', user_info.get('username', 'Social')),
                    "lastName": user_info.get('last_name', 'User'),
                    "phone": user_info.get('phone', ''),
                    "source": f"{platform.title()} - Automated",
                    "customFields": {
                        "social_platform": platform,
                        "social_username": user_info.get('username', ''),
                        "first_comment": comment[:500],
                        "comment_date": datetime.now().isoformat(),
                        "post_id": post_id or 'Unknown'
                    }
                }
                
                # Process with GHL
                ghl_result = self.ghl.process_comment(
                    comment=comment,
                    category=ai_result['category'],
                    contact_info=contact_info
                )
                
                result['ghl_integration'] = ghl_result
                result['ghl_success'] = 'error' not in ghl_result
                
                # Log automation actions
                if ghl_result.get('workflow_triggered'):
                    logger.info(f"Workflow triggered for {ai_result['category']} lead")
                if ghl_result.get('tags_added'):
                    logger.info(f"Tags added: {', '.join(ghl_result['tags_added'])}")
            
            # Step 3: Platform-specific actions
            result['platform_actions'] = self._get_platform_actions(
                platform, 
                ai_result['category']
            )
            
            # Step 4: Analytics tracking
            self._track_analytics(result)
            
        except Exception as e:
            logger.error(f"Error processing comment: {str(e)}")
            result['error'] = str(e)
            result['ai_success'] = False
        
        return result
    
    def _get_platform_actions(self, platform: str, category: str) -> Dict:
        """
        Get platform-specific actions based on category.
        
        Returns:
            Dictionary of recommended platform actions
        """
        actions = {
            "should_pin_comment": False,
            "should_hide_comment": False,
            "should_flag_urgent": False,
            "should_auto_reply": True,
            "priority_level": "normal"
        }
        
        # Category-based actions
        if category == "LEAD":
            actions["should_pin_comment"] = True
            actions["priority_level"] = "high"
        elif category == "SPAM":
            actions["should_hide_comment"] = True
            actions["should_auto_reply"] = False
        elif category == "COMPLAINT":
            actions["should_flag_urgent"] = True
            actions["priority_level"] = "urgent"
        
        return actions
    
    def _track_analytics(self, result: Dict):
        """
        Track analytics for reporting.
        In production, this would send to your analytics service.
        """
        analytics_data = {
            "event": "comment_processed",
            "platform": result['platform'],
            "category": result.get('ai_category'),
            "ghl_success": result.get('ghl_success', False),
            "timestamp": result['timestamp']
        }
        
        # In production: send to analytics service
        logger.info(f"Analytics tracked: {analytics_data['category']} on {analytics_data['platform']}")
    
    def batch_process_comments(self, comments: list) -> list:
        """
        Process multiple comments efficiently.
        
        Args:
            comments: List of comment dictionaries
            
        Returns:
            List of results
        """
        results = []
        for comment_data in comments:
            result = self.process_social_media_comment(
                comment=comment_data['comment'],
                platform=comment_data['platform'],
                user_info=comment_data['user_info'],
                post_id=comment_data.get('post_id')
            )
            results.append(result)
        
        return results
    
    def get_automation_stats(self) -> Dict:
        """
        Get statistics about automation performance.
        """
        # In production, this would query your database
        return {
            "total_processed": 1527,
            "leads_captured": 234,
            "workflows_triggered": 189,
            "average_response_time": "1.3s",
            "conversion_rate": "15.3%",
            "platforms": {
                "facebook": 645,
                "instagram": 523,
                "youtube": 234,
                "twitter": 125
            }
        }


# Platform-specific webhook handlers
class FacebookWebhookHandler:
    """Handle Facebook/Instagram webhooks."""
    
    def __init__(self, automation_system: SocialMediaAutomationSystem):
        self.automation = automation_system
    
    def handle_comment(self, webhook_data: Dict) -> Dict:
        """Process Facebook/Instagram comment webhook."""
        # Extract comment data from Facebook webhook format
        comment_text = webhook_data['entry'][0]['changes'][0]['value']['text']
        user_info = {
            'username': webhook_data['entry'][0]['changes'][0]['value']['from']['name'],
            'user_id': webhook_data['entry'][0]['changes'][0]['value']['from']['id']
        }
        
        return self.automation.process_social_media_comment(
            comment=comment_text,
            platform='facebook',
            user_info=user_info,
            post_id=webhook_data['entry'][0]['changes'][0]['value']['post_id']
        )


# Example usage for different scenarios
def example_usage():
    """Examples of how to use the system in production."""
    
    # Initialize the system
    system = SocialMediaAutomationSystem()
    
    # Example 1: Process a single Facebook comment
    result = system.process_social_media_comment(
        comment="I'm interested in your product! How can I order?",
        platform="facebook",
        user_info={
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        },
        post_id="123456789"
    )
    
    print("AI Reply:", result['ai_reply'])
    print("Category:", result['ai_category'])
    if result.get('ghl_integration'):
        print("GHL Actions:", result['ghl_integration'])
    
    # Example 2: Batch process comments
    comments_batch = [
        {
            "comment": "Great product!",
            "platform": "instagram",
            "user_info": {"username": "happy_customer"}
        },
        {
            "comment": "Is this still available?",
            "platform": "facebook",
            "user_info": {"username": "interested_buyer"}
        }
    ]
    
    batch_results = system.batch_process_comments(comments_batch)
    
    # Example 3: Get automation statistics
    stats = system.get_automation_stats()
    print(f"Total leads captured: {stats['leads_captured']}")
    print(f"Conversion rate: {stats['conversion_rate']}")


# FastAPI/Flask endpoint example
def create_api_endpoint(app):
    """
    Example of how to create an API endpoint for your backend.
    This works with FastAPI, Flask, or any Python web framework.
    """
    system = SocialMediaAutomationSystem()
    
    @app.post("/api/process-comment")
    async def process_comment(request_data: dict):
        """API endpoint to process a social media comment."""
        try:
            result = system.process_social_media_comment(
                comment=request_data['comment'],
                platform=request_data['platform'],
                user_info=request_data['user_info'],
                post_id=request_data.get('post_id')
            )
            
            return {
                "success": True,
                "data": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @app.get("/api/automation-stats")
    async def get_stats():
        """Get automation statistics."""
        return system.get_automation_stats()


if __name__ == "__main__":
    # Run examples
    example_usage()