*** Settings ***

Library    SeleniumLibrary
Variables    ../locators/PriceCollection.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/

*** Keywords ***

Collect Price
    Wait Until Element Is Visible    ${txt_firstProduct}
    ${price}=    Get Text    ${txt_firstProductPrice}
    Log To Console       The price of first product is: ${price}