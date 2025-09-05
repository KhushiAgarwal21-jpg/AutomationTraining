#!/usr/bin/env python3
"""
Fixed Hot New Releases Extractor for Robot Framework
Handles blank page issues and provides better debugging
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

class FixedHotNewReleasesExtractor:
    def __init__(self, headless=False):
        """Initialize the extractor with Chrome WebDriver"""
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options to prevent blank pages"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Add options to prevent blank pages
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Disable images and CSS to speed up loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.maximize_window()
    
    def login_to_amazon(self, email, password):
        """Login to Amazon with provided credentials"""
        try:
            print("Starting login process...")
            
            # Navigate to Amazon
            self.driver.get("https://www.amazon.in/")
            time.sleep(5)
            
            # Click on Sign In
            sign_in_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Hello, sign in']"))
            )
            sign_in_element.click()
            time.sleep(3)
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
            )
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(1)
            
            # Click Continue
            continue_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            continue_button.click()
            time.sleep(3)
            
            # Enter password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click Sign In
            sign_in_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
            sign_in_button.click()
            time.sleep(5)
            
            print("Login successful!")
            return True
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def navigate_to_hot_new_releases(self):
        """Navigate to Amazon's Hot New Releases section with blank page handling"""
        try:
            print("Navigating to Hot New Releases...")
            
            # Try direct navigation first
            self.driver.get("https://www.amazon.in/gp/new-releases/")
            time.sleep(10)  # Increased wait time
            
            # Check if page loaded properly
            page_title = self.driver.title
            print(f"Page title: {page_title}")
            
            # Wait for page to contain expected content
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Hot New Releases')]"))
                )
                print("Page contains 'Hot New Releases' text")
            except:
                print("Warning: 'Hot New Releases' text not found on page")
            
            # Scroll to load content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            
            # Check page source length
            page_source = self.driver.page_source
            print(f"Page source length: {len(page_source)}")
            
            # Take screenshot for debugging
            self.driver.save_screenshot("debug_new_releases_page.png")
            
            # If page seems blank, try refreshing
            if len(page_source) < 10000:  # Arbitrary threshold
                print("Page seems blank, refreshing...")
                self.driver.refresh()
                time.sleep(10)
            
            return True
            
        except Exception as e:
            print(f"Error navigating to Hot New Releases: {str(e)}")
            return False
    
    def get_category_name(self):
        """Get the current Hot New Releases category name"""
        try:
            # Try multiple locators for category name
            category_locators = [
                "//h2[contains(text(), 'Hot New Releases')]",
                "//h1[contains(text(), 'Hot New Releases')]",
                "//div[contains(text(), 'Hot New Releases')]",
                "//span[contains(text(), 'Hot New Releases')]"
            ]
            
            for locator in category_locators:
                try:
                    category_elements = self.driver.find_elements(By.XPATH, locator)
                    if category_elements:
                        category_name = category_elements[0].text
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
            time.sleep(5)
            
            # Try multiple strategies to find products
            product_containers = []
            
            # Strategy 1: Primary locator
            try:
                containers = self.driver.find_elements(By.XPATH, "//div[@class='zg-item-immersion']")
                product_containers = containers
                print(f"Found {len(containers)} product containers using primary locator")
            except:
                print("Primary locator failed, trying alternatives...")
                
                # Strategy 2: Alternative locators
                try:
                    containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'zg-item')]")
                    product_containers = containers
                    print(f"Found {len(containers)} product containers using alternative locator")
                except:
                    try:
                        containers = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'item')]")
                        product_containers = containers
                        print(f"Found {len(containers)} product containers using fallback locator")
                    except:
                        # Strategy 3: Look for product links
                        product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
                        product_containers = product_links
                        print(f"Found {len(product_links)} product links")
            
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
            ".//a[contains(@class, 'a-link')]//span"
        ]
        
        for selector in title_selectors:
            try:
                title_element = container.find_element(By.XPATH, selector)
                title = title_element.text.strip()
                if title and len(title) > 5:
                    return title
            except:
                continue
        
        return "No Title Available"
    
    def get_product_price(self, container):
        """Extract product price from container"""
        price_selectors = [
            ".//span[@class='a-price-whole']",
            ".//span[contains(@class, 'a-price')]//span[contains(@class, 'a-offscreen')]",
            ".//span[contains(@class, 'price')]",
            ".//span[contains(text(), '₹')]",
            ".//span[contains(text(), '$')]"
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
            print("Starting Fixed Hot New Releases extraction...")
            
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
        extractor = FixedHotNewReleasesExtractor(headless=False)
        
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
