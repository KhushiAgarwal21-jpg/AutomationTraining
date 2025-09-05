#!/usr/bin/env python3
"""
Simple Working Extractor
Focuses on the core issue: getting actual product data from Amazon's New Releases page
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

class SimpleWorkingExtractor:
    def __init__(self, headless=False):
        """Initialize with basic setup"""
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with minimal options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Basic options only
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
    
    def login_to_amazon(self, email, password):
        """Login to Amazon"""
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
    
    def navigate_to_new_releases(self):
        """Navigate to New Releases page"""
        try:
            print("Navigating to New Releases...")
            
            # Try direct navigation first
            self.driver.get("https://www.amazon.in/gp/new-releases/")
            time.sleep(10)
            
            # Check if we're on the right page
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            
            if "new-releases" in current_url:
                print("Successfully navigated to New Releases page!")
                return True
            else:
                print("Direct navigation failed, trying menu navigation...")
                
                # Try menu navigation
                self.driver.get("https://www.amazon.in/")
                time.sleep(3)
                
                # Click on category menu
                category_menu = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='hm-icon-label'][1]"))
                )
                category_menu.click()
                time.sleep(3)
                
                # Click on "All" category
                all_category = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='hmenu-item' and contains(text(), 'All')]"))
                )
                all_category.click()
                time.sleep(2)
                
                # Click on "New Releases"
                new_releases = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='/gp/new-releases/?ref_=nav_em_cs_newreleases_0_1_1_3']"))
                )
                new_releases.click()
                time.sleep(5)
                
                print("Successfully navigated via menu!")
                return True
            
        except Exception as e:
            print(f"Error navigating to New Releases: {str(e)}")
            return False
    
    def debug_page_content(self):
        """Debug what's actually on the page"""
        try:
            print("\n=== PAGE DEBUG ===")
            
            # Get page title
            page_title = self.driver.title
            print(f"Page title: {page_title}")
            
            # Get current URL
            current_url = self.driver.current_url
            print(f"Current URL: {current_url}")
            
            # Get page source length
            page_source = self.driver.page_source
            print(f"Page source length: {len(page_source)}")
            
            # Check for specific text
            if "Hot New Releases" in page_source:
                print("✓ Found 'Hot New Releases' text in page source")
            else:
                print("✗ 'Hot New Releases' text NOT found in page source")
            
            if "New Releases" in page_source:
                print("✓ Found 'New Releases' text in page source")
            else:
                print("✗ 'New Releases' text NOT found in page source")
            
            # Look for any product-related elements
            product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
            print(f"Found {len(product_links)} product links")
            
            # Look for any divs with product-like content
            all_divs = self.driver.find_elements(By.XPATH, "//div")
            product_divs = []
            for div in all_divs:
                text = div.text.lower()
                if any(keyword in text for keyword in ['₹', '$', 'price', 'rating', 'stars']):
                    product_divs.append(div)
            print(f"Found {len(product_divs)} divs with product-like content")
            
            # Take screenshot
            self.driver.save_screenshot("debug_page_content.png")
            print("Screenshot saved as debug_page_content.png")
            
            print("=== END DEBUG ===\n")
            
        except Exception as e:
            print(f"Error in debug: {str(e)}")
    
    def get_category_name(self):
        """Get the current category name"""
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
        """Extract product information"""
        products = []
        
        try:
            print("Looking for product elements...")
            
            # Wait for page to load
            time.sleep(5)
            
            # Scroll to load content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            
            # Try to find product containers
            product_containers = []
            
            # Strategy 1: Look for product containers
            try:
                containers = self.driver.find_elements(By.XPATH, "//div[@class='zg-item-immersion']")
                if containers:
                    product_containers = containers
                    print(f"Found {len(containers)} product containers using zg-item-immersion")
                else:
                    print("No zg-item-immersion containers found")
            except:
                print("Error finding zg-item-immersion containers")
            
            # Strategy 2: Look for product links
            if not product_containers:
                try:
                    product_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
                    product_containers = product_links
                    print(f"Found {len(product_links)} product links")
                except:
                    print("Error finding product links")
            
            # Strategy 3: Look for any elements with product-like content
            if not product_containers:
                try:
                    all_divs = self.driver.find_elements(By.XPATH, "//div")
                    potential_products = []
                    for div in all_divs:
                        text = div.text.lower()
                        if any(keyword in text for keyword in ['₹', '$', 'price', 'rating', 'stars']):
                            potential_products.append(div)
                    product_containers = potential_products
                    print(f"Found {len(potential_products)} potential product divs")
                except:
                    print("Error finding potential product divs")
            
            print(f"Total containers to process: {len(product_containers)}")
            
            # Extract products
            for i, container in enumerate(product_containers[:max_products]):
                try:
                    print(f"\n--- Processing Product {i+1} ---")
                    
                    # Get all text from this container for debugging
                    container_text = container.text.strip()
                    print(f"Container text: {container_text[:200]}...")
                    
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
            print("Starting Simple Working extraction...")
            
            # Login to Amazon
            if not self.login_to_amazon(email, password):
                print("Login failed!")
                return False
            
            # Navigate to New Releases
            if not self.navigate_to_new_releases():
                print("Navigation to New Releases failed!")
                return False
            
            # Debug page content
            self.debug_page_content()
            
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
        extractor = SimpleWorkingExtractor(headless=False)
        
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
