*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String
Library    DateTime
Library    Process
Variables    ../locators/HotNewRelease.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${username}
${password}

*** Keywords ***
Open my browser
    [Arguments]    ${siteUrl}    ${Browser}
    Open Browser    ${siteUrl}    ${Browser}
    Maximize Browser Window

User Login
    [Arguments]    ${username}    ${password}
    Wait Until Element Is Visible    ${txt_signIn}
    Click Element    ${txt_signIn}
    Wait Until Element Is Visible    ${txt_loginUsername}
    Input Text    ${txt_loginUsername}    ${username}
    Click Button    ${txt_loginContinue}
    Wait Until Element Is Visible    ${txt_loginPassword}
    Input Text    ${txt_loginPassword}    ${password}
    Click Button    ${txt_passwordContinue}

Open Category Menu
    Wait Until Element Is Visible    ${lnk_categoryMenu}
    Click Element    ${lnk_categoryMenu}

Navigate To All Category
    Open Category Menu
    Sleep    3s
    # Try multiple approaches to find and click "All" category
    ${all_found}=    Set Variable    False
    TRY
        Wait Until Element Is Visible    ${lnk_allCategory}    5s
        Click Element    ${lnk_allCategory}
        ${all_found}=    Set Variable    True
        Log    Found and clicked All category using primary locator
    EXCEPT
        TRY
            # Try alternative approach - look for any element containing "All"
            ${all_elements}=    Get WebElements    //*[contains(text(), 'All')]
            FOR    ${element}    IN    @{all_elements}
                ${text}=    Get Text    ${element}
                IF    'All' in '${text}' and 'Categories' not in '${text}'
                    Click Element    ${element}
                    ${all_found}=    Set Variable    True
                    Log    Found and clicked All category using alternative approach: ${text}
                    Exit For Loop
                END
            END
        EXCEPT
            Log    Could not find All category, trying direct navigation
            # Skip All category and go directly to New Releases
            ${all_found}=    Set Variable    True
        END
    END
    Sleep    2s

Navigate To New Release
    # Try multiple approaches to find and click New Releases
    ${new_release_found}=    Set Variable    False
    TRY
        Wait Until Element Is Visible    ${lnk_newRelease}    5s
    Click Element    ${lnk_newRelease}
        ${new_release_found}=    Set Variable    True
        Log    Found and clicked New Releases using primary locator
    EXCEPT
        TRY
            # Try alternative approach - look for any element containing "New Releases"
            ${new_release_elements}=    Get WebElements    //*[contains(text(), 'New Releases')]
            FOR    ${element}    IN    @{new_release_elements}
                ${text}=    Get Text    ${element}
                IF    'New Releases' in '${text}'
                    Click Element    ${element}
                    ${new_release_found}=    Set Variable    True
                    Log    Found and clicked New Releases using alternative approach: ${text}
                    Exit For Loop
                END
            END
        EXCEPT
            Log    Could not find New Releases link, trying direct navigation
            # Try direct navigation to new releases page
            Go To    https://www.amazon.in/gp/new-releases/
            ${new_release_found}=    Set Variable    True
        END
    END
    
    # Wait for page to load
    Sleep    5s
    
    # Verify we're on the right page
    TRY
        Wait Until Element Is Visible    ${hot_new_releases_title}    10s
        Log    Successfully navigated to Hot New Releases page
    EXCEPT
        Log    Hot New Releases title not found, but continuing...
    END

Get Dynamic Category Name
    [Documentation]    Gets the first available Hot New Releases category name
    ${category_name}=    Set Variable    Unknown Category
    TRY
        ${category_elements}=    Get WebElements    ${hot_new_releases_title}
        FOR    ${element}    IN    @{category_elements}
            ${text}=    Get Text    ${element}
            IF    'Hot New Releases in' in '${text}'
                ${category_name}=    Set Variable    ${text}
                Exit For Loop
            END
        END
    EXCEPT
        Log    Could not find category using primary locator, trying alternatives...
        TRY
            ${category_elements}=    Get WebElements    //h2[contains(text(), 'Hot New Releases')]
            FOR    ${element}    IN    @{category_elements}
                ${text}=    Get Text    ${element}
                IF    'Hot New Releases' in '${text}'
                    ${category_name}=    Set Variable    ${text}
                    Exit For Loop
                END
            END
        EXCEPT
            Log    Could not find any category name
        END
    END
    Log    Found category: ${category_name}
    RETURN    ${category_name}

