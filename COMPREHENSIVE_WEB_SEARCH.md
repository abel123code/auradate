# Comprehensive Web Search Feature using Exa

## Overview

This feature uses **Exa's powerful web search and crawling APIs** to automatically discover and retrieve as much public information as possible about a user, given their display name, full name, and social media usernames. This goes far beyond simple social media scraping by:

1. **Intelligently searching the web** using multiple query variations
2. **Using category-focused searches** to find specific types of content (LinkedIn profiles, personal sites, etc.)
3. **Crawling all discovered URLs** to extract full content
4. **Generating AI-powered summaries** from all gathered information

## Architecture

```
User Input (Full Name + Usernames)
        ↓
Multiple Search Queries (Exa Search API)
        ↓
Discover URLs (10-50+ unique sources)
        ↓
Batch Crawl Content (Exa Get Contents API)
        ↓
AI Summary Generation (Interfaze API)
        ↓
Store in mem0 (Persistent Memory)
```

## Features

### 1. **Multi-Query Search Strategy**

The system automatically generates and executes multiple search queries to maximize coverage:

```python
search_queries = [
    '"Full Name" profile about bio',
    '"Full Name" professional background experience',
    '"Full Name" personal interests hobbies',
    '"Full Name" @username social media',
    'username profile'
]
```

### 2. **Category-Focused Searches**

Uses Exa's category parameter to find specific types of content:

```python
focused_searches = [
    ('"Full Name" LinkedIn', 'linkedin profile'),
    ('"Full Name" professional', 'personal site'),
    ('"Full Name" about me', 'personal site'),
]
```

**Available categories:**
- `linkedin profile`
- `personal site`
- `company`
- `news`
- `research paper`
- `pdf`
- `github`
- `tweet`

### 3. **Intelligent Query Optimization**

Uses Exa's `use_autoprompt=True` to let Exa's AI optimize queries for better results:

```python
result = self.exa.search(
    query=query,
    type="auto",  # Auto-select neural or keyword search
    num_results=10,
    use_autoprompt=True  # AI query optimization
)
```

### 4. **Batch Content Crawling**

After discovering URLs, the system batch-crawls all unique URLs to extract content:

```python
contents_result = self.exa.get_contents(
    ids=urls_list,  # List of discovered URLs
    text=True,      # Extract text content
    summary=True    # Generate AI summaries
)
```

### 5. **AI-Powered Summary Generation**

Combines all discovered content and uses Interfaze to generate a comprehensive personal profile:

```python
summary_prompt = f"""Analyze the following information about {full_name} and create a comprehensive personal profile summary.

Focus on extracting:
- Professional background and current role
- Skills and expertise
- Personal interests and hobbies
- Personality traits and communication style
- Notable achievements or activities

Information from {len(sources)} web sources:
{combined_content}
"""
```

## API Usage

### New Method: `search_web_for_user()`

```python
from social_media_scraper import get_social_media_scraper

scraper = get_social_media_scraper()

result = scraper.search_web_for_user(
    full_name="John Doe",
    username="johndoe",  # Optional: Instagram/Twitter username
    additional_context="Software Engineer at Google",  # Optional
    num_results=10  # Number of results per search query
)
```

### Response Structure

```python
{
    "platform": "web_search",
    "full_name": "John Doe",
    "queries_executed": 6,  # Number of search queries run
    "urls_found": 45,  # Total unique URLs discovered
    "pages_crawled": 20,  # Number of pages successfully crawled
    
    "search_results": [
        {
            "url": "https://example.com/profile",
            "title": "John Doe - Software Engineer",
            "query": "\"John Doe\" professional background",
            "score": 0.95
        },
        # ... more results
    ],
    
    "crawled_content": [
        {
            "url": "https://example.com/profile",
            "title": "John Doe - Software Engineer",
            "text": "Full page content...",
            "summary": "AI-generated summary of the page...",
            "author": "John Doe",
            "published_date": "2024-01-15"
        },
        # ... more content
    ],
    
    "ai_summary": "Comprehensive AI-generated summary from all sources...",
    "data": "Comprehensive AI-generated summary...",  # For mem0 storage
    "success": true
}
```

