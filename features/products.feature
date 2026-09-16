Feature: Product catalog administration
  As an eCommerce administrator
  I need a product catalog UI
  So that I can manage saleable products

  Background:
    Given the following products
      | name   | description   | price | available | category |
      | Hat    | Red fedora    | 59.95 | True      | CLOTHS   |
      | Shoes  | Blue shoes    | 120.50| False     | CLOTHS   |
      | Burger | Quarter pound | 5.99  | True      | FOOD     |

  Scenario: Create a Product
    When I create a product named "Hammer"
    Then the product list contains "Hammer"

  Scenario: Read a Product
    When I retrieve the product named "Hat"
    Then the retrieved product is named "Hat"

  Scenario: Update a Product
    When I rename the product "Hat" to "Cap"
    Then the product list contains "Cap"

  Scenario: Delete a Product
    When I delete the product named "Shoes"
    Then the product list does not contain "Shoes"

  Scenario: List all Products
    When I list all products
    Then I receive 3 products

  Scenario: List by Category
    When I list products in category "CLOTHS"
    Then I receive 2 products

  Scenario: Search by Availability
    When I list products with availability "True"
    Then I receive 2 products

  Scenario: Search by Name
    When I list products named "Hat"
    Then I receive 1 products
