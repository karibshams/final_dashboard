# test.py - Testing Tool for Social Media AI System

import os
from dotenv import load_dotenv
from app import SocialMediaAI
from typing import List

# Load environment variables from .env file
load_dotenv()

# Sample test comments for different categories
TEST_COMMENTS = [
    # LEAD examples
    "I'm interested in your product! How can I order?",
    "Where can I buy this? Looks amazing!",
    "Do you ship to Canada? Want to purchase",
    
    # PRAISE examples
    "Best service ever! You guys are amazing 🎉",
    "Love your products! Keep up the great work!",
    "Just received my order and it's perfect! Thank you!",
    
    # SPAM examples
    "Check out my profile for free followers!!! 🔥🔥",
    "CLICK HERE FOR AMAZING DEALS >>> bit.ly/spam123",
    "Make $5000 working from home! DM me now!",
    
    # QUESTION examples
    "What are your business hours?",
    "Do you have this in size XL?",
    "How long does shipping usually take?",
    
    # COMPLAINT examples
    "My order hasn't arrived yet and it's been 2 weeks!",
    "The product quality is terrible, very disappointed",
    "Worst customer service experience ever!"
]

def test_single_comment(ai: SocialMediaAI, comment: str) -> None:
    """Test a single comment and display results."""
    print("\n" + "="*80)
    print(f"📝 COMMENT: {comment}")
    print("-"*80)
    
    result = ai.process_comment(comment)
    
    print(f"🏷️  CATEGORY: {result['category']}")
    print(f"💬 AI REPLY: {result['reply']}")
    print("="*80)

def test_batch_comments(ai: SocialMediaAI, comments: List[str]) -> None:
    """Test multiple comments and display summary."""
    print("\n🚀 BATCH PROCESSING TEST")
    print("="*80)
    
    results = ai.batch_process(comments)
    
    # Summary statistics
    category_counts = {}
    for result in results:
        cat = result['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\n📊 SUMMARY:")
    for category, count in category_counts.items():
        print(f"   {category}: {count} comments")
    
    print("\n📋 DETAILED RESULTS:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Comment: {result['comment'][:50]}...")
        print(f"   Category: {result['category']}")
        print(f"   Reply: {result['reply'][:100]}...")

def interactive_test(ai: SocialMediaAI) -> None:
    """Interactive testing mode."""
    print("\n🎮 INTERACTIVE TEST MODE")
    print("Type 'quit' to exit")
    print("="*80)
    
    while True:
        comment = input("\n💭 Enter a comment to test: ").strip()
        
        if comment.lower() == 'quit':
            print("👋 Exiting interactive mode...")
            break
        
        if comment:
            test_single_comment(ai, comment)

def main():
    """Main test function."""
    print("🤖 SOCIAL MEDIA AI TESTING TOOL")
    print("================================")
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n❌ ERROR: OpenAI API key not found!")
        print("Please set the OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    try:
        # Initialize AI
        ai = SocialMediaAI(api_key)
        print("✅ AI System initialized successfully!")
        
        while True:
            print("\n📋 TEST MENU:")
            print("1. Test sample comments")
            print("2. Test specific category")
            print("3. Interactive mode")
            print("4. Batch processing test")
            print("5. Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                # Test all sample comments
                for comment in TEST_COMMENTS:
                    test_single_comment(ai, comment)
            
            elif choice == '2':
                # Test specific category
                print("\nCategories: LEAD, PRAISE, SPAM, QUESTION, COMPLAINT")
                category = input("Enter category to test: ").upper()
                
                # Filter comments by expected category
                category_comments = {
                    'LEAD': TEST_COMMENTS[0:3],
                    'PRAISE': TEST_COMMENTS[3:6],
                    'SPAM': TEST_COMMENTS[6:9],
                    'QUESTION': TEST_COMMENTS[9:12],
                    'COMPLAINT': TEST_COMMENTS[12:15]
                }
                
                if category in category_comments:
                    for comment in category_comments[category]:
                        test_single_comment(ai, comment)
                else:
                    print("❌ Invalid category!")
            
            elif choice == '3':
                # Interactive mode
                interactive_test(ai)
            
            elif choice == '4':
                # Batch processing
                test_batch_comments(ai, TEST_COMMENTS)
            
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option! Please try again.")
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()