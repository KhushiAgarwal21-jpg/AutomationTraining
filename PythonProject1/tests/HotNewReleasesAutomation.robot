*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    OperatingSystem
Resource    ../pageobjects/Resources/HotNewRelease.resource

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${username}    aggarwalkhushi1721@gmail.com
${password}    Asdfghjkl1@

*** Test Cases ***
Hot New Releases Product Extraction Test
    [Documentation]    Complete automation flow to extract top 5 products from Hot New Releases
    [Tags]    HotNewReleases    ProductExtraction    JSON    Excel
    
    # Step 1: Open browser and navigate to Amazon
    Open my browser    ${siteUrl}    ${Browser}
    
    # Step 2: Login to Amazon
    User Login    ${username}    ${password}
    Verify Successful Login
    
    # Step 3: Navigate directly to New Releases (bypassing category menu)
    Log    Starting navigation to Hot New Releases section...
    Go To    https://www.amazon.in/gp/new-releases/
    Sleep    8s
    
    # Debug: Check if page loaded properly
    ${page_title}=    Get Title
    Log    Page title: ${page_title}
    
    # Wait for page to fully load
    Wait Until Page Contains    Hot New Releases    15s
    Log    Page contains 'Hot New Releases' text
    
    # Scroll to ensure content is loaded
    Execute JavaScript    window.scrollTo(0, document.body.scrollHeight/2)
    Sleep    3s
    
    # Check for any content on the page
    ${page_source}=    Get Source
    ${source_length}=    Get Length    ${page_source}
    Log    Page source length: ${source_length}
    
    # Take screenshot for debugging
    Capture Page Screenshot    debug_new_releases_page.png
    
    # Step 4: Get the dynamic category name
    ${category_name}=    Get Dynamic Category Name
    Log    Current Hot New Releases category: ${category_name}
    
    # Step 5: Debug - Check what elements are actually on the page
    Log    Debugging page elements...
    ${product_containers}=    Get WebElements    //div[@class='zg-item-immersion']
    Log    Found ${product_containers.__len__()} zg-item-immersion containers
    
    ${product_links}=    Get WebElements    //a[contains(@href, '/dp/')]
    Log    Found ${product_links.__len__()} product links
    
    ${all_divs}=    Get WebElements    //div
    Log    Found ${all_divs.__len__()} total divs
    
    # Look for any elements with price symbols
    ${price_elements}=    Get WebElements    //*[contains(text(), '₹')]
    Log    Found ${price_elements.__len__()} elements with ₹ symbol
    
    # Try to find any h1, h2, h3 elements to see page structure
    ${h2_elements}=    Get WebElements    //h2
    Log    Found ${h2_elements.__len__()} h2 elements
    FOR    ${element}    IN    @{h2_elements}
        ${text}=    Get Text    ${element}
        Log    H2 text: ${text}
    END
    
    # Step 6: Extract top 5 products
    Log    Extracting top 5 products from the category...
    ${products}=    Extract Top 5 Products
    Log    Successfully extracted ${products.__len__()} products
    
    # Step 6: Save products to JSON file
    Log    Saving products to JSON file...
    ${json_file}=    Save Products To JSON    ${products}    ${category_name}
    Log    JSON file created: ${json_file}
    
    # Step 7: Save products to Excel file
    Log    Saving products to Excel file...
    ${excel_file}=    Save Products To Excel    ${products}    ${category_name}
    Log    Excel file created: ${excel_file}
    
    # Step 8: Display extracted product information
    Log    \n=== EXTRACTED PRODUCTS ===
    FOR    ${index}    ${product}    IN ENUMERATE    @{products}
        ${rank}=    Evaluate    ${index} + 1
        Log    \nProduct ${rank}:
        Log    Title: ${product['title']}
        Log    Price: ${product['price']}
        Log    Rating: ${product['rating']}
        Log    Ranking: ${product['ranking']}
        Log    Extracted At: ${product['extracted_at']}
    END
    
    # Step 9: Verify files were created
    File Should Exist    ${json_file}
    File Should Exist    ${excel_file}
    
    Log    \n=== AUTOMATION COMPLETED SUCCESSFULLY ===
    Log    JSON file: ${json_file}
    Log    Excel file: ${excel_file}
    Log    Category: ${category_name}
    Log    Total products extracted: ${products.__len__()}
    
    # Step 10: Close browser
    Close Browser

*** Keywords ***
Verify Successful Login
    [Documentation]    Verifies that login was successful
    Wait Until Element Is Visible    ${txt_validate}    10s
    Element Should Be Visible    ${txt_validate}
    Log    Login successful - User authenticated
