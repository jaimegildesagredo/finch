Feature: Get an user from the collection

    Scenario: Get an user
        Given I have the users collection
        When I get the user "1"
        Then I should have the user

    Scenario: Get an user
        Given I have an authenticated session
        And I have the users collection
        And the collection is authenticated
        When I get the user "1"
        Then I should have the user
