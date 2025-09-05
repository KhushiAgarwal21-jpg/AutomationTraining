*** Settings ***

Library    SeleniumLibrary
Variables    ../locators/BrokenLink.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://practice-automation.com/

*** Keywords ***
Open my browser for detecting broken link
    [Arguments]    ${siteUrl}    ${Browser}
    Open Browser    ${siteUrl}    ${Browser}
    Maximize Browser Window
    Wait Until Page Contains Element    ${btn_brokenLinks}

Go To Broken Links Page
    Scroll Element Into View    ${btn_brokenLinks}
    Click Element    ${btn_brokenLinks}
    Wait Until Page Contains Element    ${lnk_broken}

Click Broken Link
    Click Element    ${lnk_broken}
    Wait Until Page Contains Element    ${validation_txt}
    Sleep    2s

Open my browser for detecting broken Image
    [Arguments]    ${siteUrl}    ${Browser}
    Open Browser    ${siteUrl}    ${Browser}
    Maximize Browser Window
    Wait Until Page Contains Element    ${btn_brokenImages}

Go To Broken Images Page
    Scroll Element Into View    ${btn_brokenImages}
    Click Element    ${btn_brokenImages}
    Wait Until Page Contains Element    ${img_broken}
    Sleep    2s
