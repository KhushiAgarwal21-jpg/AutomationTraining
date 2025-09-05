#!/usr/bin/env python3
"""
Simple Amazon Hot New Releases Extractor
Uses a different approach to bypass blank page issues
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import re
from datetime import datetime
import time
import random

class SimpleAmazonExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.products = []
        
    def setup_session(self):
        """Setup requests session with proper headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }
        self.session.headers.update(headers)
        
    def get_page_content(self, url):
        """Get page content with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🌐 Fetching page (attempt {attempt + 1})...")
                
                # Add random delay
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(url, timeout=30)
                
                if response.status_code == 200:
                    print(f"✅ Page fetched successfully (length: {len(response.text)})")
                    return response.text
                else:
                    print(f"⚠️ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                    
        return None
    
    def extract_products_from_html(self, html_content):
        """Extract products from HTML content"""
        try:
            print("🛍️ Extracting products from HTML...")
            soup = BeautifulSoup(html_content, 'html.parser')
            products = []
            
            # Find category name
            category_name = "Hot New Releases"
            category_selectors = [
                'h2:contains("Hot New Releases in")',
                'h1:contains("Hot New Releases in")',
                '*:contains("Hot New Releases in")'
            ]
            
            for selector in category_selectors:
                try:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text(strip=True)
                        if "Hot New Releases in" in text:
                            category_name = text
                            print(f"✅ Found category: {category_name}")
                            break
                    if category_name != "Hot New Releases":
                        break
                except:
                    continue
            
            # Find product links
            product_links = soup.find_all('a', href=re.compile(r'/dp/'))
            print(f"Found {len(product_links)} product links")
            
            # Extract product data
            for i, link in enumerate(product_links[:5]):
                try:
                    product_data = {
                        'ranking': i + 1,
                        'title': 'No Title Available',
                        'price': 'Price Not Available',
                        'rating': 'No Rating Available',
                        'extracted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Get title from link text
                    title = link.get_text(strip=True)
                    if title and len(title) > 10 and len(title) < 200:
                        product_data['title'] = title
                    
                    # Look for price in nearby elements
                    parent = link.parent
                    if parent:
                        # Search in parent and siblings
                        search_elements = [parent] + list(parent.find_next_siblings()[:3])
                        for element in search_elements:
                            text = element.get_text()
                            price_match = re.search(r'₹[\d,]+\.?\d*', text)
                            if price_match:
                                product_data['price'] = price_match.group()
                                break
                            
                            rating_match = re.search(r'\d+\.\d+ out of 5 stars', text)
                            if rating_match:
                                product_data['rating'] = rating_match.group()
                    
                    if product_data['title'] != 'No Title Available':
                        products.append(product_data)
                        print(f"✅ Extracted product {i+1}: {product_data['title'][:50]}...")
                    
                except Exception as e:
                    print(f"❌ Error extracting product {i+1}: {e}")
                    continue
            
            return products, category_name
            
        except Exception as e:
            print(f"❌ Error extracting from HTML: {e}")
            return [], "Hot New Releases"
    
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
    
    def run_extraction(self):
        """Main extraction process"""
        try:
            print("🚀 Starting Simple Amazon Hot New Releases extraction...")
            
            # Setup session
            self.setup_session()
            
            # Try multiple URLs
            urls = [
                "https://www.amazon.in/gp/new-releases/",
                "https://www.amazon.in/gp/new-releases/?ref_=nav_em_cs_newreleases_0_1_1_3",
                "https://www.amazon.in/s?k=new+releases&ref=sr_pg_1"
            ]
            
            for i, url in enumerate(urls, 1):
                print(f"\n🔄 Trying URL {i}: {url}")
                
                html_content = self.get_page_content(url)
                if html_content and "Hot New Releases" in html_content:
                    print(f"✅ URL {i} successful!")
                    
                    # Extract products
                    products, category_name = self.extract_products_from_html(html_content)
                    
                    if products:
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
                    else:
                        print(f"⚠️ URL {i} - No products extracted")
                else:
                    print(f"❌ URL {i} - No content or blank page")
            
            print("❌ All URLs failed")
            return False
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

def main():
    """Main function"""
    extractor = SimpleAmazonExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n✅ All done! Check the generated JSON and CSV files.")
    else:
        print("\n❌ Extraction failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
