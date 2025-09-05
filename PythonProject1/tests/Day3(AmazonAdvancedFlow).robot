*** Settings ***
Library    SeleniumLibrary
Resource    ../pageobjects/Resources/CategoryObjectModel.resource
Resource    ../pageobjects/Resources/BrandValidation.resource


*** Test Cases ***
Category Object Model test

    Open my browser    ${siteUrl}    ${Browser}
    Open Category Menu
    Navigate To Laptops
    Navigate To Mens Clothing
    Navigate To Appliances
    Close my browser

Brand Validation Test

    Open my browser    ${siteUrl}    ${Browser}
    Search Product    ${product}
    Select Casio Brand
    Select Titan Brand
    Validate Casio Brand In Results
    Validate Titan Brand In Results
    Unselect Casio Brand
    Unselect Titan Brand
    Select Fastrack Brand
    Validate Fastrack Brand In Results
    Close my browser


