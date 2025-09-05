#!/usr/bin/env python3
"""
Advanced Amazon Hot New Releases Extractor with Multiple Bypass Strategies
Uses multiple techniques to bypass anti-bot detection
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
from datetime import datetime
import random
import re
import requests
from bs4 import BeautifulSoup

class AdvancedAmazonExtractor:
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.products = []
        
    def setup_requests_session(self):
        """Setup requests session with proper headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
        
    def setup_driver_stealth(self):
        """Setup Chrome driver with maximum stealth"""
        print("🔧 Setting up stealth Chrome driver...")
        
        chrome_options = Options()
        
        # Remove automation indicators
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced stealth options
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        
        # Random user agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Window size
        chrome_options.add_argument("--window-size=1366,768")
        
        # Disable images for faster loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute stealth scripts
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        print("✅ Stealth Chrome driver setup complete")
        
    def human_like_delay(self, min_delay=1, max_delay=3):
        """Add human-like delays"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def login_to_amazon(self, email, password):
        """Login to Amazon with human-like behavior"""
        try:
            print("🔐 Logging into Amazon...")
            
            # Go to Amazon homepage first
            self.driver.get("https://www.amazon.in/")
            self.human_like_delay(2, 4)
            
            # Click on sign in
            sign_in_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Hello, sign in']"))
            )
            sign_in_element.click()
            self.human_like_delay(1, 2)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_field.clear()
            for char in email:
                email_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Click continue
            continue_btn = self.driver.find_element(By.ID, "continue")
            continue_btn.click()
            self.human_like_delay(1, 2)
            
            # Enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            # Click sign in
            signin_btn = self.driver.find_element(By.ID, "signInSubmit")
            signin_btn.click()
            
            # Wait for login to complete
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "nav-link-accountList"))
            )
            print("✅ Successfully logged in!")
            return True
            
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def navigate_with_multiple_strategies(self):
        """Try multiple navigation strategies"""
        strategies = [
            self.strategy_direct_navigation,
            self.strategy_menu_navigation,
            self.strategy_search_navigation,
            self.strategy_requests_fallback
        ]
        
        for i, strategy in enumerate(strategies, 1):
            print(f"🔄 Trying strategy {i}...")
            try:
                if strategy():
                    print(f"✅ Strategy {i} successful!")
                    return True
            except Exception as e:
                print(f"❌ Strategy {i} failed: {e}")
                continue
        
        print("❌ All navigation strategies failed")
        return False
    
    def strategy_direct_navigation(self):
        """Strategy 1: Direct navigation to new releases"""
        try:
            print("🌐 Direct navigation to new releases...")
            self.driver.get("https://www.amazon.in/gp/new-releases/")
            self.human_like_delay(5, 8)
            
            # Check if page loaded
            page_source = self.driver.page_source
            if "Hot New Releases" in page_source and len(page_source) > 10000:
                print("✅ Direct navigation successful")
                return True
            else:
                print("⚠️ Direct navigation - page too short or no content")
                return False
        except Exception as e:
            print(f"❌ Direct navigation failed: {e}")
            return False
    
    def strategy_menu_navigation(self):
        """Strategy 2: Navigate through menu"""
        try:
            print("🍔 Menu navigation...")
            self.driver.get("https://www.amazon.in/")
            self.human_like_delay(2, 3)
            
            # Click on All menu
            all_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='hm-icon-label'][1]"))
            )
            all_menu.click()
            self.human_like_delay(2, 3)
            
            # Click on New Releases
            new_releases = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'New Releases')]"))
            )
            new_releases.click()
            self.human_like_delay(5, 8)
            
            # Check if page loaded
            page_source = self.driver.page_source
            if "Hot New Releases" in page_source and len(page_source) > 10000:
                print("✅ Menu navigation successful")
                return True
            else:
                print("⚠️ Menu navigation - page too short or no content")
                return False
        except Exception as e:
            print(f"❌ Menu navigation failed: {e}")
            return False
    
    def strategy_search_navigation(self):
        """Strategy 3: Search for new releases"""
        try:
            print("🔍 Search navigation...")
            self.driver.get("https://www.amazon.in/")
            self.human_like_delay(2, 3)
            
            # Search for "new releases"
            search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
            search_box.clear()
            search_box.send_keys("new releases")
            search_box.submit()
            self.human_like_delay(3, 5)
            
            # Try to find new releases link
            new_releases_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/gp/new-releases/')]")
            new_releases_link.click()
            self.human_like_delay(5, 8)
            
            # Check if page loaded
            page_source = self.driver.page_source
            if "Hot New Releases" in page_source and len(page_source) > 10000:
                print("✅ Search navigation successful")
                return True
            else:
                print("⚠️ Search navigation - page too short or no content")
                return False
        except Exception as e:
            print(f"❌ Search navigation failed: {e}")
            return False
    
    def strategy_requests_fallback(self):
        """Strategy 4: Use requests as fallback"""
        try:
            print("🌐 Requests fallback...")
            self.setup_requests_session()
            
            # Get the page with requests
            response = self.session.get("https://www.amazon.in/gp/new-releases/")
            if response.status_code == 200 and "Hot New Releases" in response.text:
                print("✅ Requests fallback successful")
                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                return self.extract_products_from_soup(soup)
            else:
                print("⚠️ Requests fallback - no content")
                return False
        except Exception as e:
            print(f"❌ Requests fallback failed: {e}")
            return False
    
    def extract_products_from_soup(self, soup):
        """Extract products from BeautifulSoup object"""
        try:
            print("🛍️ Extracting products from HTML...")
            products = []
            
            # Find product links
            product_links = soup.find_all('a', href=re.compile(r'/dp/'))
            
            for i, link in enumerate(product_links[:5]):
                try:
                    product_data = {
                        'ranking': i + 1,
                        'title': link.get_text(strip=True)[:100] if link.get_text(strip=True) else 'No Title',
                        'price': 'Price Not Available',
                        'rating': 'No Rating Available',
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Try to find price in nearby elements
                    parent = link.parent
                    if parent:
                        price_text = parent.get_text()
                        price_match = re.search(r'₹[\d,]+\.?\d*', price_text)
                        if price_match:
                            product_data['price'] = price_match.group()
                    
                    products.append(product_data)
                    print(f"✅ Extracted product {i+1}: {product_data['title'][:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error extracting product {i+1}: {e}")
                    continue
            
            if products:
                self.products = products
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error extracting from soup: {e}")
            return False
    
    def extract_products_selenium(self):
        """Extract products using Selenium"""
        try:
            print("🛍️ Extracting products with Selenium...")
            products = []
            
            # Wait for page to load
            self.human_like_delay(3, 5)
            
            # Scroll to load content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            self.human_like_delay(2, 3)
            
            # Try multiple selectors
            selectors = [
                "//a[contains(@href, '/dp/')]",
                "//div[contains(@class, 'zg-item')]",
                "//div[contains(@class, 'item')]",
                "//div[contains(@class, 'product')]"
            ]
            
            product_elements = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        product_elements = elements[:10]
                        print(f"Found {len(elements)} elements with selector: {selector}")
                        break
                except:
                    continue
            
            if not product_elements:
                print("❌ No product elements found")
                return []
            
            # Extract data from elements
            for i, element in enumerate(product_elements[:5]):
                try:
                    product_data = {
                        'ranking': i + 1,
                        'title': 'No Title Available',
                        'price': 'Price Not Available',
                        'rating': 'No Rating Available',
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Get text from element
                    element_text = element.text.strip()
                    
                    # Extract title (longest meaningful text)
                    lines = element_text.split('\n')
                    title_candidates = []
                    for line in lines:
                        line = line.strip()
                        if len(line) > 20 and len(line) < 200 and '₹' not in line and 'out of' not in line:
                            title_candidates.append(line)
                    
                    if title_candidates:
                        product_data['title'] = max(title_candidates, key=len)
                    
                    # Extract price
                    price_match = re.search(r'₹[\d,]+\.?\d*', element_text)
                    if price_match:
                        product_data['price'] = price_match.group()
                    
                    # Extract rating
                    rating_match = re.search(r'\d+\.\d+ out of 5 stars', element_text)
                    if rating_match:
                        product_data['rating'] = rating_match.group()
                    
                    if product_data['title'] != 'No Title Available':
                        products.append(product_data)
                        print(f"✅ Extracted product {i+1}: {product_data['title'][:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error extracting product {i+1}: {e}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"❌ Error extracting products: {e}")
            return []
    
    def get_category_name(self):
        """Get category name from page"""
        try:
            print("🔍 Getting category name...")
            
            # Try multiple selectors
            selectors = [
                "//h2[contains(text(), 'Hot New Releases in')]",
                "//h1[contains(text(), 'Hot New Releases in')]",
                "//*[contains(text(), 'Hot New Releases in')]"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        text = element.text.strip()
                        if "Hot New Releases in" in text:
                            print(f"✅ Found category: {text}")
                            return text
                except:
                    continue
            
            print("⚠️ No category found, using default")
            return "Hot New Releases"
            
        except Exception as e:
            print(f"❌ Error getting category: {e}")
            return "Hot New Releases"
    
    def save_to_files(self, products, category_name):
        """Save products to JSON and CSV files"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_category = re.sub(r'[^\w\-_.]', '_', category_name)
            
            # Save JSON
            json_filename = f"hot_new_releases_{safe_category}_{timestamp}.json"
            json_data = {
                'category': category_name,
                'extracted_at': timestamp,
                'total_products': len(products),
                'products': products
            }
            
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            # Save CSV
            csv_filename = f"hot_new_releases_{safe_category}_{timestamp}.csv"
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ranking', 'title', 'price', 'rating', 'category', 'extracted_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in products:
                    product['category'] = category_name
                    writer.writerow(product)
            
            print(f"💾 Files saved:")
            print(f"   JSON: {json_filename}")
            print(f"   CSV: {csv_filename}")
            
            return json_filename, csv_filename
            
        except Exception as e:
            print(f"❌ Error saving files: {e}")
            return None, None
    
    def run_extraction(self, email, password):
        """Main extraction process"""
        try:
            print("🚀 Starting Advanced Amazon Hot New Releases extraction...")
            
            # Setup
            self.setup_driver_stealth()
            
            # Login
            if not self.login_to_amazon(email, password):
                print("❌ Cannot proceed without login")
                return False
            
            # Navigate with multiple strategies
            if not self.navigate_with_multiple_strategies():
                print("❌ All navigation strategies failed")
                return False
            
            # Get category name
            category_name = self.get_category_name()
            
            # Extract products
            if self.products:  # If we got products from requests fallback
                products = self.products
            else:
                products = self.extract_products_selenium()
            
            if not products:
                print("❌ No products extracted")
                return False
            
            # Save to files
            json_file, csv_file = self.save_to_files(products, category_name)
            
            # Display results
            print(f"\n🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
            print(f"📊 Category: {category_name}")
            print(f"🛍️ Products extracted: {len(products)}")
            print(f"📄 JSON file: {json_file}")
            print(f"📊 CSV file: {csv_file}")
            
            print(f"\n📋 EXTRACTED PRODUCTS:")
            for i, product in enumerate(products, 1):
                print(f"\n{i}. {product['title']}")
                print(f"   Price: {product['price']}")
                print(f"   Rating: {product['rating']}")
                print(f"   Ranking: {product['ranking']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                print("🔚 Browser closed")

def main():
    """Main function"""
    # Your Amazon credentials
    email = "aggarwalkhushi1721@gmail.com"
    password = "Asdfghjkl1@"
    
    extractor = AdvancedAmazonExtractor()
    success = extractor.run_extraction(email, password)
    
    if success:
        print("\n✅ All done! Check the generated JSON and CSV files.")
    else:
        print("\n❌ Extraction failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
