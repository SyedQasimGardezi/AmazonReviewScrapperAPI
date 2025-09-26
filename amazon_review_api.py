"""
Amazon Review Scraper API
A clean, easy-to-integrate API for scraping Amazon product reviews.
"""

import asyncio
import random
import json
from typing import List, Dict, Optional
from urllib.parse import urlparse
import logging
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Review:
    """Data class for storing review information"""
    reviewer_name: str
    rating: int
    review_title: str
    review_text: str
    review_date: str
    verified_purchase: bool
    helpful_votes: int

class AmazonReviewScraper:
    """Clean Amazon product review scraper API"""
    
    def __init__(self, proxies: List[str] = None, username: str = None, password: str = None):
        """
        Initialize the scraper
        
        Args:
            proxies: List of proxy URLs (optional)
            username: Proxy username (optional)
            password: Proxy password (optional)
        """
        self.proxies = proxies or []
        self.proxy_username = username
        self.proxy_password = password
        self.current_proxy_index = 0
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def get_next_proxy(self) -> Optional[str]:
        """Get the next proxy in rotation"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self.user_agents)
    
    async def setup_browser(self) -> None:
        """Setup browser with optional proxy and anti-detection measures"""
        playwright = await async_playwright().start()
        
        # Browser launch options with anti-detection
        browser_options = {
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--disable-extensions',
                '--disable-gpu',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-default-apps',
                '--disable-popup-blocking',
                '--disable-translate',
                '--disable-background-timer-throttling',
                '--disable-renderer-backgrounding',
                '--disable-backgrounding-occluded-windows',
                '--disable-ipc-flooding-protection'
            ]
        }
        
        # Add proxy if available
        proxy_url = self.get_next_proxy()
        if proxy_url:
            proxy_parts = urlparse(proxy_url)
            browser_options['proxy'] = {
                'server': f"{proxy_parts.scheme}://{proxy_parts.hostname}:{proxy_parts.port}",
                'username': self.proxy_username,
                'password': self.proxy_password
            }
            logger.info(f"Using proxy: {proxy_url}")
        
        self.browser = await playwright.chromium.launch(**browser_options)
        
        # Create context with additional anti-detection measures
        self.context = await self.browser.new_context(
            user_agent=self.get_random_user_agent(),
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Add stealth scripts
        await self.context.add_init_script("""
            try {
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            } catch(e) {}
            
            try {
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            } catch(e) {}
            
            try {
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
            } catch(e) {}
            
            window.chrome = {
                runtime: {},
            };
        """)
        
        self.page = await self.context.new_page()
        logger.info("Browser setup complete")
    
    async def random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
        """Add random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    async def navigate_to_product(self, product_url: str) -> bool:
        """Navigate to Amazon product page"""
        try:
            logger.info(f"Navigating to product: {product_url}")
            await self.page.goto(product_url, wait_until='domcontentloaded', timeout=15000)
            await self.random_delay(2, 4)
            
            # Check if we're on a valid product page
            if "amazon." not in self.page.url:
                logger.error("Not on a valid Amazon product page")
                return False
                
            # Check for captcha or blocking
            if await self.page.locator("text=Robot or human?").count() > 0:
                logger.warning("Captcha detected")
                return False
                
            if await self.page.locator("text=Sorry, we just need to make sure you're not a robot").count() > 0:
                logger.warning("Bot detection triggered")
                return False
            
            # Scroll down to reviews section and wait for it to load
            await self.scroll_to_reviews_section()
                
            return True
            
        except Exception as e:
            logger.error(f"Error navigating to product: {e}")
            return False
    
    async def scroll_to_reviews_section(self) -> None:
        """Scroll to reviews section and wait for it to load"""
        try:
            logger.info("Scrolling to reviews section...")
            
            # First, scroll down gradually to find reviews section
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.3)")
            await self.random_delay(1, 2)
            
            # Look for reviews section indicators
            reviews_indicators = [
                'h2:has-text("Customer reviews")',
                'h2:has-text("Top reviews")',
                'h3:has-text("Top reviews")',
                'h3:has-text("Customer reviews")',
                '[data-hook="dp-local-reviews-header"]',
                '#cm-cr-dp-review-list',
                '.reviews-content',
                '[data-hook="top-customer-reviews-widget"]'
            ]
            
            # Wait for any reviews indicator to appear
            found_indicator = False
            for indicator in reviews_indicators:
                try:
                    await self.page.wait_for_selector(indicator, timeout=2000)
                    logger.info(f"Found reviews section with indicator: {indicator}")
                    found_indicator = True
                    break
                except:
                    continue
            
            # If no indicator found, scroll more
            if not found_indicator:
                logger.info("No reviews indicator found, scrolling more...")
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.6)")
                await self.random_delay(2, 3)
                
                # Try again to find indicators
                for indicator in reviews_indicators:
                    try:
                        await self.page.wait_for_selector(indicator, timeout=2000)
                        logger.info(f"Found reviews section with indicator: {indicator}")
                        found_indicator = True
                        break
                    except:
                        continue
            
            # Scroll a bit more to ensure reviews are visible
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.8)")
            await self.random_delay(2, 3)
            
            # Wait for reviews to load
            await self.wait_for_reviews_to_load()
            
        except Exception as e:
            logger.warning(f"Error scrolling to reviews section: {e}")
    
    async def wait_for_reviews_to_load(self) -> None:
        """Wait for reviews to load on the page"""
        try:
            logger.info("Waiting for reviews to load...")
            
            # Wait for review elements to appear
            review_selectors = [
                'li[data-hook="review"]',
                '#cm-cr-dp-review-list li[data-hook="review"]',
                '[data-hook="review"]',
                '.review'
            ]
            
            # Try multiple times with different approaches
            for attempt in range(3):
                logger.info(f"Attempt {attempt + 1} to find reviews...")
                
                for selector in review_selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=3000)
                        logger.info(f"Reviews loaded with selector: {selector}")
                        return
                    except:
                        continue
                
                # If no reviews found, scroll a bit more and wait
                if attempt < 2:  # Don't scroll on last attempt
                    logger.info("No reviews found, scrolling more and waiting...")
                    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.9)")
                    await self.random_delay(2, 4)
            
            # Final attempt - wait a bit more
            logger.info("Final attempt - waiting longer for reviews...")
            await self.random_delay(3, 5)
            
        except Exception as e:
            logger.warning(f"Error waiting for reviews to load: {e}")
    
    async def extract_reviews_from_page(self) -> List[Review]:
        """Extract reviews from current page"""
        reviews = []
        
        try:
            # Wait for reviews to load - try multiple selectors
            selectors_to_try = [
                'li[data-hook="review"]',  # Main selector for Amazon India
                '#cm-cr-dp-review-list li[data-hook="review"]',  # More specific
                '[data-hook="review"]',
                '.review',  # Alternative selector
                '#cm-cr-dp-review-list .review'
            ]
            
            review_elements = []
            for selector in selectors_to_try:
                try:
                    await self.page.wait_for_selector(selector, timeout=5000)
                    review_elements = await self.page.query_selector_all(selector)
                    if review_elements:
                        logger.info(f"Found {len(review_elements)} reviews using selector: {selector}")
                        break
                except:
                    continue
            
            # If no reviews found, try scrolling and waiting more
            if not review_elements:
                logger.info("No reviews found initially, trying to scroll and wait...")
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.8)")
                await self.random_delay(2, 4)
                
                # Try again with all selectors
                for selector in selectors_to_try:
                    try:
                        await self.page.wait_for_selector(selector, timeout=3000)
                        review_elements = await self.page.query_selector_all(selector)
                        if review_elements:
                            logger.info(f"Found {len(review_elements)} reviews after scrolling using selector: {selector}")
                            break
                    except:
                        continue
            
            if not review_elements:
                logger.warning("No review elements found after scrolling")
                return reviews
            
            for element in review_elements:
                try:
                    # Extract reviewer name
                    reviewer_name = "Anonymous"
                    name_element = await element.query_selector('.a-profile-name')
                    if name_element:
                        reviewer_name = await name_element.inner_text()
                    
                    # Extract rating - try multiple selectors and methods
                    rating = 0
                    rating_selectors = [
                        '[data-hook="review-star-rating"] .a-icon-alt',
                        '[data-hook="review-star-rating"] span',
                        '.review-rating .a-icon-alt',
                        '.a-icon-star .a-icon-alt',
                        '[data-hook="review-star-rating"]',
                        '.a-icon-star span'
                    ]
                    
                    for selector in rating_selectors:
                        try:
                            rating_element = await element.query_selector(selector)
                            if rating_element:
                                # Try different methods to get rating
                                rating_text = await rating_element.get_attribute('innerHTML')
                                if not rating_text:
                                    rating_text = await rating_element.inner_text()
                                
                                if rating_text:
                                    # Extract number from text like "5.0 out of 5 stars" or "5 stars"
                                    import re
                                    numbers = re.findall(r'\d+\.?\d*', rating_text)
                                    if numbers:
                                        rating = int(float(numbers[0]))
                                        break
                        except Exception as e:
                            continue
                    
                    # If still no rating found, try looking for star classes
                    if rating == 0:
                        try:
                            star_elements = await element.query_selector_all('.a-icon-star')
                            for star_element in star_elements:
                                class_name = await star_element.get_attribute('class')
                                if class_name and 'a-star-' in class_name:
                                    # Extract rating from class like "a-star-5"
                                    import re
                                    star_match = re.search(r'a-star-(\d+)', class_name)
                                    if star_match:
                                        rating = int(star_match.group(1))
                                        break
                        except:
                            pass
                    
                    # Extract review title
                    review_title = ""
                    title_element = await element.query_selector('[data-hook="review-title"] span:not([class])')
                    if title_element:
                        review_title = await title_element.inner_text()
                    
                    # Extract review text
                    review_text = ""
                    text_element = await element.query_selector('[data-hook="review-collapsed"] span')
                    if text_element:
                        review_text = await text_element.inner_text()
                    
                    # Extract review date
                    review_date = ""
                    date_element = await element.query_selector('[data-hook="review-date"]')
                    if date_element:
                        review_date = await date_element.inner_text()
                    
                    # Check if verified purchase
                    verified_purchase = False
                    verified_element = await element.query_selector('[data-hook="avp-badge-linkless"]')
                    if verified_element:
                        verified_text = await verified_element.inner_text()
                        if "verified" in verified_text.lower() or "purchase" in verified_text.lower():
                            verified_purchase = True
                    
                    # Extract helpful votes
                    helpful_votes = 0
                    helpful_element = await element.query_selector('[data-hook="helpful-vote-statement"]')
                    if helpful_element:
                        helpful_text = await helpful_element.inner_text()
                        if "people found this helpful" in helpful_text:
                            try:
                                helpful_votes = int(helpful_text.split()[0])
                            except:
                                helpful_votes = 0
                    
                    review = Review(
                        reviewer_name=reviewer_name.strip(),
                        rating=rating,
                        review_title=review_title.strip(),
                        review_text=review_text.strip(),
                        review_date=review_date.strip(),
                        verified_purchase=verified_purchase,
                        helpful_votes=helpful_votes
                    )
                    
                    reviews.append(review)
                    
                except Exception as e:
                    logger.warning(f"Error extracting individual review: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting reviews from page: {e}")
            
        return reviews
    
    async def scrape_reviews(self, product_url: str, max_pages: int = 5) -> List[Dict]:
        """
        Scrape reviews from Amazon product page
        
        Args:
            product_url: Amazon product URL
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of review dictionaries
        """
        all_reviews = []
        
        try:
            await self.setup_browser()
            
            # Navigate to product page
            if not await self.navigate_to_product(product_url):
                return all_reviews
            
            # Skip "See all reviews" click to avoid login screens - extract from main page
            logger.info("Extracting reviews from main page to avoid login screens...")
            await self.scroll_to_reviews_section()
            
            # Additional scroll to ensure we're at the reviews section
            logger.info("Ensuring we're at the reviews section...")
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.85)")
            await self.random_delay(2, 3)
            
            # Extract reviews from each page
            for page_num in range(max_pages):
                logger.info(f"Extracting reviews from page {page_num + 1}")
                
                # Extract reviews from current page
                page_reviews = await self.extract_reviews_from_page()
                all_reviews.extend(page_reviews)
                
                logger.info(f"Found {len(page_reviews)} reviews on page {page_num + 1}")
                
                # Try to go to next page
                try:
                    next_button = await self.page.query_selector('li.a-last a')
                    if next_button and await next_button.is_enabled():
                        await next_button.click()
                        await self.random_delay(3, 6)
                        await self.page.wait_for_load_state('networkidle')
                    else:
                        logger.info("No more pages available")
                        break
                except Exception as e:
                    logger.warning(f"Error navigating to next page: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Error getting reviews: {e}")
        finally:
            await self.close()
            
        # Convert to dictionaries for easy JSON serialization
        return [asdict(review) for review in all_reviews]
    
    async def close(self) -> None:
        """Close browser and cleanup"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

# Convenience functions for easy integration
async def scrape_amazon_reviews(product_url: str, max_pages: int = 5, proxies: List[str] = None, username: str = None, password: str = None) -> List[Dict]:
    """
    Convenience function to scrape Amazon reviews
    
    Args:
        product_url: Amazon product URL
        max_pages: Maximum number of pages to scrape
        proxies: List of proxy URLs (optional)
        username: Proxy username (optional)
        password: Proxy password (optional)
        
    Returns:
        List of review dictionaries
    """
    scraper = AmazonReviewScraper(proxies=proxies, username=username, password=password)
    return await scraper.scrape_reviews(product_url, max_pages)

def scrape_amazon_reviews_sync(product_url: str, max_pages: int = 5, proxies: List[str] = None, username: str = None, password: str = None) -> List[Dict]:
    """
    Synchronous wrapper for scraping Amazon reviews
    
    Args:
        product_url: Amazon product URL
        max_pages: Maximum number of pages to scrape
        proxies: List of proxy URLs (optional)
        username: Proxy username (optional)
        password: Proxy password (optional)
        
    Returns:
        List of review dictionaries
    """
    return asyncio.run(scrape_amazon_reviews(product_url, max_pages, proxies, username, password))

# API Response function
def get_amazon_reviews(product_url: str, max_pages: int = 5, proxies: List[str] = None, username: str = None, password: str = None) -> Dict:
    """
    Main API function that returns JSON response
    
    Args:
        product_url: Amazon product URL
        max_pages: Maximum number of pages to scrape
        proxies: List of proxy URLs (optional)
        username: Proxy username (optional)
        password: Proxy password (optional)
        
    Returns:
        Dictionary with status and reviews data
    """
    try:
        reviews = scrape_amazon_reviews_sync(product_url, max_pages, proxies, username, password)
        
        return {
            "status": "success",
            "message": f"Successfully scraped {len(reviews)} reviews",
            "total_reviews": len(reviews),
            "reviews": reviews
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error scraping reviews: {str(e)}",
            "total_reviews": 0,
            "reviews": []
        }

# Example usage
if __name__ == "__main__":
    # Example usage
    product_url = "https://www.amazon.in/10000mAh-Li-Polymer-Indicator-Charging-Consumotion/dp/B0CGP252T4"
    
    # Get reviews using the API
    result = get_amazon_reviews(product_url, max_pages=3)
    
    # Print the JSON response
    print(json.dumps(result, indent=2, ensure_ascii=False))