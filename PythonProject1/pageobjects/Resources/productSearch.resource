*** Settings ***

Library    SeleniumLibrary
Variables    ../locators/ProductSearch.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${searchItem}    siddhartha book

*** Keywords ***

Search Element
    [Arguments]    ${searchItem}
    Wait Until Element Is Visible    ${txt_searchBar}
    Click Element    ${txt_searchBar}
    Input Text    ${txt_searchBar}    ${searchItem}
    Press Keys    ${txt_searchBar}    ENTER

Verify Successful Search
    Wait Until Element Is Visible    ${txt_validateSearch}


