*** Settings ***
Library    SeleniumLibrary
Variables    ../locators/BrandValidation.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${product}    Watches

*** Keywords ***
#Open my browser
#    [Arguments]    ${siteUrl}    ${Browser}
#    Open Browser    ${siteUrl}    ${Browser}
#    Maximize Browser Window

Search Product
    [Arguments]    ${product}
    Wait Until Element Is Visible    ${txt_searchBar}
    Input Text    ${txt_searchBar}    ${product}
    Press Keys    ${txt_searchBar}    ENTER

Select Casio Brand
    Wait Until Element Is Visible    ${chk_casio}    10s
    Click Element    ${chk_casio}

Select Titan Brand
    Wait Until Element Is Visible    ${chk_titan}    10s
    Click Element    ${chk_titan}

Select Fastrack Brand
    Wait Until Element Is Visible    ${chk_fastrack}    10s
    Click Element    ${chk_fastrack}

Validate Casio Brand In Results
    Wait Until Element Is Visible    ${validate_casio}

Validate Titan Brand In Results
    Wait Until Element Is Visible    ${validate_titan}

Unselect Casio Brand
    Wait Until Element Is Visible    ${chk_casio}    10s
    Click Element    ${chk_casio}
    
Unselect Titan Brand
    Wait Until Element Is Visible    ${chk_titan}    10s
    Click Element    ${chk_titan}

Validate Fastrack Brand In Results
    Wait Until Element Is Visible    ${validate_fastrack}

Close my browser
    Close All Browsers


