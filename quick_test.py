# quick_test.py - Quick test to verify AI is working

import os
from dotenv import load_dotenv
from app import SocialMediaAI

# Load environment variables
load_dotenv()

def test_ai_responses():
    """Quick test to verify AI is generating proper responses."""
    
    print("🧪 Testing AI Response Generation\n")
    
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ ERROR: OpenAI API key not found in .env file!")
        print("Please add: OPENAI_API_KEY=your-key-here")
        return
    
    print(f"✅ API Key found: {api_key[:10]}...\n")
    
    try:
        # Initialize AI
        ai = SocialMediaAI(api_key)
        print("✅ AI initialized successfully\n")
        
        # Test comments
        test_cases = [
            "I'm interested in your product! How can I order?",
            "This is the best service ever! Love it!",
            "What are your business hours?",
            "My order hasn't arrived yet and it's been 2 weeks!",
            "Click here for free followers >>> spam.com"
        ]
        
        for i, comment in enumerate(test_cases, 1):
            print(f"Test {i}:")
            print(f"Comment: {comment}")
            
            try:
                # Process comment
                result = ai.process_comment(comment)
                
                print(f"Category: {result['category']}")
                print(f"Reply: {result['reply']}")
                print("-" * 60)
                
            except Exception as e:
                print(f"Error: {str(e)}")
                print("-" * 60)
            
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error initializing AI: {str(e)}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. No internet connection")
        print("3. OpenAI API quota exceeded")

if __name__ == "__main__":
    test_ai_responses()