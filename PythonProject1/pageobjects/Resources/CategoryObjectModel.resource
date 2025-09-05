*** Settings ***
Library    SeleniumLibrary
Variables    ../locators/CategoryObjectModel.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/

*** Keywords ***
Open my browser
    [Arguments]    ${siteUrl}    ${Browser}
    Open Browser    ${siteUrl}    ${Browser}
    Maximize Browser Window

Open Category Menu
    Wait Until Element Is Visible    ${lnk_categoryMenu}
    Click Element    ${lnk_categoryMenu}

Navigate To Laptops
    Open Category Menu
    Wait Until Element Is Visible    ${lnk_electronics}    10s
    Scroll Element Into View    ${lnk_electronics}
    Click Element    ${lnk_electronics}
    Wait Until Element Is Visible    ${lnk_tablets}    10s
    Wait Until Element Is Enabled    ${lnk_tablets}
    Scroll Element Into View    ${lnk_tablets}
    Click Element    ${lnk_tablets}
    Sleep    1
    Title Should Be    Buy Android & iOS Tablets Online with Up to 60% at Amazon.in

Navigate To Mens Clothing
    Open Category Menu
    Wait Until Element Is Visible    ${lnk_fashion}    10s
    Scroll Element Into View    ${lnk_fashion}
    Click Element    ${lnk_fashion}
    Wait Until Element Is Visible    ${lnk_mensClothing}    10s
    Wait Until Element Is Enabled    ${lnk_mensClothing}
    Scroll Element Into View    ${lnk_mensClothing}
    Click Element    ${lnk_mensClothing}
    Sleep    1
    Title Should Be    Buy T-Shirts & Shirts for Men Online in India at Best Prices - Amazon.in

Navigate To Appliances
    Open Category Menu
         Wait Until Element Is Visible    ${lnk_appliances}    10s
         Scroll Element Into View    ${lnk_appliances}
         Click Element    ${lnk_appliances}
         Wait Until Element Is Visible    ${lnk_speakers}    10s
         Wait Until Element Is Enabled    ${lnk_speakers}
         Scroll Element Into View    ${lnk_speakers}
         Click Element    ${lnk_speakers}
         Sleep    1
         Title Should Be    Speakers: Buy Bluetooth Speaker Online at Best Price in India

#Close my browser
#    Close All Browsers
