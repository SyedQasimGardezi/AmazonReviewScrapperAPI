#!/usr/bin/env python3
"""
Comprehensive test suite for Amazon Review Scraper API
"""

import pytest
import asyncio
import json
from unittest.mock import patch, MagicMock
from amazon_review_api import (
    get_amazon_reviews,
    scrape_amazon_reviews,
    scrape_amazon_reviews_sync,
    AmazonReviewScraper
)


class TestAmazonReviewScraper:
    """Test the AmazonReviewScraper class"""
    
    @pytest.fixture
    def scraper(self):
        """Create a scraper instance for testing"""
        return AmazonReviewScraper()
    
    def test_init(self, scraper):
        """Test scraper initialization"""
        assert scraper is not None
        assert scraper.current_proxy_index == 0
    
    def test_get_next_proxy(self, scraper):
        """Test proxy rotation"""
        # Test with no proxies
        scraper.proxies = []
        proxy = scraper.get_next_proxy()
        assert proxy is None
        
        # Test with proxies
        scraper.proxies = ["http://proxy1:8080", "http://proxy2:8080"]
        proxy1 = scraper.get_next_proxy()
        proxy2 = scraper.get_next_proxy()
        proxy3 = scraper.get_next_proxy()
        
        assert proxy1 == "http://proxy1:8080"
        assert proxy2 == "http://proxy2:8080"
        assert proxy3 == "http://proxy1:8080"  # Should cycle back


class TestAPI:
    """Test the main API functions"""
    
    def test_get_amazon_reviews_invalid_url(self):
        """Test with invalid URL"""
        result = asyncio.run(get_amazon_reviews("invalid-url"))
        
        assert result["status"] == "error"
        assert "Invalid Amazon product URL" in result["message"]
        assert result["total_reviews"] == 0
        assert result["reviews"] == []
    
    def test_get_amazon_reviews_empty_url(self):
        """Test with empty URL"""
        result = asyncio.run(get_amazon_reviews(""))
        
        assert result["status"] == "error"
        assert "Invalid Amazon product URL" in result["message"]
        assert result["total_reviews"] == 0
        assert result["reviews"] == []
    
    def test_get_amazon_reviews_none_url(self):
        """Test with None URL"""
        result = asyncio.run(get_amazon_reviews(None))
        
        assert result["status"] == "error"
        assert "Invalid Amazon product URL" in result["message"]
        assert result["total_reviews"] == 0
        assert result["reviews"] == []
    
    @patch('amazon_review_api.scrape_amazon_reviews')
    def test_get_amazon_reviews_success(self, mock_scrape):
        """Test successful review scraping"""
        # Mock successful scraping
        mock_reviews = [
            {
                "reviewer_name": "Test User",
                "rating": 5,
                "review_title": "Great product!",
                "review_text": "This product is amazing.",
                "review_date": "Reviewed in India on 1 January 2025",
                "verified_purchase": True,
                "helpful_votes": 5
            }
        ]
        mock_scrape.return_value = mock_reviews
        
        result = asyncio.run(get_amazon_reviews("https://www.amazon.in/dp/B0CGP252T4"))
        
        assert result["status"] == "success"
        assert result["total_reviews"] == 1
        assert len(result["reviews"]) == 1
        assert result["reviews"][0]["reviewer_name"] == "Test User"
        assert result["reviews"][0]["rating"] == 5
    
    @patch('amazon_review_api.scrape_amazon_reviews')
    def test_get_amazon_reviews_error(self, mock_scrape):
        """Test error handling in review scraping"""
        # Mock error
        mock_scrape.side_effect = Exception("Test error")
        
        result = asyncio.run(get_amazon_reviews("https://www.amazon.in/dp/B0CGP252T4"))
        
        assert result["status"] == "error"
        assert "Test error" in result["message"]
        assert result["total_reviews"] == 0
        assert result["reviews"] == []
    
    def test_get_amazon_reviews_with_proxies(self):
        """Test with proxy configuration"""
        proxies = ["http://proxy1:8080", "http://proxy2:8080"]
        
        with patch('amazon_review_api.scrape_amazon_reviews') as mock_scrape:
            mock_scrape.return_value = []
            
            result = asyncio.run(get_amazon_reviews(
                "https://www.amazon.in/dp/B0CGP252T4",
                max_pages=3,
                proxies=proxies,
                username="test_user",
                password="test_pass"
            ))
            
            # Verify that scrape_amazon_reviews was called with correct parameters
            mock_scrape.assert_called_once_with(
                "https://www.amazon.in/dp/B0CGP252T4",
                3,
                proxies,
                "test_user",
                "test_pass"
            )


