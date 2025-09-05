#!/usr/bin/env python3
"""
Robust Amazon Hot New Releases Extractor
Bypasses anti-bot detection and extracts product data
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

class AmazonHotReleasesExtractor:
    def __init__(self):
        self.driver = None
        self.products = []
        
    def setup_driver(self):
        """Setup Chrome driver with advanced anti-detection options"""
        print("🔧 Setting up Chrome driver with anti-detection measures...")
        
        chrome_options = Options()
        
        # Basic options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced anti-detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-default-apps")
        
        # User agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Chrome driver setup complete")
        
    def login_to_amazon(self, email, password):
        """Login to Amazon with provided credentials"""
        try:
            print("🔐 Logging into Amazon...")
            self.driver.get("https://www.amazon.in/ap/signin")
            
            # Wait for email field
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            email_field.clear()
            email_field.send_keys(email)
            
            # Click continue
            continue_btn = self.driver.find_element(By.ID, "continue")
            continue_btn.click()
            
            # Wait for password field
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_field.clear()
            password_field.send_keys(password)
            
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
    
    def navigate_to_new_releases(self):
        """Navigate to Amazon Hot New Releases page"""
        try:
            print("🌐 Navigating to Hot New Releases page...")
            
            # Try direct navigation first
            self.driver.get("https://www.amazon.in/gp/new-releases/")
            time.sleep(5)
            
            # Check if page loaded properly
            page_title = self.driver.title
            print(f"📄 Page title: {page_title}")
            
            # Wait for content to load
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Scroll to load content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            
            # Check for Hot New Releases content
            page_source = self.driver.page_source
            if "Hot New Releases" in page_source:
                print("✅ Successfully navigated to Hot New Releases page")
                return True
            else:
                print("⚠️ Page loaded but Hot New Releases content not found")
                return False
                
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def extract_category_name(self):
        """Extract the first available category name"""
        try:
            print("🔍 Extracting category name...")
            
            # Look for category headings
            category_selectors = [
                "//h2[contains(text(), 'Hot New Releases in')]",
                "//h1[contains(text(), 'Hot New Releases in')]",
                "//*[contains(text(), 'Hot New Releases in')]"
            ]
            
            for selector in category_selectors:
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
            print(f"❌ Error extracting category: {e}")
            return "Hot New Releases"
    
    def extract_products(self):
        """Extract top 5 products from the page"""
        try:
            print("🛍️ Extracting products...")
            products = []
            
            # Wait for page to fully load
            time.sleep(5)
            
            # Try multiple strategies to find products
            product_containers = []
            
            # Strategy 1: Look for product links
            try:
                product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
                print(f"Found {len(product_links)} product links")
                product_containers = product_links[:10]  # Take first 10
            except:
                print("No product links found")
            
            # Strategy 2: Look for product containers
            if not product_containers:
                try:
                    containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'zg-item')]")
                    print(f"Found {len(containers)} zg-item containers")
                    product_containers = containers[:10]
                except:
                    print("No zg-item containers found")
            
            # Strategy 3: Look for any divs that might contain products
            if not product_containers:
                try:
                    all_divs = self.driver.find_elements(By.XPATH, "//div")
                    # Filter divs that might contain product info
                    for div in all_divs[:50]:  # Check first 50 divs
                        try:
                            text = div.text.strip()
                            if len(text) > 20 and len(text) < 500 and ('₹' in text or 'out of' in text):
                                product_containers.append(div)
                                if len(product_containers) >= 10:
                                    break
                        except:
                            continue
                    print(f"Found {len(product_containers)} potential product containers")
                except:
                    print("No product containers found")
            
            # Extract product data
            for i, container in enumerate(product_containers[:5]):
                try:
                    product_data = self.extract_product_data(container, i + 1)
                    if product_data and product_data.get('title') != 'No Title Available':
                        products.append(product_data)
                        print(f"✅ Extracted product {i+1}: {product_data['title'][:50]}...")
                    else:
                        print(f"⚠️ Skipped product {i+1} - insufficient data")
                except Exception as e:
                    print(f"❌ Error extracting product {i+1}: {e}")
                    continue
            
            print(f"🎉 Successfully extracted {len(products)} products")
            return products
            
        except Exception as e:
            print(f"❌ Error extracting products: {e}")
            return []
    
    def extract_product_data(self, container, rank):
        """Extract data from a single product container"""
        try:
            product_data = {
                'ranking': rank,
                'title': 'No Title Available',
                'price': 'Price Not Available',
                'rating': 'No Rating Available',
                'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Get all text from container
            container_text = container.text.strip()
            
            # Extract title (longest meaningful text)
            lines = container_text.split('\n')
            title_candidates = []
            for line in lines:
                line = line.strip()
                if len(line) > 20 and len(line) < 200 and '₹' not in line and 'out of' not in line and '#' not in line:
                    title_candidates.append(line)
            
            if title_candidates:
                # Choose the longest candidate as title
                product_data['title'] = max(title_candidates, key=len)
            
            # Extract price
            price_pattern = r'₹[\d,]+\.?\d*'
            price_match = re.search(price_pattern, container_text)
            if price_match:
                product_data['price'] = price_match.group()
            
            # Extract rating
            rating_pattern = r'\d+\.\d+ out of 5 stars'
            rating_match = re.search(rating_pattern, container_text)
            if rating_match:
                product_data['rating'] = rating_match.group()
            
            return product_data
            
        except Exception as e:
            print(f"❌ Error extracting product data: {e}")
            return None
    
    def save_to_json(self, products, category_name):
        """Save products to JSON file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hot_new_releases_{category_name}_{timestamp}.json"
            filename = re.sub(r'[^\w\-_.]', '_', filename)
            
            data = {
                'category': category_name,
                'extracted_at': timestamp,
                'total_products': len(products),
                'products': products
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 JSON file saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return None
    
    def save_to_csv(self, products, category_name):
        """Save products to CSV file"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"hot_new_releases_{category_name}_{timestamp}.csv"
            filename = re.sub(r'[^\w\-_.]', '_', filename)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ranking', 'title', 'price', 'rating', 'category', 'extracted_at']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in products:
                    product['category'] = category_name
                    writer.writerow(product)
            
            print(f"💾 CSV file saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def run_extraction(self, email, password):
        """Main extraction process"""
        try:
            print("🚀 Starting Amazon Hot New Releases extraction...")
            
            # Setup driver
            self.setup_driver()
            
            # Login
            if not self.login_to_amazon(email, password):
                print("❌ Cannot proceed without login")
                return False
            
            # Navigate to new releases
            if not self.navigate_to_new_releases():
                print("❌ Cannot proceed without proper navigation")
                return False
            
            # Extract category name
            category_name = self.extract_category_name()
            
            # Extract products
            products = self.extract_products()
            
            if not products:
                print("❌ No products extracted")
                return False
            
            # Save to files
            json_file = self.save_to_json(products, category_name)
            csv_file = self.save_to_csv(products, category_name)
            
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
    
    extractor = AmazonHotReleasesExtractor()
    success = extractor.run_extraction(email, password)
    
    if success:
        print("\n✅ All done! Check the generated JSON and CSV files.")
    else:
        print("\n❌ Extraction failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
