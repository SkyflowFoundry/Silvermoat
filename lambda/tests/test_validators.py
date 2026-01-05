"""
Unit tests for shared.validators - input validation utilities.

Tests:
- convert_floats_to_decimal() - Float to Decimal conversion for DynamoDB
"""
import pytest
from decimal import Decimal
from shared.validators import convert_floats_to_decimal


class TestFloatToDecimalConversion:
    """Tests for convert_floats_to_decimal() function"""

    def test_convert_simple_float(self):
        """Single float should convert to Decimal"""
        result = convert_floats_to_decimal(3.14)
        assert isinstance(result, Decimal)
        assert result == Decimal("3.14")

    def test_convert_integer_unchanged(self):
        """Integers should pass through unchanged"""
        result = convert_floats_to_decimal(42)
        assert result == 42
        assert isinstance(result, int)

    def test_convert_string_unchanged(self):
        """Strings should pass through unchanged"""
        result = convert_floats_to_decimal("hello")
        assert result == "hello"
        assert isinstance(result, str)

    def test_convert_none_unchanged(self):
        """None should pass through unchanged"""
        result = convert_floats_to_decimal(None)
        assert result is None

    def test_convert_bool_unchanged(self):
        """Booleans should pass through unchanged"""
        result_true = convert_floats_to_decimal(True)
        result_false = convert_floats_to_decimal(False)
        assert result_true is True
        assert result_false is False

    def test_convert_dict_with_floats(self):
        """Dict with float values should convert floats to Decimal"""
        data = {
            "price": 99.99,
            "quantity": 5,
            "name": "Product",
        }
        result = convert_floats_to_decimal(data)

        assert isinstance(result["price"], Decimal)
        assert result["price"] == Decimal("99.99")
        assert result["quantity"] == 5
        assert result["name"] == "Product"

    def test_convert_nested_dict(self):
        """Nested dicts should convert all floats recursively"""
        data = {
            "customer": {
                "name": "John",
                "balance": 1250.50,
            },
            "order": {
                "total": 500.00,
                "tax": 45.00,
            },
        }
        result = convert_floats_to_decimal(data)

        assert isinstance(result["customer"]["balance"], Decimal)
        assert result["customer"]["balance"] == Decimal("1250.50")
        assert isinstance(result["order"]["total"], Decimal)
        assert isinstance(result["order"]["tax"], Decimal)

    def test_convert_list_with_floats(self):
        """List with float values should convert floats to Decimal"""
        data = [1.5, 2.5, 3.5]
        result = convert_floats_to_decimal(data)

        assert all(isinstance(x, Decimal) for x in result)
        assert result[0] == Decimal("1.5")
        assert result[1] == Decimal("2.5")
        assert result[2] == Decimal("3.5")

    def test_convert_list_with_mixed_types(self):
        """List with mixed types should convert only floats"""
        data = [1, 2.5, "three", None, True]
        result = convert_floats_to_decimal(data)

        assert result[0] == 1
        assert isinstance(result[1], Decimal)
        assert result[1] == Decimal("2.5")
        assert result[2] == "three"
        assert result[3] is None
        assert result[4] is True

    def test_convert_list_of_dicts(self):
        """List of dicts should convert floats recursively"""
        data = [
            {"price": 10.50, "name": "Item 1"},
            {"price": 20.00, "name": "Item 2"},
        ]
        result = convert_floats_to_decimal(data)

        assert isinstance(result[0]["price"], Decimal)
        assert isinstance(result[1]["price"], Decimal)
        assert result[0]["name"] == "Item 1"

    def test_convert_deeply_nested_structure(self):
        """Deeply nested structures should convert all floats"""
        data = {
            "level1": {
                "level2": {
                    "level3": [
                        {"value": 1.23},
                        {"value": 4.56},
                    ]
                }
            }
        }
        result = convert_floats_to_decimal(data)

        deep_value = result["level1"]["level2"]["level3"][0]["value"]
        assert isinstance(deep_value, Decimal)
        assert deep_value == Decimal("1.23")

    def test_convert_empty_dict(self):
        """Empty dict should return empty dict"""
        result = convert_floats_to_decimal({})
        assert result == {}

    def test_convert_empty_list(self):
        """Empty list should return empty list"""
        result = convert_floats_to_decimal([])
        assert result == []

    def test_convert_negative_floats(self):
        """Negative floats should convert correctly"""
        result = convert_floats_to_decimal(-99.99)
        assert isinstance(result, Decimal)
        assert result == Decimal("-99.99")

    def test_convert_zero_float(self):
        """Zero as float should convert to Decimal"""
        result = convert_floats_to_decimal(0.0)
        assert isinstance(result, Decimal)
        assert result == Decimal("0")
