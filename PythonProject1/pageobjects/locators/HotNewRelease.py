#login page locators
txt_signIn = "//span[text()='Hello, sign in']"
txt_loginUsername = "//input[@name='email']"
txt_loginContinue ="//input[@type='submit']"
txt_loginPassword = "//input[@name='password']"
txt_passwordContinue = "//input[@type='submit']"
txt_validate ="//span[text()='Hello, Khushi']"

# Category Navigation Locators
lnk_categoryMenu = "//span[@class='hm-icon-label'][1]"

# All category navigation - Updated with multiple fallback locators
lnk_allCategory = "//a[@class='hmenu-item' and contains(text(), 'All')] | //a[contains(text(), 'All')] | //div[contains(text(), 'All')] | //span[contains(text(), 'All')]"

# New Release category
lnk_newRelease = "//a[@href='/gp/new-releases/?ref_=nav_em_cs_newreleases_0_1_1_3']"

# Dynamic Hot New Releases section locators - Updated based on actual HTML structure
hot_new_releases_section = "//h2[contains(text(), 'Hot New Releases in')]"
hot_new_releases_title = "//h2[contains(text(), 'Hot New Releases in')]"

# Product extraction locators - Updated based on actual Amazon structure
# Products are structured as: #1, #2, etc. followed by title, rating, price
product_container = "//div[contains(@class, 'zg-item-immersion')] | //div[contains(@class, 'zg-item')] | //div[contains(@class, 'item')] | //div[contains(@class, 'product')] | //div[contains(@class, 's-result-item')]"
product_title = ".//a[contains(@href, '/dp/')] | .//span[contains(@class, 'a-size')] | .//h2//span | .//h3//span | .//a[contains(@class, 'a-link')]//span"
product_price = ".//span[contains(text(), '₹')] | .//span[contains(text(), '$')] | .//span[contains(@class, 'a-price')] | .//span[contains(@class, 'price')]"
product_rating = ".//span[contains(text(), 'out of')] | .//span[contains(text(), 'stars')] | .//span[contains(@class, 'a-icon-alt')] | .//span[contains(@class, 'rating')]"
product_rank = ".//span[contains(text(), '#')] | .//span[contains(@class, 'badge')] | .//span[contains(@class, 'rank')]"

# Alternative locators for different product layouts
product_title_alt = ".//a[contains(@href, '/dp/')] | .//div[contains(@class, 'title')]//span | .//div[contains(@class, 'name')]//span"
product_price_alt = ".//span[contains(@class, 'a-price')]//span[contains(@class, 'a-offscreen')] | .//span[contains(@class, 'a-price-symbol')]/following-sibling::span"
product_rating_alt = ".//span[contains(@class, 'a-icon-alt')] | .//span[contains(@class, 'rating')] | .//span[contains(text(), 'out of')]"

# Section Category (keeping existing for backward compatibility)
Section_firstTitle = "//*[text()='Hot New Releases in Home & Kitchen']"
Section_secondTitle = "//*[text()='Hot New Releases in Musical Instruments'][1]"
Section_thirdTitle = "//*[text()='Hot New Releases in Home Improvement']"
Section_fourTitle = "//*[text()='Hot New Releases in Bags, Wallets and Luggage']"
Section_fiveTitle = "//*[text()='Hot New Releases in Health & Personal Care']"
Section_sixTitle = "//*[text()='Hot New Releases in Shoes & Handbags']"
