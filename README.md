# Amazon Review Scraper API

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/flask-3.0%2B-red.svg)](https://flask.palletsprojects.com/)
[![Playwright](https://img.shields.io/badge/playwright-1.40%2B-orange.svg)](https://playwright.dev/)

A clean, easy-to-integrate API for scraping Amazon product reviews using Playwright with rotating proxies and anti-detection measures.

## ✨ Features

- **🚀 Easy Integration**: Simple REST API endpoints for seamless integration
- **🛡️ Robust Scraping**: Handles dynamic content loading and anti-bot measures
- **🔄 Proxy Support**: Built-in proxy rotation to avoid IP bans and rate limiting
- **🥷 Anti-Detection**: Stealth mode, random delays, and realistic browser headers
- **📊 Clean JSON Output**: Structured, easy-to-parse JSON responses
- **⚡ Error Recovery**: Comprehensive error handling and recovery mechanisms
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux
- **🐳 Docker Ready**: Containerized deployment with Docker and Docker Compose
- **📈 Production Ready**: Flask server optimized for production deployment

## 🎯 What You Get

Extract comprehensive review data including:
- ⭐ Star ratings (1-5 stars)
- 👤 Reviewer names
- 📝 Review titles and full text
- 📅 Review dates
- ✅ Verified purchase status
- 👍 Helpful votes count
- 🖼️ Review images (when available)

## 📋 Requirements

- Python 3.8 or higher
- Playwright
- Flask
- Chromium browser

## 🛠️ Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/SyedQasimGardezi/AmazonReviewScrapperAPI.git
cd AmazonReviewScrapperAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Start the API server
python api_server.py
```

### Using Make (Recommended)

```bash
# Full setup
make setup

# Run the server
make run

# Run tests
make test
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t amazon-review-scraper-api .
docker run -p 5000:5000 amazon-review-scraper-api
```

## 🚀 Quick Start

### 1. Start the API Server
```bash
python api_server.py
```
The API will be available at `http://localhost:5000`

### 2. Scrape Reviews

#### Method 1: GET Request (Browser)
Open your browser and go to:
```
http://localhost:5000/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=3
```

#### Method 2: cURL
```bash
curl "http://localhost:5000/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=3"
```

#### Method 3: POST Request
```bash
curl -X POST http://localhost:5000/scrape-reviews \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.amazon.in/dp/B0CGP252T4", "max_pages": 3}'
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API documentation and usage examples |
| `/health` | GET | Health check endpoint |
| `/scrape-reviews` | GET/POST | Scrape Amazon product reviews |

### GET /scrape-reviews
**Parameters:**
- `url` (required): Amazon product URL
- `max_pages` (optional): Number of review pages to scrape (default: 3)

### POST /scrape-reviews
**Request Body:**
```json
{
  "product_url": "https://www.amazon.in/dp/B0CGP252T4",
  "max_pages": 3
}
```

## 📝 Response Format

```json
{
  "status": "success",
  "message": "Successfully scraped X reviews",
  "total_reviews": X,
  "reviews": [
    {
      "reviewer_name": "John Doe",
      "rating": 5,
      "review_title": "Excellent product!",
      "review_text": "This product exceeded my expectations...",
      "review_date": "Reviewed in India on 15 January 2025",
      "verified_purchase": true,
      "helpful_votes": 10
    }
  ]
}
```

## 🔧 Configuration

### Proxy Settings
Edit `config.py` to configure proxies:

```python
PROXIES = [
    "http://proxy1:port",
    "http://proxy2:port",
    # Add more proxies
]

USERNAME = "your_proxy_username"
PASSWORD = "your_proxy_password"
```

### Environment Variables
```bash
export PROXY_USERNAME="your_username"
export PROXY_PASSWORD="your_password"
export FLASK_ENV="production"
```

## 🧪 Testing

```bash
# Run tests
make test

# Or directly
python test_api.py
```

## 📚 Usage Examples

### Python Integration
```python
import requests

# Scrape reviews
response = requests.get(
    "http://localhost:5000/scrape-reviews",
    params={
        "url": "https://www.amazon.in/dp/B0CGP252T4",
        "max_pages": 5
    }
)

data = response.json()
print(f"Found {data['total_reviews']} reviews")

for review in data['reviews']:
    print(f"Rating: {review['rating']}/5")
    print(f"Review: {review['review_text'][:100]}...")
    print("---")
```

### JavaScript/Node.js Integration
```javascript
const response = await fetch(
  'http://localhost:5000/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=3'
);
const data = await response.json();
console.log(`Found ${data.total_reviews} reviews`);
```

### PHP Integration
```php
<?php
$url = 'http://localhost:5000/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=3';
$response = file_get_contents($url);
$data = json_decode($response, true);
echo "Found " . $data['total_reviews'] . " reviews";
?>
```

## 🐳 Docker Deployment

### Docker Compose (Recommended)
```yaml
version: '3.8'
services:
  amazon-scraper:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: amazon-scraper
spec:
  replicas: 3
  selector:
    matchLabels:
      app: amazon-scraper
  template:
    metadata:
      labels:
        app: amazon-scraper
    spec:
      containers:
      - name: amazon-scraper
        image: amazon-review-scraper-api:latest
        ports:
        - containerPort: 5000
```

## ⚠️ Important Notes

- **Rate Limiting**: Use reasonable delays between requests to avoid being blocked
- **Proxy Usage**: Configure proxies for better success rates and to avoid IP bans
- **Legal Compliance**: Ensure compliance with Amazon's Terms of Service and robots.txt
- **Error Handling**: Always check the response status and handle errors appropriately
- **Resource Usage**: Monitor memory and CPU usage for large-scale scraping

## 🐛 Troubleshooting

### Common Issues

1. **"No reviews found"**
   - ✅ Check if the product URL is valid
   - ✅ Verify the product has reviews
   - ✅ Try with different proxy settings
   - ✅ Check if reviews are loaded dynamically

2. **"Page not found"**
   - ✅ Ensure the URL is a valid Amazon product page
   - ✅ Check if the product is available in your region
   - ✅ Verify the URL format

3. **"Timeout errors"**
   - ✅ Increase timeout settings
   - ✅ Check your internet connection
   - ✅ Try with different proxy settings
   - ✅ Check if the page is loading slowly

4. **"Proxy errors"**
   - ✅ Verify proxy credentials
   - ✅ Check proxy server status
   - ✅ Try different proxy servers

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

- [ ] Support for other Amazon domains (.com, .co.uk, .de, etc.)
- [ ] Rate limiting and request throttling
- [ ] Database integration for storing reviews
- [ ] Webhook support for real-time notifications
- [ ] Advanced filtering and sorting options
- [ ] Review sentiment analysis
- [ ] Product information extraction
- [ ] Price monitoring integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) for browser automation
- [Flask](https://flask.palletsprojects.com/) for the web framework
- Amazon for providing the review data (please respect their Terms of Service)

⭐ **Star this repository if you find it helpful!**
