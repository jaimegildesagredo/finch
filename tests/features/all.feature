Feature: Get all users from the collection

    Scenario: Get all users
        Given I have the users collection
        When I get all the users
        Then I should have a list of users
