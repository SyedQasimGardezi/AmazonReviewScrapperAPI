#!/usr/bin/env python3
"""
Test script for Amazon Review Scraper API
"""

import json
from amazon_review_api import get_amazon_reviews

def test_api():
    """Test the Amazon Review Scraper API"""
    print("🧪 Testing Amazon Review Scraper API")
    print("=" * 50)
    
    # Test URL
    product_url = "https://www.amazon.in/10000mAh-Li-Polymer-Indicator-Charging-Consumotion/dp/B0CGP252T4"
    
    print(f"📱 Testing with URL: {product_url}")
    print("⏳ Scraping reviews...")
    
    # Get reviews using the API
    result = get_amazon_reviews(product_url, max_pages=3)
    
    # Print the JSON response
    print("\n📊 API Response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Print summary
    if result["status"] == "success":
        print(f"\n✅ Success! Found {result['total_reviews']} reviews")
        
        # Show first review as example
        if result["reviews"]:
            first_review = result["reviews"][0]
            print(f"\n📝 First Review Example:")
            print(f"   Reviewer: {first_review['reviewer_name']}")
            print(f"   Rating: {first_review['rating']}/5")
            print(f"   Title: {first_review['review_title']}")
            print(f"   Text: {first_review['review_text'][:100]}...")
    else:
        print(f"\n❌ Error: {result['message']}")

if __name__ == "__main__":
    test_api()
