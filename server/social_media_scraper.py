"""
Social Media Scraper Service using Interfaze API and Exa for content crawling.
Scrapes user social media profiles to enrich conversation context for dating app.
"""
import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from pydantic import BaseModel
from exa_py import Exa

# Define schemas for structured extraction

class LinkedInProfile(BaseModel):
    """Schema for LinkedIn profile data extraction"""
    full_name: str
    current_position: str
    current_company: str
    about: str
    previous_positions: List[str]
    education: str
    skills: List[str]
    interests_and_hobbies: str
    professional_achievements: str
    industry: str
    connections_count: Optional[str] = None

class InstagramProfile(BaseModel):
    """Schema for Instagram profile data extraction"""
    username: str
    bio: str
    followers_count: Optional[str] = None
    following_count: Optional[str] = None
    posts_count: Optional[str] = None
    main_content_themes: List[str]
    hobbies_and_interests: List[str]
    lifestyle_type: str
    pets: Optional[str] = None
    travel_destinations: List[str]
    personality_traits: List[str]

class TwitterProfile(BaseModel):
    """Schema for Twitter/X profile data extraction"""
    username: str
    display_name: str
    bio: str
    followers_count: Optional[str] = None
    main_topics: List[str]
    interests_and_passions: List[str]
    communication_style: str
    professional_interests: List[str]
    hobbies: List[str]
    personality_traits: List[str]

