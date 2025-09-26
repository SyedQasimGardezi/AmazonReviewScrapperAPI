# Changelog

All notable changes to the Amazon Review Scraper API project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added
- Initial release of Amazon Review Scraper API
- Core scraping functionality with Playwright
- Flask REST API server
- Support for Amazon India (.in) domains
- Rotating proxy support
- Anti-detection measures (stealth mode, random delays)
- Comprehensive review data extraction:
  - Reviewer name
  - Star rating (1-5 stars)
  - Review title and text
  - Review date
  - Verified purchase status
  - Helpful votes count
- Multiple API endpoints:
  - `GET /` - API documentation
  - `GET /health` - Health check
  - `GET /scrape-reviews` - Scrape reviews via GET
  - `POST /scrape-reviews` - Scrape reviews via POST
- JSON response format
- Error handling and validation
- URL validation for Amazon product pages
- Pagination support for multiple review pages
- Screenshot capability for debugging
- Comprehensive logging
- Virtual environment setup
- Requirements.txt with dependencies
- Setup.py for package installation
- pyproject.toml for modern Python packaging
- MIT License
- Comprehensive README with usage examples
- Contributing guidelines
- Git ignore rules

### Features
- **Easy Integration**: Simple API endpoints for easy integration
- **Robust Scraping**: Handles dynamic content loading and anti-bot measures
- **Proxy Support**: Built-in proxy rotation to avoid IP bans
- **Error Recovery**: Comprehensive error handling and recovery mechanisms
- **Clean JSON Output**: Structured, easy-to-parse JSON responses
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Production Ready**: Flask server ready for deployment

### Technical Details
- **Python Version**: 3.8+
- **Dependencies**: Playwright, Flask
- **Browser**: Chromium (headless)
- **Async Support**: Full async/await support
- **Type Hints**: Comprehensive type annotations
- **Logging**: Structured logging with different levels

### API Examples
```bash
# GET request
curl "http://localhost:5000/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=3"

# POST request
curl -X POST http://localhost:5000/scrape-reviews \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.in/dp/B0CGP252T4", "max_pages": 3}'
```

### Response Format
```json
{
  "status": "success",
  "message": "Successfully scraped X reviews",
  "total_reviews": X,
  "reviews": [
    {
      "reviewer_name": "Reviewer Name",
      "rating": 5,
      "review_title": "Review Title",
      "review_text": "Full review text...",
      "review_date": "Reviewed in India on Date",
      "verified_purchase": true,
      "helpful_votes": 10
    }
  ]
}
```

---

## [Unreleased]

### Planned Features
- Support for other Amazon domains (.com, .co.uk, .de, etc.)
- Rate limiting and request throttling
- Database integration for storing reviews
- Webhook support for real-time notifications
- Docker containerization
- Kubernetes deployment manifests
- CI/CD pipeline setup
- Performance monitoring and metrics
- Caching layer for frequently accessed reviews
- Batch processing for multiple products
- Export functionality (CSV, Excel)
- Advanced filtering and sorting options
- Review sentiment analysis
- Product information extraction
- Price monitoring integration
