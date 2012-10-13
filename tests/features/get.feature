Feature: Get an user from the collection

    Scenario: Get an user
        Given I have the users collection
        When I get the user "1"
        Then I should have the user