class SocialMediaScraper:
    """
    Scrapes social media profiles using Interfaze API to gather contextual information
    about users for better conversation prompts during dates.
    """
    
    def __init__(self, api_key: Optional[str] = None, exa_api_key: Optional[str] = None):
        """
        Initialize Social Media Scraper with Interfaze and Exa APIs.
        
        Args:
            api_key: Interfaze API key (falls back to INTERFAZE_API_KEY env var)
            exa_api_key: Exa API key (falls back to EXA_API_KEY env var)
        """
        interfaze_api_key = api_key or os.getenv("INTERFAZE_API_KEY")
        exa_key = exa_api_key or os.getenv("EXA_API_KEY")
        
        if not interfaze_api_key:
            raise ValueError("INTERFAZE_API_KEY is required for Interfaze API")
        
        if not exa_key:
            raise ValueError("EXA_API_KEY is required for Exa API")
        
        try:
            # Initialize Interfaze client (uses OpenAI SDK structure)
            self.client = OpenAI(
                api_key=interfaze_api_key,
                base_url="https://api.interfaze.ai/v1"
            )
            
            # Initialize Exa client for web crawling
            self.exa = Exa(api_key=exa_key)
            
            print(f"[SocialMediaScraper] ✅ Initialized with Interfaze and Exa APIs")
            
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Error initializing clients: {e}")
            import traceback
            print(f"[SocialMediaScraper] Traceback: {traceback.format_exc()}")
            raise
    
    def scrape_linkedin(self, linkedin_url: str) -> Dict[str, any]:
        """
        Scrape LinkedIn profile using Exa to crawl content, then Interfaze to format it.
        
        Args:
            linkedin_url: LinkedIn profile URL (e.g., "https://linkedin.com/in/username")
            
        Returns:
            Dictionary with scraped LinkedIn data
        """
        if not linkedin_url or not linkedin_url.strip():
            return {"error": "No LinkedIn URL provided"}
        
        try:
            print(f"[SocialMediaScraper] 🔍 Step 1: Crawling LinkedIn URL with Exa: {linkedin_url}")
            
            # Step 1: Use Exa to crawl the LinkedIn page content
            exa_result = self.exa.get_contents([linkedin_url])
            
            if not exa_result or not exa_result.results:
                raise Exception("Exa failed to retrieve LinkedIn content")
            
            # Extract the text content from Exa result
            linkedin_content = exa_result.results[0].text
            print(f"[SocialMediaScraper] ✅ Exa crawled {len(linkedin_content)} characters")
            
            print(f"[SocialMediaScraper] 🔍 Step 2: Formatting with Interfaze...")
            
            # Step 2: Use Interfaze to format the crawled content into structured data
            prompt = f"""Extract and format the professional information from this LinkedIn profile content into the specified schema:

{linkedin_content[:4000]}"""  # Limit content to avoid token limits
            
            response = self.client.chat.completions.create(
                model="interfaze-beta",
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "linkedin_profile",
                        "schema": LinkedInProfile.model_json_schema(),
                        "strict": True
                    }
                }
            )
            
            # Parse the structured response
            content = response.choices[0].message.content
            profile_data = json.loads(content)
            
            # Format into conversational summary
            summary = self._format_linkedin_summary(profile_data)
            print("SUMMARYASJDNAKSD",summary)
            
            print(f"[SocialMediaScraper] ✅ LinkedIn data formatted successfully")
            
            return {
                "platform": "linkedin",
                "url": linkedin_url,
                "data": summary,
                "structured_data": profile_data,
                "success": True
            }
            
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Error scraping LinkedIn: {e}")
            import traceback
            print(f"[SocialMediaScraper] Traceback: {traceback.format_exc()}")
            return {
                "platform": "linkedin",
                "url": linkedin_url,
                "error": str(e),
                "success": False
            }
    
    def _format_linkedin_summary(self, data: Dict) -> str:
        """Format LinkedIn structured data into conversational summary"""
        parts = []
        
        if data.get('full_name'):
            parts.append(f"Name: {data['full_name']}")
        
        if data.get('current_position') and data.get('current_company'):
            parts.append(f"Currently works as {data['current_position']} at {data['current_company']}")
        
        if data.get('about'):
            parts.append(f"About: {data['about']}")
        
        if data.get('previous_positions'):
            prev = ', '.join(data['previous_positions'][:3])  # Top 3
            parts.append(f"Previous experience: {prev}")
        
        if data.get('education'):
            parts.append(f"Education: {data['education']}")
        
        if data.get('skills'):
            skills = ', '.join(data['skills'][:10])  # Top 10 skills
            parts.append(f"Skills: {skills}")
        
        if data.get('interests_and_hobbies'):
            parts.append(f"Interests: {data['interests_and_hobbies']}")
        
        if data.get('industry'):
            parts.append(f"Industry: {data['industry']}")
        
        return '. '.join(parts) + '.'
    
    def scrape_instagram(self, username: str) -> Dict[str, any]:
        """
        Scrape Instagram profile for lifestyle, interests, and visual content.
        Uses Exa to crawl Instagram profile, then Interfaze to format data.
        
        Args:
            username: Instagram username (with or without @ prefix)
            
        Returns:
            Dictionary with scraped Instagram data
        """
        if not username or not username.strip():
            return {"error": "No Instagram username provided"}
        
        try:
            # Clean username and derive URL
            clean_username = username.strip().lstrip('@')
            instagram_url = f"https://instagram.com/{clean_username}"
            
            print(f"[SocialMediaScraper] 🔍 Scraping Instagram for @{clean_username}")
            print(f"[SocialMediaScraper] 📍 Crawling URL: {instagram_url}")
            
            # Step 1: Use Exa to crawl the Instagram profile
            exa_result = self.exa.get_contents(
                ids=[instagram_url],
                text=True
            )
            
            if not exa_result.results or not exa_result.results[0].text:
                print(f"[SocialMediaScraper] ⚠️ No content retrieved from Instagram")
                return {
                    "platform": "instagram",
                    "username": clean_username,
                    "error": "Could not retrieve Instagram content",
                    "success": False
                }
            
            # Get the crawled content
            crawled_content = exa_result.results[0].text
            print(f"[SocialMediaScraper] 📄 Retrieved {len(crawled_content)} characters of content")
            
            # Step 2: Use Interfaze to format the crawled content with schema
            prompt = f"Extract the Instagram profile information from the following content:\n\n{crawled_content[:4000]}"
            
            response = self.client.chat.completions.create(
                model="interfaze-beta",
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "instagram_profile",
                        "schema": InstagramProfile.model_json_schema(),
                        "strict": True
                    }
                }
            )
            
            # Parse the structured response
            content = response.choices[0].message.content
            profile_data = json.loads(content)
            
            # Format into conversational summary
            summary = self._format_instagram_summary(profile_data)
            
            print(f"[SocialMediaScraper] ✅ Instagram data scraped successfully for @{clean_username}")
            
            return {
                "platform": "instagram",
                "username": clean_username,
                "data": summary,
                "structured_data": profile_data,
                "success": True
            }
            
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Error scraping Instagram: {e}")
            import traceback
            print(f"[SocialMediaScraper] Traceback: {traceback.format_exc()}")
            return {
                "platform": "instagram",
                "username": username,
                "error": str(e),
                "success": False
            }
    
    def _format_instagram_summary(self, data: Dict) -> str:
        """Format Instagram structured data into conversational summary"""
        parts = []
        
        if data.get('username'):
            parts.append(f"Instagram: @{data['username']}")
        
        if data.get('bio'):
            parts.append(f"Bio: {data['bio']}")
        
        if data.get('followers_count'):
            parts.append(f"Followers: {data['followers_count']}")
        
        if data.get('main_content_themes'):
            themes = ', '.join(data['main_content_themes'])
            parts.append(f"Content themes: {themes}")
        
        if data.get('hobbies_and_interests'):
            hobbies = ', '.join(data['hobbies_and_interests'])
            parts.append(f"Hobbies: {hobbies}")
        
        if data.get('lifestyle_type'):
            parts.append(f"Lifestyle: {data['lifestyle_type']}")
        
        if data.get('pets'):
            parts.append(f"Pets: {data['pets']}")
        
        if data.get('travel_destinations'):
            travel = ', '.join(data['travel_destinations'])
            parts.append(f"Travel: {travel}")
        
        if data.get('personality_traits'):
            traits = ', '.join(data['personality_traits'])
            parts.append(f"Personality: {traits}")
        
        return '. '.join(parts) + '.'
    
    def scrape_twitter(self, twitter_username: str) -> Dict[str, any]:
        """
        Scrape Twitter/X profile for opinions, interests, and conversation style.
        Uses Exa to crawl Twitter profile, then Interfaze to format data.
        
        Args:
            twitter_username: Twitter/X username (with or without @)
            
        Returns:
            Dictionary with scraped Twitter data
        """
        if not twitter_username or not twitter_username.strip():
            return {"error": "No Twitter username provided"}
        
        # Normalize username and derive URL
        username = twitter_username.strip().lstrip('@')
        twitter_url = f"https://x.com/{username}"
        
        try:
            print(f"[SocialMediaScraper] 🔍 Scraping Twitter/X: @{username}")
            print(f"[SocialMediaScraper] 📍 Crawling URL: {twitter_url}")
            
            # Step 1: Use Exa to crawl the Twitter profile
            exa_result = self.exa.get_contents([twitter_url])
            
            if not exa_result.results or not exa_result.results[0].text:
                print(f"[SocialMediaScraper] ⚠️ No content retrieved from Twitter")
                return {
                    "platform": "twitter",
                    "username": username,
                    "url": twitter_url,
                    "error": "Could not retrieve Twitter content",
                    "success": False
                }
            
            # Get the crawled content
            crawled_content = exa_result.results[0].text
            print(f"[SocialMediaScraper] 📄 Retrieved {len(crawled_content)} characters of content")
            
            # Step 2: Use Interfaze to format the crawled content with schema
            prompt = f"Extract the Twitter/X profile information from the following content:\n\n{crawled_content[:4000]}"
            
            response = self.client.chat.completions.create(
                model="interfaze-beta",
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "twitter_profile",
                        "schema": TwitterProfile.model_json_schema(),
                        "strict": True
                    }
                }
            )
            
            # Parse the structured response
            content = response.choices[0].message.content
            profile_data = json.loads(content)
            
            # Format into conversational summary
            summary = self._format_twitter_summary(profile_data)
            
            print(f"[SocialMediaScraper] ✅ Twitter/X data scraped successfully")
            
            return {
                "platform": "twitter",
                "username": username,
                "url": twitter_url,
                "data": summary,
                "structured_data": profile_data,
                "success": True
            }
            
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Error scraping Twitter/X: {e}")
            import traceback
            print(f"[SocialMediaScraper] Traceback: {traceback.format_exc()}")
            return {
                "platform": "twitter",
                "username": username,
                "error": str(e),
                "success": False
            }
    
    def _format_twitter_summary(self, data: Dict) -> str:
        """Format Twitter structured data into conversational summary"""
        parts = []
        
        if data.get('display_name'):
            parts.append(f"Name: {data['display_name']}")
        
        if data.get('username'):
            parts.append(f"Twitter: @{data['username']}")
        
        if data.get('bio'):
            parts.append(f"Bio: {data['bio']}")
        
        if data.get('followers_count'):
            parts.append(f"Followers: {data['followers_count']}")
        
        if data.get('main_topics'):
            topics = ', '.join(data['main_topics'])
            parts.append(f"Tweets about: {topics}")
        
        if data.get('interests_and_passions'):
            interests = ', '.join(data['interests_and_passions'])
            parts.append(f"Interests: {interests}")
        
        if data.get('communication_style'):
            parts.append(f"Communication style: {data['communication_style']}")
        
        if data.get('professional_interests'):
            prof = ', '.join(data['professional_interests'])
            parts.append(f"Professional interests: {prof}")
        
        if data.get('hobbies'):
            hobbies = ', '.join(data['hobbies'])
            parts.append(f"Hobbies: {hobbies}")
        
        if data.get('personality_traits'):
            traits = ', '.join(data['personality_traits'])
            parts.append(f"Personality: {traits}")
        
        return '. '.join(parts) + '.'
    
    def scrape_all_profiles(
        self,
        linkedin_url: Optional[str] = None,
        instagram_username: Optional[str] = None,
        twitter_username: Optional[str] = None
    ) -> List[Dict]:
        """
        Scrape all provided social media profiles.
        
        Args:
            linkedin_url: LinkedIn profile URL
            instagram_username: Instagram username
            twitter_username: Twitter/X username
            
        Returns:
            List of scraping results for each platform
        """
        results = []
        
        if linkedin_url and linkedin_url.strip():
            # Scrape LinkedIn using URL (with Exa crawling)
            results.append(self.scrape_linkedin(linkedin_url))
        
        if instagram_username and instagram_username.strip():
            results.append(self.scrape_instagram(instagram_username))
        
        if twitter_username and twitter_username.strip():
            results.append(self.scrape_twitter(twitter_username))
        
        return results
    
    def format_for_conversation_context(self, scraping_results: List[Dict]) -> str:
        """
        Format scraped social media data into conversation context for AI.
        
        Args:
            scraping_results: List of scraping results from different platforms
            
        Returns:
            Formatted string for conversation context
        """
        if not scraping_results:
            return ""
        
        context_parts = ["# User Social Media Profile Summary\n"]
        context_parts.append("This information can help you ask relevant questions and create engaging conversation during the date:\n")
        
        for result in scraping_results:
            if not result.get('success', False):
                continue
            
            platform = result.get('platform', 'unknown').title()
            data = result.get('data', '')
            
            context_parts.append(f"\n## {platform} Profile:")
            context_parts.append(data)
            context_parts.append("")  # Empty line for spacing
        
        return "\n".join(context_parts)


# Singleton instance
_scraper_instance = None

def get_social_media_scraper() -> SocialMediaScraper:
    """
    Get or create the singleton SocialMediaScraper instance.
    
    Returns:
        SocialMediaScraper instance
    """
    global _scraper_instance
    
    if _scraper_instance is None:
        try:
            _scraper_instance = SocialMediaScraper()
            print("[SocialMediaScraper] 🎯 Singleton instance created")
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Failed to create singleton: {e}")
            raise
    
    return _scraper_instance
