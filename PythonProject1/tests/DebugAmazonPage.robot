*** Settings ***
Library    SeleniumLibrary
Library    Collections
Resource    ../pageobjects/Resources/HotNewRelease.resource

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${username}    aggarwalkhushi1721@gmail.com
${password}    Asdfghjkl1@

*** Test Cases ***
Debug Amazon New Releases Page
    [Documentation]    Debug what's actually on the Amazon New Releases page
    [Tags]    Debug    NewReleases
    
    # Step 1: Open browser and navigate to Amazon
    Open my browser    ${siteUrl}    ${Browser}
    
    # Step 2: Login to Amazon
    User Login    ${username}    ${password}
    Verify Successful Login
    
    # Step 3: Navigate directly to New Releases
    Log    Starting navigation to Hot New Releases section...
    Go To    https://www.amazon.in/gp/new-releases/
    Sleep    10s
    
    # Debug: Check page details
    ${page_title}=    Get Title
    Log    Page title: ${page_title}
    
    ${current_url}=    Get Location
    Log    Current URL: ${current_url}
    
    ${page_source}=    Get Source
    ${source_length}=    Get Length    ${page_source}
    Log    Page source length: ${source_length}
    
    # Check for specific text
    ${contains_hot_new_releases}=    Run Keyword And Return Status    Page Should Contain    Hot New Releases
    Log    Page contains 'Hot New Releases': ${contains_hot_new_releases}
    
    ${contains_new_releases}=    Run Keyword And Return Status    Page Should Contain    New Releases
    Log    Page contains 'New Releases': ${contains_new_releases}
    
    # Look for any product links
    ${product_links}=    Get WebElements    //a[contains(@href, '/dp/')]
    Log    Found ${product_links.__len__()} product links
    
    # Look for any divs with product-like content
    ${all_divs}=    Get WebElements    //div
    Log    Found ${all_divs.__len__()} total divs
    
    # Look for specific product containers
    ${zg_containers}=    Get WebElements    //div[@class='zg-item-immersion']
    Log    Found ${zg_containers.__len__()} zg-item-immersion containers
    
    ${zg_containers_alt}=    Get WebElements    //div[contains(@class, 'zg-item')]
    Log    Found ${zg_containers_alt.__len__()} zg-item containers
    
    # Look for any elements with price symbols
    ${price_elements}=    Get WebElements    //*[contains(text(), '₹')]
    Log    Found ${price_elements.__len__()} elements with ₹ symbol
    
    # Look for any elements with rating text
    ${rating_elements}=    Get WebElements    //*[contains(text(), 'out of')]
    Log    Found ${rating_elements.__len__()} elements with 'out of' text
    
    # Take screenshot
    Capture Page Screenshot    debug_amazon_page.png
    
    # Try to find any h1, h2, h3 elements
    ${h1_elements}=    Get WebElements    //h1
    Log    Found ${h1_elements.__len__()} h1 elements
    FOR    ${element}    IN    @{h1_elements}
        ${text}=    Get Text    ${element}
        Log    H1 text: ${text}
    END
    
    ${h2_elements}=    Get WebElements    //h2
    Log    Found ${h2_elements.__len__()} h2 elements
    FOR    ${element}    IN    @{h2_elements}
        ${text}=    Get Text    ${element}
        Log    H2 text: ${text}
    END
    
    ${h3_elements}=    Get WebElements    //h3
    Log    Found ${h3_elements.__len__()} h3 elements
    FOR    ${element}    IN    @{h3_elements}
        ${text}=    Get Text    ${element}
        Log    H3 text: ${text}
    END
    
    # Close browser
    Close Browser
