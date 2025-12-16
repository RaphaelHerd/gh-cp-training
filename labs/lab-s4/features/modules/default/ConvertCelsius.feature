Feature: Convert Celsius Feature
  Description: The purpose of this feature is to illustrate the usage of inline variables

  @inlineVars 
  Scenario: Convert Celsius to correct Fahrenheit middle range equivalent
    Given I provide "30" degree Celsius
    When I click the convert button
    Then I should see as result "86" Fahrenheit

  @inlineVars 
  Scenario: Convert Celsius to correct Fahrenheit high range equivalent
    Given I provide "35" degree Celsius
    When I click the convert button
    Then I should see as result "95" Fahrenheit