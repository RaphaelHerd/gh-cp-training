Feature: Home page smoke
  As a tester I want to ensure the home page is available and main navigation exists

  @smoke @p0 @home
  Scenario: Home page loads and shows critical navigation links
    Given I open the home page
    Then the page title should contain "Test Site"
    And the left navigation should contain "Form 3 - Credit Card"
    And the left navigation should contain "Form 6 - Celsius/Fahrenheit"
