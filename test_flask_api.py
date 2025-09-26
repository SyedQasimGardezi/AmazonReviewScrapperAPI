#!/usr/bin/env python3
"""
Test Flask API with the specific Amazon URL
"""

import requests
import json

def test_flask_api():
    """Test the Flask API with the specific Amazon URL"""
    print("🧪 Testing Flask API with Amazon URL")
    print("=" * 50)
    
    # The specific URL you provided
    product_url = "https://www.amazon.in/10000mAh-Li-Polymer-Indicator-Charging-Consumotion/dp/B0CGP252T4/ref=pd_sim_d_sccl_3_3/523-9503265-9095510?pd_rd_w=UKAFU&content-id=amzn1.sym.1f02df7f-f362-4e6d-9a92-f270d75713e4&pf_rd_p=1f02df7f-f362-4e6d-9a92-f270d75713e4&pf_rd_r=X76XGPY8CT7BR4TSTHTC&pd_rd_wg=4ZMnd&pd_rd_r=964c843f-2a9b-421a-8974-4cc70502e5dc&pd_rd_i=B0CGP252T4&th=1"
    
    # Test GET request
    print("📡 Testing GET request...")
    try:
        response = requests.get(
            "http://localhost:5000/scrape-reviews",
            params={
                "url": product_url,
                "max_pages": 3
            },
            timeout=120  # 2 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ GET Request Successful!")
            print(f"Status: {result['status']}")
            print(f"Total Reviews: {result['total_reviews']}")
            print(f"Message: {result['message']}")
            
            if result['reviews']:
                print(f"\n📝 First Review:")
                first_review = result['reviews'][0]
                print(f"   Reviewer: {first_review['reviewer_name']}")
                print(f"   Rating: {first_review['rating']}/5")
                print(f"   Title: {first_review['review_title']}")
                print(f"   Text: {first_review['review_text'][:100]}...")
        else:
            print(f"❌ GET Request Failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
    
    print("\n" + "=" * 50)
    
    # Test POST request
    print("📡 Testing POST request...")
    try:
        response = requests.post(
            "http://localhost:5000/scrape-reviews",
            json={
                "product_url": product_url,
                "max_pages": 3
            },
            timeout=120  # 2 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ POST Request Successful!")
            print(f"Status: {result['status']}")
            print(f"Total Reviews: {result['total_reviews']}")
        else:
            print(f"❌ POST Request Failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    test_flask_api()