class TestScrapeAmazonReviews:
    """Test the scrape_amazon_reviews function"""
    
    @pytest.mark.asyncio
    async def test_scrape_amazon_reviews_invalid_url(self):
        """Test with invalid URL"""
        reviews = await scrape_amazon_reviews("invalid-url")
        assert reviews == []
    
    @pytest.mark.asyncio
    async def test_scrape_amazon_reviews_empty_url(self):
        """Test with empty URL"""
        reviews = await scrape_amazon_reviews("")
        assert reviews == []
    
    @pytest.mark.asyncio
    async def test_scrape_amazon_reviews_none_url(self):
        """Test with None URL"""
        reviews = await scrape_amazon_reviews(None)
        assert reviews == []


class TestScrapeAmazonReviewsSync:
    """Test the synchronous wrapper"""
    
    def test_scrape_amazon_reviews_sync_invalid_url(self):
        """Test with invalid URL"""
        reviews = scrape_amazon_reviews_sync("invalid-url")
        assert reviews == []
    
    def test_scrape_amazon_reviews_sync_empty_url(self):
        """Test with empty URL"""
        reviews = scrape_amazon_reviews_sync("")
        assert reviews == []
    
    def test_scrape_amazon_reviews_sync_none_url(self):
        """Test with None URL"""
        reviews = scrape_amazon_reviews_sync(None)
        assert reviews == []


class TestResponseFormat:
    """Test response format consistency"""
    
    def test_success_response_format(self):
        """Test successful response format"""
        with patch('amazon_review_api.scrape_amazon_reviews') as mock_scrape:
            mock_reviews = [
                {
                    "reviewer_name": "Test User",
                    "rating": 5,
                    "review_title": "Great product!",
                    "review_text": "This product is amazing.",
                    "review_date": "Reviewed in India on 1 January 2025",
                    "verified_purchase": True,
                    "helpful_votes": 5
                }
            ]
            mock_scrape.return_value = mock_reviews
            
            result = asyncio.run(get_amazon_reviews("https://www.amazon.in/dp/B0CGP252T4"))
            
            # Check required fields
            assert "status" in result
            assert "message" in result
            assert "total_reviews" in result
            assert "reviews" in result
            
            # Check status
            assert result["status"] == "success"
            assert isinstance(result["total_reviews"], int)
            assert isinstance(result["reviews"], list)
            
            # Check review format
            if result["reviews"]:
                review = result["reviews"][0]
                required_fields = [
                    "reviewer_name", "rating", "review_title", 
                    "review_text", "review_date", "verified_purchase", "helpful_votes"
                ]
                for field in required_fields:
                    assert field in review
    
    def test_error_response_format(self):
        """Test error response format"""
        result = asyncio.run(get_amazon_reviews("invalid-url"))
        
        # Check required fields
        assert "status" in result
        assert "message" in result
        assert "total_reviews" in result
        assert "reviews" in result
        
        # Check status
        assert result["status"] == "error"
        assert result["total_reviews"] == 0
        assert result["reviews"] == []


class TestURLValidation:
    """Test URL validation logic"""
    
    def test_valid_amazon_urls(self):
        """Test valid Amazon URLs"""
        valid_urls = [
            "https://www.amazon.in/dp/B0CGP252T4",
            "https://www.amazon.com/dp/B0CGP252T4",
            "https://www.amazon.co.uk/dp/B0CGP252T4",
            "https://amazon.in/dp/B0CGP252T4",
            "https://amazon.com/dp/B0CGP252T4",
        ]
        
        for url in valid_urls:
            result = asyncio.run(get_amazon_reviews(url))
            # Should not fail due to invalid URL
            assert result["status"] != "error" or "Invalid Amazon product URL" not in result["message"]
    
    def test_invalid_urls(self):
        """Test invalid URLs"""
        invalid_urls = [
            "not-a-url",
            "https://google.com",
            "https://www.ebay.com/item/123",
            "ftp://amazon.com/dp/B0CGP252T4",
            "",
            None,
        ]
        
        for url in invalid_urls:
            result = asyncio.run(get_amazon_reviews(url))
            assert result["status"] == "error"
            assert "Invalid Amazon product URL" in result["message"]


if __name__ == "__main__":
    pytest.main([__file__])