Extract Top 5 Products
    [Documentation]    Extracts top 5 products from the current Hot New Releases section
    ${products}=    Create List
    ${count}=    Set Variable    0
    
    # Wait for page to load completely
    Sleep    5s
    
    # Try multiple strategies to find products based on actual HTML structure
    ${product_containers}=    Create List
    
    # Strategy 1: Look for product links with /dp/ (most reliable)
    TRY
        ${product_links}=    Get WebElements    //a[contains(@href, '/dp/')]
        Log    Found ${product_links.__len__()} product links with /dp/
        ${product_containers}=    Set Variable    ${product_links}
    EXCEPT
        Log    No product links found, trying alternative approaches...
        
        # Strategy 2: Try zg-item-immersion containers
        TRY
            ${containers}=    Get WebElements    //div[contains(@class, 'zg-item-immersion')]
            Log    Found ${containers.__len__()} zg-item-immersion containers
            ${product_containers}=    Set Variable    ${containers}
        EXCEPT
            # Strategy 3: Try other container types
            TRY
                ${containers}=    Get WebElements    //div[contains(@class, 'zg-item')]
                Log    Found ${containers.__len__()} zg-item containers
                ${product_containers}=    Set Variable    ${containers}
            EXCEPT
                TRY
                    ${containers}=    Get WebElements    //div[contains(@class, 'item')]
                    Log    Found ${containers.__len__()} item containers
                    ${product_containers}=    Set Variable    ${containers}
                EXCEPT
                    Log    No product containers found with any locator
                END
            END
        END
    END
    
    Log    Total containers to process: ${product_containers.__len__()}
    
    FOR    ${container}    IN    @{product_containers}
        Exit For Loop If    ${count} >= 5
        
        ${product_data}=    Create Dictionary
        ${rank}=    Evaluate    ${count} + 1
        
        # Extract product title
        ${title}=    Get Product Title    ${container}
        Set To Dictionary    ${product_data}    title    ${title}
        
        # Extract product price
        ${price}=    Get Product Price    ${container}
        Set To Dictionary    ${product_data}    price    ${price}
        
        # Extract product rating
        ${rating}=    Get Product Rating    ${container}
        Set To Dictionary    ${product_data}    rating    ${rating}
        
        # Set ranking
        Set To Dictionary    ${product_data}    ranking    ${rank}
        
        # Add timestamp
        ${timestamp}=    Get Current Date    result_format=%Y-%m-%d %H:%M:%S
        Set To Dictionary    ${product_data}    extracted_at    ${timestamp}
        
        # Only add if we got meaningful data
        IF    '${title}' != 'No Title Available' and len('${title}') > 10
            Append To List    ${products}    ${product_data}
            Log    Added product ${rank}: ${title}
        ELSE
            Log    Skipping product ${rank} - no meaningful data (title: ${title})
        END
        
        ${count}=    Evaluate    ${count} + 1
    END
    
    Log    Successfully extracted ${products.__len__()} products
    RETURN    ${products}

Get Product Title
    [Arguments]    ${container}
    ${title}=    Set Variable    No Title Available
    TRY
        # First try to get text from the container itself (for links)
        ${container_text}=    Get Text    ${container}
        ${container_text}=    Strip String    ${container_text}
        IF    len('${container_text}') > 10 and len('${container_text}') < 200
            ${title}=    Set Variable    ${container_text}
        ELSE
            # Try specific locators
            TRY
                ${title_element}=    Get WebElement    ${container}${product_title}
                ${title}=    Get Text    ${title_element}
                ${title}=    Strip String    ${title}
            EXCEPT
                TRY
                    ${title_element}=    Get WebElement    ${container}${product_title_alt}
                    ${title}=    Get Text    ${title_element}
                    ${title}=    Strip String    ${title}
                EXCEPT
                    # Fallback: get any meaningful text from the container
                    TRY
                        ${all_text_elements}=    Get WebElements    ${container}.//span | ${container}.//a | ${container}.//h1 | ${container}.//h2 | ${container}.//h3 | ${container}.//div
                        FOR    ${element}    IN    @{all_text_elements}
                            ${text}=    Get Text    ${element}
                            ${text}=    Strip String    ${text}
                            IF    '${text}' != '' and len('${text}') > 10 and len('${text}') < 200 and '₹' not in '${text}' and 'out of' not in '${text}'
                                ${title}=    Set Variable    ${text}
                                Exit For Loop
                            END
                        END
                    EXCEPT
                        ${title}=    Set Variable    No Title Available
                    END
                END
            END
        END
    EXCEPT
        ${title}=    Set Variable    No Title Available
    END
    RETURN    ${title}

