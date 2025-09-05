*** Settings ***

Library    SeleniumLibrary
Variables    ../locators/LoginPage.py

*** Variables ***
${Browser}    chrome
${siteUrl}    https://www.amazon.in/
${username}    aggarwalkhushi1721@gmail.com
${password}    Asdfghjkl1@

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

Verify Successful Login
    Wait Until Element Is Visible    ${txt_validate}