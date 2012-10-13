Feature: Add an user to the users collection

    Scenario: Add a new user
        Given I have the "Jack" user
        When I add it to the collection
        Then the user should have an id