Get Product Price
    [Arguments]    ${container}
    ${price}=    Set Variable    Price Not Available
    TRY
        # Look for any text that contains currency symbols
        ${all_text_elements}=    Get WebElements    ${container}.//span | ${container}.//div | ${container}.//a
        FOR    ${element}    IN    @{all_text_elements}
            ${text}=    Get Text    ${element}
            ${text}=    Strip String    ${text}
            IF    '₹' in '${text}' and len('${text}') < 20 and len('${text}') > 3
                ${price}=    Set Variable    ${text}
                Exit For Loop
            END
        END
    EXCEPT
        ${price}=    Set Variable    Price Not Available
    END
    RETURN    ${price}

Get Product Rating
    [Arguments]    ${container}
    ${rating}=    Set Variable    No Rating Available
    TRY
        # Look for any text that contains rating indicators
        ${all_text_elements}=    Get WebElements    ${container}.//span | ${container}.//div | ${container}.//a
        FOR    ${element}    IN    @{all_text_elements}
            ${text}=    Get Text    ${element}
            ${text}=    Strip String    ${text}
            IF    'out of' in '${text}' and len('${text}') < 50 and len('${text}') > 5
                ${rating}=    Set Variable    ${text}
                Exit For Loop
            END
        END
    EXCEPT
        ${rating}=    Set Variable    No Rating Available
    END
    RETURN    ${rating}

Save Products To JSON
    [Arguments]    ${products}    ${category_name}
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${filename}=    Set Variable    hot_new_releases_${category_name}_${timestamp}.json
    ${filename}=    Replace String    ${filename}    ${SPACE}    _
    ${filename}=    Replace String    ${filename}    &    and
    ${filename}=    Replace String    ${filename}    ,    _
    ${filename}=    Replace String    ${filename}    :    _
    
    ${json_data}=    Create Dictionary
    Set To Dictionary    ${json_data}    category    ${category_name}
    Set To Dictionary    ${json_data}    extracted_at    ${timestamp}
    Set To Dictionary    ${json_data}    total_products    ${products.__len__()}
    Set To Dictionary    ${json_data}    products    ${products}
    
    ${json_string}=    Evaluate    json.dumps(${json_data}, indent=2)    json
    Run Process    python    file_writer.py    json    ${filename}    ${json_string}
    Log    Products saved to JSON file: ${filename}
    RETURN    ${filename}

Save Products To Excel
    [Arguments]    ${products}    ${category_name}
    ${timestamp}=    Get Current Date    result_format=%Y%m%d_%H%M%S
    ${filename}=    Set Variable    hot_new_releases_${category_name}_${timestamp}.csv
    ${filename}=    Replace String    ${filename}    ${SPACE}    _
    ${filename}=    Replace String    ${filename}    &    and
    ${filename}=    Replace String    ${filename}    ,    _
    ${filename}=    Replace String    ${filename}    :    _
    
    # Create CSV file using Python script
    ${products_json}=    Evaluate    json.dumps(${products})    json
    Run Process    python    file_writer.py    csv    ${filename}    ${products_json}    ${category_name}    ${timestamp}
    Log    Products saved to CSV file: ${filename}
    RETURN    ${filename}

Complete Hot New Releases Flow
    [Documentation]    Complete automation flow: Navigate to All -> New Releases -> Extract products -> Save to JSON and Excel
    Navigate To All Category
    Navigate To New Release
    ${category_name}=    Get Dynamic Category Name
    Log    Current category: ${category_name}
    ${products}=    Extract Top 5 Products
    Log    Extracted ${products.__len__()} products
    ${json_file}=    Save Products To JSON    ${products}    ${category_name}
    ${excel_file}=    Save Products To Excel    ${products}    ${category_name}
    RETURN    ${json_file}    ${excel_file}