### Updated `scrape_all_profiles()` Method

```python
results = scraper.scrape_all_profiles(
    full_name="John Doe",
    linkedin_url="https://linkedin.com/in/johndoe",
    instagram_username="@johndoe",
    twitter_username="@johndoe",
    perform_web_search=True,  # Enable web search
    web_search_depth=10  # Results per query
)

# Returns list with results from:
# 1. Web search (if enabled and full_name provided)
# 2. LinkedIn (if URL provided)
# 3. Instagram (if username provided)
# 4. Twitter (if username provided)
```

## Server Endpoint Integration

The `/api/update-user-profile` endpoint now automatically performs web search:

```bash
POST /api/update-user-profile
Content-Type: application/json

{
  "display_name": "user123",
  "full_name": "John Doe",
  "linkedin_url": "https://linkedin.com/in/johndoe",
  "instagram_username": "@johndoe",
  "twitter_username": "@johndoe"
}
```

**Execution flow:**
1. ✅ Comprehensive web search (if full name provided)
2. ✅ LinkedIn scraping (if URL provided)
3. ✅ Instagram scraping (if username provided)
4. ✅ Twitter scraping (if username provided)
5. ✅ All results stored in mem0 memories

## Search Strategy Details

### Standard Searches

| Query Template | Purpose |
|---------------|---------|
| `"{full_name}" profile about bio` | Find general profile pages |
| `"{full_name}" professional background experience` | Find career/work info |
| `"{full_name}" personal interests hobbies` | Find personal information |
| `"{full_name}" @{username} social media` | Find social media presence |
| `{username} profile` | Find profiles by username |

### Category-Focused Searches

| Query | Category | Purpose |
|-------|----------|---------|
| `"{full_name}" LinkedIn` | `linkedin profile` | Find LinkedIn profile directly |
| `"{full_name}" professional` | `personal site` | Find personal websites/portfolios |
| `"{full_name}" about me` | `personal site` | Find about pages |

## Cost Optimization

### API Costs (Exa)

**Search Costs:**
- Neural search (1-25 results): $0.005
- Neural search (26-100 results): $0.025
- Keyword search (1-100 results): $0.0025

**Content Crawling Costs:**
- Text per page: $0.001
- Summary per page: $0.001

**Estimated Total Cost per User:**
- 6 search queries × $0.005 = $0.03
- 20 pages crawled × $0.002 = $0.04
- **Total: ~$0.07 per comprehensive profile**

### Optimization Strategies

1. **Limit search depth**: Reduce `num_results` parameter (default: 10)
2. **Limit crawled pages**: Max 20 URLs crawled by default
3. **Use smart deduplication**: URLs are deduplicated before crawling
4. **Batch API calls**: All URLs crawled in single request

## Testing

### Basic Web Search Test

```bash
cd server
python test_web_search.py
```

### Combined Test (Web Search + Social Media)

Edit `test_web_search.py` and uncomment `test_combined_scraping()`:

```python
# In main()
test_web_search()           # ✓ Currently enabled
test_combined_scraping()    # Uncomment to test
```

### Example Output

```
================================================================================
Testing Comprehensive Web Search
================================================================================

🔍 Searching the web for: John Doe
📱 Username context: @johndoe

✅ WEB SEARCH SUCCESSFUL!

--------------------------------------------------------------------------------
📊 Search Statistics:
   Queries executed: 6
   Unique URLs found: 42
   Pages crawled: 20
--------------------------------------------------------------------------------

🔎 Top Search Results:

1. John Doe - Software Engineer at Google
   URL: https://johndoe.dev
   Query: "John Doe" professional background
   Score: 0.9543

2. About John Doe | Personal Blog
   URL: https://blog.johndoe.com/about
   Query: "John Doe" about me
   Score: 0.9201

[... more results ...]

🤖 AI-Generated Summary:
--------------------------------------------------------------------------------
John Doe is a Senior Software Engineer at Google with 8 years of experience
in distributed systems and machine learning. He holds a Master's degree in
Computer Science from Stanford University. His professional interests include
AI safety, scalable systems architecture, and developer tools.

In his personal time, John enjoys rock climbing, playing guitar, and
contributing to open-source projects. He is particularly passionate about
education technology and has mentored over 50 aspiring engineers through
various programs...
--------------------------------------------------------------------------------
```

