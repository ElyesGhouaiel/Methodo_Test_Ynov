from unittest.mock import Mock, call

import pytest

from model_objects import Product, ProductUnit, SpecialOfferType, Offer, Discount
from shopping_cart import ShoppingCart
from tests.fake_catalog import FakeCatalog


def test_handle_three_for_two_offer():
    # ARRANGE
    cart = ShoppingCart()
    product = Product("toothbrush", ProductUnit.EACH)
    cart.add_item_quantity(product, 3)

    catalog = FakeCatalog()
    catalog.add_product(product, 0.99)

    offers = {product: Offer(SpecialOfferType.THREE_FOR_TWO, product, 0)}

    receipt = Mock()
    
    # ACT
    cart.handle_offers(receipt, offers, catalog)

    # ASSERT
    expected_discount = Discount(product, "3 for 2", -0.99)
    receipt.add_discount.assert_called_once_with(expected_discount)


def test_handle_two_for_amount_offer():
    # ARRANGE
    cart = ShoppingCart()
    product = Product("shampoo", ProductUnit.EACH)
    cart.add_item_quantity(product, 2)

    catalog = FakeCatalog()
    catalog.add_product(product, 2.50)  # 2 for 4.00

    offers = {product: Offer(SpecialOfferType.TWO_FOR_AMOUNT, product, 4.00)}

    receipt = Mock()

    # ACT
    cart.handle_offers(receipt, offers, catalog)

    # ASSERT
    # 2 * 2.50 = 5.00. Offer is 2 for 4.00. Discount is 1.00
    expected_discount = Discount(product, "2 for 4.0", -1.00)
    receipt.add_discount.assert_called_once_with(expected_discount)


def test_handle_five_for_amount_offer():
    # ARRANGE
    cart = ShoppingCart()
    product = Product("soda", ProductUnit.EACH)
    cart.add_item_quantity(product, 5)

    catalog = FakeCatalog()
    catalog.add_product(product, 1.50)  # 5 for 5.00

    offers = {product: Offer(SpecialOfferType.FIVE_FOR_AMOUNT, product, 5.00)}

    receipt = Mock()

    # ACT
    cart.handle_offers(receipt, offers, catalog)

    # ASSERT
    # 5 * 1.50 = 7.50. Offer is 5 for 5.00. Discount is 2.50
    expected_discount = Discount(product, "5 for 5.0", -2.50)
    receipt.add_discount.assert_called_once_with(expected_discount)


def test_handle_ten_percent_discount_offer():
    # ARRANGE
    cart = ShoppingCart()
    product = Product("orange juice", ProductUnit.EACH)
    cart.add_item_quantity(product, 2)

    catalog = FakeCatalog()
    catalog.add_product(product, 3.00)  # 10% off

    offers = {product: Offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product, 10.0)}

    receipt = Mock()

    # ACT
    cart.handle_offers(receipt, offers, catalog)

    # ASSERT
    # 2 * 3.00 = 6.00. 10% discount is 0.60
    expected_discount = Discount(product, "10.0% off", -0.60)
    receipt.add_discount.assert_called_once_with(expected_discount) 