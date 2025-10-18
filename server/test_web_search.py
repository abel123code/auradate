"""
Test script for comprehensive web search functionality.
Tests Exa's web search and crawling capabilities to gather user information.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from social_media_scraper import get_social_media_scraper

def test_web_search():
    """Test comprehensive web search for a user"""
    print("\n" + "="*80)
    print("Testing Comprehensive Web Search")
    print("="*80)
    
    # Replace with a real name for testing
    full_name = "Yoeven D Khemlani"  # Example: your actual test user
    username = "yoeven"  # Optional: Instagram or Twitter username
    
    try:
        scraper = get_social_media_scraper()
        print(f"\n🔍 Searching the web for: {full_name}")
        print(f"📱 Username context: @{username}\n")
        
        result = scraper.search_web_for_user(
            full_name=full_name,
            username=username,
            num_results=10  # Number of results per query
        )
        
        if result.get('success'):
            print("\n✅ WEB SEARCH SUCCESSFUL!\n")
            print("-" * 80)
            
            # Summary statistics
            print(f"📊 Search Statistics:")
            print(f"   Queries executed: {result.get('queries_executed', 0)}")
            print(f"   Unique URLs found: {result.get('urls_found', 0)}")
            print(f"   Pages crawled: {result.get('pages_crawled', 0)}")
            print("-" * 80)
            
            # Show sample search results
            print(f"\n🔎 Top Search Results:")
            for i, search_result in enumerate(result.get('search_results', [])[:5], 1):
                print(f"\n{i}. {search_result.get('title', 'No title')}")
                print(f"   URL: {search_result.get('url', '')}")
                print(f"   Query: {search_result.get('query', '')}")
                if search_result.get('score'):
                    print(f"   Score: {search_result.get('score'):.4f}")
            
            print("-" * 80)
            
            # Show sample crawled content
            print(f"\n📄 Sample Crawled Content:")
            for i, content in enumerate(result.get('crawled_content', [])[:3], 1):
                print(f"\n{i}. {content.get('title', 'No title')}")
                print(f"   URL: {content.get('url', '')}")
                if content.get('author'):
                    print(f"   Author: {content.get('author')}")
                if content.get('published_date'):
                    print(f"   Published: {content.get('published_date')}")
                if content.get('summary'):
                    print(f"   Summary: {content.get('summary')[:200]}...")
                elif content.get('text'):
                    print(f"   Text preview: {content.get('text')[:200]}...")
            
            print("-" * 80)
            
            # AI-generated summary
            print(f"\n🤖 AI-Generated Summary:")
            print("-" * 80)
            print(result.get('ai_summary', 'No summary available'))
            print("-" * 80)
            
        else:
            print("\n❌ WEB SEARCH FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()

def test_combined_scraping():
    """Test combining web search with social media scraping"""
    print("\n" + "="*80)
    print("Testing Combined Web Search + Social Media Scraping")
    print("="*80)
    
    # Test data - replace with real values
    full_name = "Yoeven D Khemlani"
    linkedin_url = "https://linkedin.com/in/yoeven"
    instagram_username = "@yoeven"
    twitter_username = "@yoeven"
    
    try:
        scraper = get_social_media_scraper()
        
        print(f"\n🌐 Running comprehensive profile scraping for: {full_name}\n")
        
        results = scraper.scrape_all_profiles(
            full_name=full_name,
            linkedin_url=linkedin_url,
            instagram_username=instagram_username,
            twitter_username=twitter_username,
            perform_web_search=True,
            web_search_depth=10
        )
        
        print(f"\n✅ Scraped {len(results)} sources total\n")
        
        success_count = sum(1 for r in results if r.get('success'))
        print(f"📊 Success rate: {success_count}/{len(results)}")
        print("-" * 80)
        
        for result in results:
            platform = result.get('platform', 'unknown').replace('_', ' ').title()
            status = "✅" if result.get('success') else "❌"
            
            print(f"\n{status} {platform}")
            
            if result.get('success'):
                # Show platform-specific info
                if result.get('platform') == 'web_search':
                    print(f"   URLs found: {result.get('urls_found', 0)}")
                    print(f"   Pages crawled: {result.get('pages_crawled', 0)}")
                    print(f"   Summary preview: {result.get('ai_summary', '')[:150]}...")
                else:
                    print(f"   Data: {result.get('data', '')[:150]}...")
            else:
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("\n" + "🚀"*40)
    print("Web Search + Social Media Scraper Test Suite")
    print("🚀"*40)
    
    # Check for API keys
    if not os.getenv("INTERFAZE_API_KEY"):
        print("\n❌ ERROR: INTERFAZE_API_KEY not found in environment variables")
        print("Please set your Interfaze API key:")
        print("export INTERFAZE_API_KEY='your_api_key_here'")
        return
    
    if not os.getenv("EXA_API_KEY"):
        print("\n❌ ERROR: EXA_API_KEY not found in environment variables")
        print("Please set your Exa API key:")
        print("export EXA_API_KEY='your_api_key_here'")
        return
    
    print("\n✅ Interfaze API key found")
    print("✅ Exa API key found")
    
    # Run tests
    # Uncomment the tests you want to run
    
    test_web_search()  # Test web search only
    # test_combined_scraping()  # Test web search + social media
    
    print("\n" + "="*80)
    print("Test suite completed!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
