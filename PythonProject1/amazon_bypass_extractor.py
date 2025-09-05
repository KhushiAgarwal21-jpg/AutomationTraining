#!/usr/bin/env python3
"""
Amazon Bypass Extractor
Uses multiple strategies to bypass Amazon's anti-bot measures and extract Hot New Releases data
"""

import json
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import random
import requests
from bs4 import BeautifulSoup

class AmazonBypassExtractor:
    def __init__(self, headless=False):
        """Initialize with maximum anti-detection measures"""
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with maximum anti-detection"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Maximum anti-detection measures
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Additional options to prevent detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        
        # Enable JavaScript (important for dynamic content)
        chrome_options.add_argument("--enable-javascript")
        
        # Disable images to speed up loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute anti-detection scripts
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": random.choice(user_agents)
        })
        
        self.driver.maximize_window()
    
    def login_to_amazon(self, email, password):
        """Login to Amazon with human-like behavior"""
        try:
            print("Starting login process...")
            
            # Navigate to Amazon
            self.driver.get("https://www.amazon.in/")
            time.sleep(random.uniform(3, 5))
            
            # Click on Sign In
            sign_in_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Hello, sign in']"))
            )
            sign_in_element.click()
            time.sleep(random.uniform(2, 4))
            
            # Enter email with human-like typing
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
            )
            email_field.clear()
            for char in email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(1, 2))
            
            # Click Continue
            continue_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            continue_button.click()
            time.sleep(random.uniform(2, 4))
            
            # Enter password with human-like typing
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            time.sleep(random.uniform(1, 2))
            
            # Click Sign In
            sign_in_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            sign_in_button.click()
            time.sleep(random.uniform(5, 8))
            
            print("Login successful!")
            return True
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def try_direct_navigation(self):
        """Try direct navigation to New Releases"""
        try:
            print("Trying direct navigation to New Releases...")
            self.driver.get("https://www.amazon.in/gp/new-releases/")
            time.sleep(random.uniform(10, 15))
            
            # Check if page loaded properly
            page_title = self.driver.title
            print(f"Page title: {page_title}")
            
            # Check page source length
            page_source = self.driver.page_source
            print(f"Page source length: {len(page_source)}")
            
            # If page seems blank, try to refresh and wait
            if len(page_source) < 5000:
                print("Page seems blank, refreshing...")
                self.driver.refresh()
                time.sleep(random.uniform(10, 15))
                page_source = self.driver.page_source
                print(f"After refresh - Page source length: {len(page_source)}")
            
            # Check for specific content
            if "Hot New Releases" in page_source or "New Releases" in page_source:
                print("Successfully found Hot New Releases content!")
                return True
            else:
                print("Hot New Releases content not found")
                return False
                
        except Exception as e:
            print(f"Error in direct navigation: {str(e)}")
            return False
    
    def try_alternative_urls(self):
        """Try alternative URLs for New Releases"""
        alternative_urls = [
            "https://www.amazon.in/gp/new-releases/ref=nav_em_cs_newreleases_0_1_1_3",
            "https://www.amazon.in/s?k=new+releases&ref=sr_pg_1",
            "https://www.amazon.in/gp/bestsellers/ref=nav_em_cs_bestsellers_0_1_1_3",
            "https://www.amazon.in/s?k=hot+new+releases&ref=sr_pg_1"
        ]
        
        for url in alternative_urls:
            try:
                print(f"Trying alternative URL: {url}")
                self.driver.get(url)
                time.sleep(random.uniform(8, 12))
                
                page_source = self.driver.page_source
                if len(page_source) > 5000 and ("Hot New Releases" in page_source or "New Releases" in page_source):
                    print(f"Successfully loaded page from: {url}")
                    return True
            except Exception as e:
                print(f"Failed to load {url}: {str(e)}")
                continue
        
        return False
    
    def try_menu_navigation(self):
        """Try navigating through the menu"""
        try:
            print("Trying menu navigation...")
            self.driver.get("https://www.amazon.in/")
            time.sleep(random.uniform(3, 5))
            
            # Click on category menu
            category_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='hm-icon-label'][1]"))
            )
            category_menu.click()
            time.sleep(random.uniform(2, 4))
            
            # Look for "All" category
            all_category = None
            all_locators = [
                "//a[@class='hmenu-item' and contains(text(), 'All')]",
                "//a[contains(text(), 'All')]",
                "//div[contains(text(), 'All')]"
            ]
            
            for locator in all_locators:
                try:
                    all_category = self.driver.find_element(By.XPATH, locator)
                    break
                except:
                    continue
            
            if all_category:
                all_category.click()
                time.sleep(random.uniform(2, 4))
            
            # Look for "New Releases"
            new_releases = None
            new_releases_locators = [
                "//a[@href='/gp/new-releases/?ref_=nav_em_cs_newreleases_0_1_1_3']",
                "//a[contains(@href, 'new-releases')]",
                "//a[contains(text(), 'New Releases')]"
            ]
            
            for locator in new_releases_locators:
                try:
                    new_releases = self.driver.find_element(By.XPATH, locator)
                    break
                except:
                    continue
            
            if new_releases:
                new_releases.click()
                time.sleep(random.uniform(8, 12))
                
                page_source = self.driver.page_source
                if len(page_source) > 5000 and ("Hot New Releases" in page_source or "New Releases" in page_source):
                    print("Successfully navigated via menu!")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Menu navigation failed: {str(e)}")
            return False
    
    def try_requests_bypass(self):
        """Try using requests library to bypass Selenium detection"""
        try:
            print("Trying requests library bypass...")
            
            # Get cookies from Selenium session
            cookies = self.driver.get_cookies()
            session = requests.Session()
            
            # Add cookies to session
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            
            # Set headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Try to get the page
            response = session.get('https://www.amazon.in/gp/new-releases/', headers=headers)
            
            if response.status_code == 200 and len(response.text) > 5000:
                print("Successfully got page content via requests!")
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Look for product containers
                product_containers = soup.find_all('div', class_='zg-item-immersion')
                if product_containers:
                    print(f"Found {len(product_containers)} product containers via requests!")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Requests bypass failed: {str(e)}")
            return False
    
    def navigate_to_hot_new_releases(self):
        """Navigate to Hot New Releases using multiple strategies"""
        strategies = [
            self.try_direct_navigation,
            self.try_alternative_urls,
            self.try_menu_navigation,
            self.try_requests_bypass
        ]
        
        for i, strategy in enumerate(strategies):
            print(f"\n=== Trying Strategy {i+1} ===")
            try:
                if strategy():
                    print(f"Strategy {i+1} succeeded!")
                    return True
            except Exception as e:
                print(f"Strategy {i+1} failed: {str(e)}")
                continue
        
        print("All strategies failed!")
        return False
    
    def get_category_name(self):
        """Get the current Hot New Releases category name"""
        try:
            # Try multiple locators for category name
            category_locators = [
                "//h2[contains(text(), 'Hot New Releases')]",
                "//h1[contains(text(), 'Hot New Releases')]",
                "//div[contains(text(), 'Hot New Releases')]",
                "//span[contains(text(), 'Hot New Releases')]",
                "//*[contains(text(), 'Hot New Releases')]"
            ]
            
            for locator in category_locators:
                try:
                    category_elements = self.driver.find_elements(By.XPATH, locator)
                    if category_elements:
                        category_name = category_elements[0].text.strip()
                        if category_name:
                            print(f"Current category: {category_name}")
                            return category_name
                except:
                    continue
            
            return "Hot New Releases - Unknown Category"
        except Exception as e:
            print(f"Error getting category name: {str(e)}")
            return "Hot New Releases - Unknown Category"
    
    def extract_products(self, max_products=5):
        """Extract product information with multiple strategies"""
        products = []
        
        try:
            print("Looking for product elements...")
            
            # Wait for page to load
            time.sleep(random.uniform(5, 8))
            
            # Scroll to load content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(2, 4))
            
            # Try multiple strategies to find products
            product_containers = []
            
            # Strategy 1: Primary locators
            primary_locators = [
                "//div[@class='zg-item-immersion']",
                "//div[contains(@class, 'zg-item')]",
                "//div[contains(@class, 'item')]",
                "//div[contains(@class, 'product')]"
            ]
            
            for locator in primary_locators:
                try:
                    containers = self.driver.find_elements(By.XPATH, locator)
                    if containers:
                        product_containers = containers
                        print(f"Found {len(containers)} product containers using: {locator}")
                        break
                except:
                    continue
            
            # Strategy 2: Look for product links
            if not product_containers:
                try:
                    product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
                    product_containers = product_links
                    print(f"Found {len(product_links)} product links")
                except:
                    pass
            
            # Strategy 3: Look for any elements with product-like content
            if not product_containers:
                try:
                    all_divs = self.driver.find_elements(By.XPATH, "//div")
                    potential_products = []
                    for div in all_divs:
                        text = div.text.lower()
                        if any(keyword in text for keyword in ['₹', '$', 'price', 'rating', 'stars', 'buy', 'add to cart']):
                            potential_products.append(div)
                    product_containers = potential_products
                    print(f"Found {len(potential_products)} potential product divs")
                except:
                    pass
            
            print(f"Total containers to process: {len(product_containers)}")
            
            # Extract products
            for i, container in enumerate(product_containers[:max_products]):
                try:
                    print(f"\n--- Processing Product {i+1} ---")
                    
                    # Extract title
                    title = self.get_product_title(container)
                    
                    # Extract price
                    price = self.get_product_price(container)
                    
                    # Extract rating
                    rating = self.get_product_rating(container)
                    
                    product_data = {
                        'ranking': len(products) + 1,
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Only add if we got meaningful data
                    if title != "No Title Available" or price != "Price Not Available":
                        products.append(product_data)
                        print(f"Added product {len(products)}: {title[:50]}...")
                    else:
                        print(f"Skipping product {i+1} - no meaningful data")
                    
                except Exception as e:
                    print(f"Error extracting product {i+1}: {str(e)}")
                    continue
            
            print(f"\nSuccessfully extracted {len(products)} products")
            return products
            
        except Exception as e:
            print(f"Error extracting products: {str(e)}")
            return products
    
    def get_product_title(self, container):
        """Extract product title from container"""
        title_selectors = [
            ".//span[@class='a-size-base-plus a-color-base a-text-normal']",
            ".//h2//span",
            ".//h3//span",
            ".//a[@class='a-link-normal']//span",
            ".//span[contains(@class, 'a-size')]",
            ".//a[contains(@class, 'a-link')]//span",
            ".//span[contains(@class, 'text')]",
            ".//div[contains(@class, 'title')]//span",
            ".//div[contains(@class, 'name')]//span"
        ]
        
        for selector in title_selectors:
            try:
                title_element = container.find_element(By.XPATH, selector)
                title = title_element.text.strip()
                if title and len(title) > 5:
                    return title
            except:
                continue
        
        # Fallback: get any meaningful text from the container
        try:
            all_text_elements = container.find_elements(By.XPATH, ".//span | .//a | .//h1 | .//h2 | .//h3 | .//div")
            for element in all_text_elements:
                text = element.text.strip()
                if text and len(text) > 10 and len(text) < 200:
                    return text
        except:
            pass
        
        return "No Title Available"
    
    def get_product_price(self, container):
        """Extract product price from container"""
        price_selectors = [
            ".//span[@class='a-price-whole']",
            ".//span[contains(@class, 'a-price')]//span[contains(@class, 'a-offscreen')]",
            ".//span[contains(@class, 'price')]",
            ".//span[contains(text(), '₹')]",
            ".//span[contains(text(), '$')]",
            ".//span[contains(@class, 'a-price-symbol')]/following-sibling::span"
        ]
        
        for selector in price_selectors:
            try:
                price_element = container.find_element(By.XPATH, selector)
                price = price_element.text.strip()
                if price and ('₹' in price or '$' in price):
                    return price
            except:
                continue
        
        return "Price Not Available"
    
    def get_product_rating(self, container):
        """Extract product rating from container"""
        rating_selectors = [
            ".//span[@class='a-icon-alt']",
            ".//span[contains(@class, 'a-icon-alt')]",
            ".//span[contains(@class, 'rating')]",
            ".//span[contains(text(), 'out of')]",
            ".//span[contains(text(), 'stars')]"
        ]
        
        for selector in rating_selectors:
            try:
                rating_element = container.find_element(By.XPATH, selector)
                rating = rating_element.text.strip()
                if rating and ('out of' in rating or 'stars' in rating):
                    return rating
            except:
                continue
        
        return "No Rating Available"
    
    def save_to_json(self, products, category_name):
        """Save products to JSON file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hot_new_releases_{self.sanitize_filename(category_name)}_{timestamp}.json"
            
            data = {
                'category': category_name,
                'extracted_at': timestamp,
                'total_products': len(products),
                'products': products
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Products saved to JSON file: {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving to JSON: {str(e)}")
            return None
    
    def save_to_csv(self, products, category_name):
        """Save products to CSV file (Excel compatible)"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hot_new_releases_{self.sanitize_filename(category_name)}_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ranking', 'title', 'price', 'rating', 'category', 'extracted_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for product in products:
                    product['category'] = category_name
                    product['extracted_at'] = timestamp
                    writer.writerow(product)
            
            print(f"Products saved to CSV file: {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            return None
    
    def sanitize_filename(self, filename):
        """Sanitize filename by removing/replacing invalid characters"""
        return re.sub(r'[<>:"/\\|?*]', '_', filename).replace(' ', '_')
    
    def run_extraction(self, email, password):
        """Run the complete extraction process"""
        try:
            print("Starting Amazon Bypass extraction...")
            
            # Login to Amazon
            if not self.login_to_amazon(email, password):
                print("Login failed!")
                return False
            
            # Navigate to Hot New Releases
            if not self.navigate_to_hot_new_releases():
                print("Navigation to Hot New Releases failed!")
                return False
            
            # Get category name
            category_name = self.get_category_name()
            
            # Extract products
            products = self.extract_products()
            
            if not products:
                print("No products extracted!")
                return False
            
            # Save to JSON
            json_file = self.save_to_json(products, category_name)
            
            # Save to CSV (Excel compatible)
            csv_file = self.save_to_csv(products, category_name)
            
            # Display results
            print("\n" + "="*50)
            print("EXTRACTION COMPLETED SUCCESSFULLY")
            print("="*50)
            print(f"Category: {category_name}")
            print(f"Products extracted: {len(products)}")
            print(f"JSON file: {json_file}")
            print(f"CSV file: {csv_file}")
            print("\nExtracted Products:")
            for product in products:
                print(f"  {product['ranking']}. {product['title'][:60]}...")
                print(f"     Price: {product['price']} | Rating: {product['rating']}")
            
            return True
            
        except Exception as e:
            print(f"Error in extraction process: {str(e)}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function to run the extraction"""
    extractor = None
    try:
        # Your Amazon credentials
        email = "aggarwalkhushi1721@gmail.com"
        password = "Asdfghjkl1@"
        
        # Create extractor instance
        extractor = AmazonBypassExtractor(headless=False)
        
        # Run extraction with authentication
        success = extractor.run_extraction(email, password)
        
        if success:
            print("\nExtraction completed successfully!")
        else:
            print("\nExtraction failed!")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")
    finally:
        if extractor:
            extractor.close()

if __name__ == "__main__":
    main()
