"""
Flask API Server for Amazon Review Scraper
Simple REST API that returns JSON responses
"""

from flask import Flask, request, jsonify
from amazon_review_api import get_amazon_reviews
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/scrape-reviews', methods=['POST'])
def scrape_reviews():
    """
    Scrape Amazon product reviews
    
    Expected JSON payload:
    {
        "product_url": "https://www.amazon.in/dp/B0CGP252T4",
        "max_pages": 5,
        "proxies": ["http://proxy1:port", "http://proxy2:port"],
        "username": "proxy_user",
        "password": "proxy_pass"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'product_url' not in data:
            return jsonify({
                "status": "error",
                "message": "product_url is required",
                "total_reviews": 0,
                "reviews": []
            }), 400
        
        product_url = data['product_url']
        max_pages = data.get('max_pages', 5)
        proxies = data.get('proxies', None)
        username = data.get('username', None)
        password = data.get('password', None)
        
        logger.info(f"Scraping reviews for: {product_url}")
        
        # Scrape reviews
        result = get_amazon_reviews(
            product_url=product_url,
            max_pages=max_pages,
            proxies=proxies,
            username=username,
            password=password
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in API: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "total_reviews": 0,
            "reviews": []
        }), 500

@app.route('/scrape-reviews', methods=['GET'])
def scrape_reviews_get():
    """
    Scrape Amazon product reviews via GET request
    
    Query parameters:
    - url: Amazon product URL (required)
    - max_pages: Maximum pages to scrape (optional, default: 5)
    """
    try:
        product_url = request.args.get('url')
        
        if not product_url:
            return jsonify({
                "status": "error",
                "message": "url parameter is required",
                "total_reviews": 0,
                "reviews": []
            }), 400
        
        max_pages = int(request.args.get('max_pages', 5))
        
        logger.info(f"Scraping reviews for: {product_url}")
        
        # Scrape reviews
        result = get_amazon_reviews(
            product_url=product_url,
            max_pages=max_pages
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in API: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Internal server error: {str(e)}",
            "total_reviews": 0,
            "reviews": []
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "success",
        "message": "Amazon Review Scraper API is running",
        "version": "1.0.0"
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "Amazon Review Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "POST /scrape-reviews": "Scrape reviews with JSON payload",
            "GET /scrape-reviews?url=<amazon_url>": "Scrape reviews with URL parameter",
            "GET /health": "Health check",
            "GET /": "This documentation"
        },
        "example_usage": {
            "POST": {
                "url": "/scrape-reviews",
                "method": "POST",
                "body": {
                    "product_url": "https://www.amazon.in/dp/B0CGP252T4",
                    "max_pages": 5
                }
            },
            "GET": {
                "url": "/scrape-reviews?url=https://www.amazon.in/dp/B0CGP252T4&max_pages=5",
                "method": "GET"
            }
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Amazon Review Scraper API Server...")
    print("📖 API Documentation: http://localhost:5000/")
    print("🔍 Health Check: http://localhost:5000/health")
    print("📊 Scrape Reviews: http://localhost:5000/scrape-reviews?url=<amazon_url>")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
