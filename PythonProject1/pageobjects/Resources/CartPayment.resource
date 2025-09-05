*** Settings ***

Library    SeleniumLibrary
Variables    ../locators/CartPayment.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/

*** Keywords ***

Add Product To Cart
    Wait Until Element Is Visible    ${txt_firstProduct}
#    Click Element    ${txt_firstProduct}
    Wait Until Element Is Visible    ${btn_addToCart}
    Click Button    ${btn_addToCart}

Proceed To Payment
    Wait Until Element Is Visible    ${btn_cart}
    Click Element    ${btn_cart}
    Wait Until Element Is Visible    ${btn_proceedToBuy}
    Click Button    ${btn_proceedToBuy}
    Wait Until Element Is Visible    ${txt_addressPage}

Close my browser
    Close All Browsers
