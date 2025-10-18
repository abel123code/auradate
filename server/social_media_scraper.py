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

class FacebookProfile(BaseModel):
    """Schema for Facebook profile data extraction"""
    full_name: str
    bio: str
    location: Optional[str] = None
    work: List[str]
    education: List[str]
    relationship_status: Optional[str] = None
    interests_and_hobbies: List[str]
    favorite_quotes: Optional[str] = None
    music_preferences: List[str]
    movie_preferences: List[str]
    book_preferences: List[str]
    activities_and_groups: List[str]
    life_events: List[str]
    personality_traits: List[str]
    friends_count: Optional[str] = None

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
    
    def scrape_instagram(self, instagram_username: str) -> Dict[str, any]:
        """
        Scrape Instagram profile for lifestyle, interests, and personality.
        
        Args:
            instagram_username: Instagram username (with or without @)
            
        Returns:
            Dictionary with scraped Instagram data
        """
        if not instagram_username or not instagram_username.strip():
            return {"error": "No Instagram username provided"}
        
        # Normalize username
        username = instagram_username.strip().lstrip('@')
        instagram_url = f"https://instagram.com/{username}"
        
        try:
            print(f"[SocialMediaScraper] 🔍 Scraping Instagram: @{username}")
            
            # Use schema-based extraction
            prompt = f"Extract the profile information from this Instagram account: {instagram_url}"
            
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
            
            print(f"[SocialMediaScraper] ✅ Instagram data scraped successfully")
            
            return {
                "platform": "instagram",
                "username": username,
                "url": instagram_url,
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
        
        Args:
            twitter_username: Twitter/X username (with or without @)
            
        Returns:
            Dictionary with scraped Twitter data
        """
        if not twitter_username or not twitter_username.strip():
            return {"error": "No Twitter username provided"}
        
        # Normalize username
        username = twitter_username.strip().lstrip('@')
        twitter_url = f"https://x.com/{username}"
        
        try:
            print(f"[SocialMediaScraper] 🔍 Scraping Twitter/X: @{username}")
            
            # Use schema-based extraction
            prompt = f"Extract the profile information from this Twitter/X account: {twitter_url}"
            
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
    
    def scrape_facebook(self, full_name: str) -> Dict[str, any]:
        """
        Scrape Facebook profile for interests, life events, and social context using full name.
        
        Args:
            full_name: User's full name (e.g., "John Doe")
            
        Returns:
            Dictionary with scraped Facebook data
        """
        if not full_name or not full_name.strip():
            return {"error": "No full name provided"}
        
        try:
            print(f"[SocialMediaScraper] 🔍 Scraping Facebook for: {full_name}")
            
            # Use schema-based extraction with full name
            prompt = f"Find and extract the profile information from {full_name}'s Facebook account"
            
            response = self.client.chat.completions.create(
                model="interfaze-beta",
                messages=[{"role": "user", "content": prompt}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "facebook_profile",
                        "schema": FacebookProfile.model_json_schema(),
                        "strict": True
                    }
                }
            )
            
            # Parse the structured response
            content = response.choices[0].message.content
            profile_data = json.loads(content)
            
            # Format into conversational summary
            summary = self._format_facebook_summary(profile_data)
            
            print(f"[SocialMediaScraper] ✅ Facebook data scraped successfully for {full_name}")
            
            return {
                "platform": "facebook",
                "full_name": full_name,
                "data": summary,
                "structured_data": profile_data,
                "success": True
            }
            
        except Exception as e:
            print(f"[SocialMediaScraper] ❌ Error scraping Facebook: {e}")
            import traceback
            print(f"[SocialMediaScraper] Traceback: {traceback.format_exc()}")
            return {
                "platform": "facebook",
                "full_name": full_name,
                "error": str(e),
                "success": False
            }
    
    def _format_facebook_summary(self, data: Dict) -> str:
        """Format Facebook structured data into conversational summary"""
        parts = []
        
        if data.get('full_name'):
            parts.append(f"Name: {data['full_name']}")
        
        if data.get('bio'):
            parts.append(f"Bio: {data['bio']}")
        
        if data.get('location'):
            parts.append(f"Location: {data['location']}")
        
        if data.get('work'):
            work = ', '.join(data['work'][:3])
            parts.append(f"Work: {work}")
        
        if data.get('education'):
            edu = ', '.join(data['education'])
            parts.append(f"Education: {edu}")
        
        if data.get('relationship_status'):
            parts.append(f"Relationship: {data['relationship_status']}")
        
        if data.get('interests_and_hobbies'):
            interests = ', '.join(data['interests_and_hobbies'])
            parts.append(f"Interests: {interests}")
        
        if data.get('music_preferences'):
            music = ', '.join(data['music_preferences'][:5])
            parts.append(f"Music: {music}")
        
        if data.get('movie_preferences'):
            movies = ', '.join(data['movie_preferences'][:5])
            parts.append(f"Movies: {movies}")
        
        if data.get('book_preferences'):
            books = ', '.join(data['book_preferences'][:5])
            parts.append(f"Books: {books}")
        
        if data.get('activities_and_groups'):
            activities = ', '.join(data['activities_and_groups'][:5])
            parts.append(f"Activities/Groups: {activities}")
        
        if data.get('life_events'):
            events = ', '.join(data['life_events'][:5])
            parts.append(f"Life events: {events}")
        
        if data.get('personality_traits'):
            traits = ', '.join(data['personality_traits'])
            parts.append(f"Personality: {traits}")
        
        if data.get('favorite_quotes'):
            parts.append(f"Favorite quote: {data['favorite_quotes']}")
        
        return '. '.join(parts) + '.'
    
    def scrape_all_profiles(
        self,
        linkedin_url: Optional[str] = None,
        full_name: Optional[str] = None,
        instagram_username: Optional[str] = None,
        twitter_username: Optional[str] = None,
        include_facebook: bool = True
    ) -> List[Dict]:
        """
        Scrape all provided social media profiles.
        
        Args:
            linkedin_url: LinkedIn profile URL
            full_name: User's full name (used for Facebook)
            instagram_username: Instagram username
            twitter_username: Twitter/X username
            include_facebook: Whether to scrape Facebook (default: True)
            
        Returns:
            List of scraping results for each platform
        """
        results = []
        
        if linkedin_url and linkedin_url.strip():
            # Scrape LinkedIn using URL (with Exa crawling)
            results.append(self.scrape_linkedin(linkedin_url))
        
        if full_name and full_name.strip():
            # Scrape Facebook using full name
            if include_facebook:
                results.append(self.scrape_facebook(full_name))
        
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
