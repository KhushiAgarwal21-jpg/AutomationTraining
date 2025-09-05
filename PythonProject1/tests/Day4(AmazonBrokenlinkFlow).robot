*** Settings ***
Library    SeleniumLibrary
Resource    ../pageobjects/Resources/BrokenLink.resource

*** Test Cases ***
Broken Link Detection For Automation.com
    Open my browser for detecting broken link    ${siteUrl}    ${Browser}
    Go To Broken Links Page
    Click Broken Link
    Open my browser for detecting broken Image    ${siteUrl}    ${Browser}
    Go To Broken Images Page