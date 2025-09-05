# Hot New Releases Product Extractor

This automation script extracts the top 5 products from Amazon's "Hot New Releases" section and saves them to both JSON and Excel formats.

## Features

- **Dynamic Category Detection**: Automatically detects the current "Hot New Releases" category
- **Product Extraction**: Extracts product title, price, rating, and ranking
- **Dual Format Export**: Saves data in both JSON and Excel formats
- **Error Handling**: Robust error handling for different page layouts
- **Flexible Execution**: Can be run via Robot Framework or Python script

## Files Structure

```
PythonProject1/
├── pageobjects/
│   ├── locators/
│   │   └── HotNewRelease.py          # Updated locators for dynamic detection
│   └── Resources/
│       └── HotNewRelease.resource    # Enhanced keywords for product extraction
├── tests/
│   └── HotNewReleasesAutomation.robot # Main Robot Framework test cases
├── hot_new_releases_extractor.py     # Standalone Python script
├── requirements.txt                  # Python dependencies
└── README_HotNewReleases.md         # This file
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Chrome WebDriver** (automatically handled by webdriver-manager)

## Usage

### Option 1: Robot Framework (Recommended)

Run the Robot Framework test:

```bash
# Run the complete automation test
robot tests/HotNewReleasesAutomation.robot

# Run with specific tags
robot --include HotNewReleases tests/HotNewReleasesAutomation.robot
```

### Option 2: Python Script

Run the standalone Python script:

```bash
python hot_new_releases_extractor.py
```

## Output Files

The automation generates two types of output files:

### JSON Format
```json
{
  "category": "Hot New Releases in Home & Kitchen",
  "extracted_at": "20231215_143022",
  "total_products": 5,
  "products": [
    {
      "ranking": 1,
      "title": "Product Name",
      "price": "₹1,299",
      "rating": "4.5 out of 5 stars",
      "extracted_at": "2023-12-15 14:30:22"
    }
  ]
}
```

### Excel Format
| ranking | title | price | rating | category | extracted_at |
|---------|-------|-------|--------|----------|--------------|
| 1 | Product Name | ₹1,299 | 4.5 out of 5 stars | Hot New Releases in Home & Kitchen | 2023-12-15 14:30:22 |

## File Naming Convention

- **JSON**: `hot_new_releases_{category_name}_{timestamp}.json`
- **Excel**: `hot_new_releases_{category_name}_{timestamp}.xlsx`

Example: `hot_new_releases_Hot_New_Releases_in_Home_and_Kitchen_20231215_143022.json`

## Key Features

### Dynamic Category Detection
- Automatically detects the current "Hot New Releases" category
- Works with any category that appears on the page
- No hardcoded category names

### Robust Product Extraction
- Multiple locator strategies for different page layouts
- Fallback mechanisms for missing data
- Handles various product card formats

### Error Handling
- Graceful handling of missing elements
- Continues extraction even if some products fail
- Comprehensive logging

## Configuration

### Robot Framework Variables
```robot
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${username}    your_email@example.com
${password}    your_password
```

### Python Script Options
```python
# Create extractor with headless mode
extractor = HotNewReleasesExtractor(headless=True)

# Or with visible browser
extractor = HotNewReleasesExtractor(headless=False)
```

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**
   - The script automatically downloads and manages ChromeDriver
   - Ensure Chrome browser is installed

2. **Element Not Found**
   - Amazon's page structure may change
   - Check and update locators in `HotNewRelease.py`

3. **Login Issues**
   - Login is optional in the current implementation
   - Uncomment login section if required

4. **Empty Results**
   - Check if the page loaded completely
   - Verify the category is available
   - Check for any popups or overlays

### Debug Mode

For Robot Framework:
```bash
robot --loglevel DEBUG tests/HotNewReleasesAutomation.robot
```

For Python script, the console output provides detailed logging.

## Customization

### Extract More Products
Change the `max_products` parameter in the Python script or modify the loop in Robot Framework.

### Different Categories
The script automatically detects categories, but you can modify the navigation logic to target specific categories.

### Additional Data Fields
Add new extraction methods in the respective files to capture additional product information.

## Requirements

- Python 3.7+
- Chrome Browser
- Internet Connection
- Required Python packages (see requirements.txt)

## Notes

- The automation respects Amazon's robots.txt and rate limiting
- Use responsibly and in accordance with Amazon's terms of service
- The script includes delays to avoid being detected as a bot
- Results may vary based on Amazon's current page structure
