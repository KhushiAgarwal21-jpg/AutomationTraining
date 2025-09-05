#!/usr/bin/env python3
"""
Debug script to capture Amazon page source and analyze the structure
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def login_to_amazon(driver, email, password):
    """Login to Amazon"""
    try:
        print("🔐 Logging into Amazon...")
        driver.get("https://www.amazon.in/ap/signin")
        
        # Wait for email field
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_field.send_keys(email)
        
        # Click continue
        continue_btn = driver.find_element(By.ID, "continue")
        continue_btn.click()
        
        # Wait for password field
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_field.send_keys(password)
        
        # Click sign in
        signin_btn = driver.find_element(By.ID, "signInSubmit")
        signin_btn.click()
        
        # Wait for login to complete
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        )
        print("✅ Successfully logged in!")
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def capture_page_source(driver, url, filename):
    """Capture page source and save to file"""
    try:
        print(f"🌐 Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(5)
        
        # Get page title
        page_title = driver.title
        print(f"📄 Page Title: {page_title}")
        
        # Get page source
        page_source = driver.page_source
        print(f"📝 Page source length: {len(page_source)} characters")
        
        # Save page source to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"💾 Page source saved to: {filename}")
        
        # Take screenshot
        screenshot_name = filename.replace('.html', '.png')
        driver.save_screenshot(screenshot_name)
        print(f"📸 Screenshot saved to: {screenshot_name}")
        
        return page_title, len(page_source)
        
    except Exception as e:
        print(f"❌ Error capturing page source: {e}")
        return None, 0

def analyze_page_structure(driver):
    """Analyze the page structure to find relevant elements"""
    try:
        print("\n🔍 Analyzing page structure...")
        
        # Check for various elements
        elements_to_check = [
            ("h1 elements", "//h1"),
            ("h2 elements", "//h2"),
            ("h3 elements", "//h3"),
            ("divs with 'zg' class", "//div[contains(@class, 'zg')]"),
            ("divs with 'item' class", "//div[contains(@class, 'item')]"),
            ("divs with 'product' class", "//div[contains(@class, 'product')]"),
            ("links with '/dp/'", "//a[contains(@href, '/dp/')]"),
            ("elements with 'Hot New Releases'", "//*[contains(text(), 'Hot New Releases')]"),
            ("elements with 'New Releases'", "//*[contains(text(), 'New Releases')]"),
            ("elements with currency symbol", "//*[contains(text(), '₹')]"),
            ("elements with 'out of'", "//*[contains(text(), 'out of')]"),
        ]
        
        analysis_results = {}
        
        for description, xpath in elements_to_check:
            try:
                elements = driver.find_elements(By.XPATH, xpath)
                count = len(elements)
                analysis_results[description] = count
                
                if count > 0 and count <= 10:  # Show text for small number of elements
                    print(f"  {description}: {count}")
                    for i, element in enumerate(elements[:5]):  # Show first 5
                        try:
                            text = element.text.strip()
                            if text and len(text) < 100:
                                print(f"    {i+1}: {text}")
                        except:
                            pass
                else:
                    print(f"  {description}: {count}")
                    
            except Exception as e:
                print(f"  {description}: Error - {e}")
                analysis_results[description] = f"Error: {e}"
        
        # Save analysis results
        with open('page_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        print(f"📊 Analysis results saved to: page_analysis.json")
        
        return analysis_results
        
    except Exception as e:
        print(f"❌ Error analyzing page structure: {e}")
        return {}

def main():
    """Main function"""
    print("🚀 Starting Amazon page source debug...")
    
    # Your Amazon credentials
    email = "khushi.aggarwal@outlook.com"
    password = "Khushi@123"
    
    driver = None
    try:
        # Setup driver
        driver = setup_driver()
        
        # Login
        if not login_to_amazon(driver, email, password):
            print("❌ Cannot proceed without login")
            return
        
        # Navigate to New Releases page
        new_releases_url = "https://www.amazon.in/gp/new-releases/"
        
        # Capture page source
        page_title, source_length = capture_page_source(
            driver, 
            new_releases_url, 
            "amazon_new_releases_page_source.html"
        )
        
        if source_length > 0:
            # Analyze page structure
            analysis = analyze_page_structure(driver)
            
            print(f"\n✅ Debug complete!")
            print(f"📄 Page title: {page_title}")
            print(f"📝 Source length: {source_length}")
            print(f"📊 Found {len(analysis)} element types")
            
        else:
            print("❌ Failed to capture page source")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("🔚 Browser closed")

if __name__ == "__main__":
    main()
