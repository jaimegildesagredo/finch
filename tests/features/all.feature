Feature: Get all users from the collection

    Scenario: Get all users
        Given I have the users collection
        When I get all the users
        Then I should have a list of users

    Scenario: Get all users with HTTP Basic Auth
        Given I have an authenticated session
        And I have the users collection
        And the collection is authenticated
        When I get all the users
        Then I should have a list of users
