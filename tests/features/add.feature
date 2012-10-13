Feature: Add an user to the users collection

    Scenario: Add a new user
        Given I have the users collection
        And I have the "Jack" user
        When I add it to the collection
        Then the user should have an id

    Scenario: Add a new user with HTTP Basic Auth
        Given I have an authenticated session
        And I have the users collection
        And the collection is authenticated
        And I have the "Jack" user
        When I add it to the collection
        Then the user should have an id
