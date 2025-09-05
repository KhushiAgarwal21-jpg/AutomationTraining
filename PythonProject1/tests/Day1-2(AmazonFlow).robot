*** Settings ***
Library    SeleniumLibrary
Resource    ../pageobjects/Resources/LoginKeywords.resource
Resource    ../pageobjects/Resources/productSearch.resource
Resource    ../pageobjects/Resources/PriceCollection.resource
Resource    ../pageobjects/Resources/CartPayment.resource

*** Test Cases ***
LoginTest For Amazon
    Open my browser    ${siteUrl}    ${Browser}
    User Login    ${username}    ${password}
    Verify Successful Login

Search a Book
    Search Element    ${searchItem}
    Verify Successful Search

Price Collection for a book
    Collect Price

Cart Payment for a book
    Add Product To Cart
    Proceed To Payment
    Close my browser