## Benefits Over Traditional Scraping

| Feature | Traditional Scraping | Exa Web Search |
|---------|---------------------|----------------|
| **Coverage** | Only specific platforms | Entire public web |
| **Discovery** | Manual URL entry | Automatic discovery |
| **Variety** | Social media only | Articles, blogs, profiles, projects |
| **Updates** | Static URLs | Finds latest content |
| **Accuracy** | Depends on profile access | Aggregates multiple sources |
| **Context** | Limited to platforms | Comprehensive digital footprint |

## Privacy & Ethics

### Ethical Guidelines

✅ **Only scrapes publicly available information**
✅ **Users provide explicit consent** by entering their own details
✅ **Respects robots.txt** (handled by Exa)
✅ **No password-protected content** accessed
✅ **Transparent about data collection** (documented in UI)

### User Control

Users can:
- Choose whether to provide full name
- Opt out by not providing certain fields
- See exactly what was scraped (in API response)
- Delete their data through mem0 API

## Example Use Cases

### 1. Dating App Context (Current Use Case)

Before a video date, the AI avatar can:
- Know the user's professional background
- Reference their hobbies and interests
- Ask about recent projects or achievements
- Create personalized ice-breakers

### 2. Professional Networking

- Discover shared interests before meetings
- Research potential collaborators
- Understand someone's expertise areas

### 3. Content Personalization

- Tailor content recommendations
- Customize conversation topics
- Adapt communication style

## Future Enhancements

### Potential Improvements

1. **Real-time Updates**: Periodically re-search to find new content
2. **Sentiment Analysis**: Analyze tone and personality from content
3. **Relationship Mapping**: Find connections between people
4. **Timeline Construction**: Build chronological life events
5. **Topic Extraction**: Identify key themes and interests
6. **Language Detection**: Support multilingual profiles
7. **Image Analysis**: Analyze profile pictures and shared images
8. **Verification**: Cross-reference information across sources

### Advanced Search Strategies

```python
# Time-based filtering
exa.search(
    query=f'"{full_name}" latest news',
    start_published_date="2024-01-01",
    end_published_date="2024-12-31"
)

# Domain filtering
exa.search(
    query=f'"{full_name}" professional',
    include_domains=["linkedin.com", "github.com", "medium.com"]
)

# Content filtering
exa.search(
    query=f'"{full_name}" achievements',
    include_text=["award", "recognition", "published"]
)
```

## Troubleshooting

### Common Issues

**Issue**: No URLs found
- **Solution**: Try simpler search queries or check if name is unique enough

**Issue**: Crawling fails
- **Solution**: URLs may be behind paywalls or require authentication

**Issue**: AI summary is generic
- **Solution**: Need more distinctive content; try adding more context

**Issue**: High API costs
- **Solution**: Reduce `num_results` and limit pages crawled

## Security Considerations

### API Key Protection

```bash
# Never commit API keys
export EXA_API_KEY='your_key_here'
export INTERFAZE_API_KEY='your_key_here'

# Use environment variables
# Check .env is in .gitignore
```

### Rate Limiting

```python
# Implement rate limiting for production
from time import sleep

def rate_limited_search(queries):
    for query in queries:
        result = exa.search(query)
        sleep(0.5)  # 500ms between requests
        yield result
```

## References

- [Exa Search API Documentation](https://docs.exa.ai/reference/search)
- [Exa Get Contents API](https://docs.exa.ai/reference/get-contents)
- [Exa Python SDK](https://github.com/exa-labs/exa-py)
- [Interfaze API](https://api.interfaze.ai)

---

**Last Updated**: December 2024

**Version**: 1.0.0

**Changelog**:
- Initial implementation of comprehensive web search
- Integration with Exa search and crawling APIs
- AI-powered summary generation
- mem0 storage integration
