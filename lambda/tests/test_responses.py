"""
Unit tests for shared.responses - API Gateway response utilities.

Tests:
- _resp() - Response formatting with CORS headers
- decimal_default() - Decimal serialization for JSON
"""
import json
import pytest
from decimal import Decimal
from shared.responses import _resp, decimal_default


class TestResponseFormatter:
    """Tests for _resp() function"""

    def test_resp_basic_structure(self):
        """_resp should return proper API Gateway response structure"""
        response = _resp(200, {"message": "success"})

        assert response["statusCode"] == 200
        assert "headers" in response
        assert "body" in response

    def test_resp_cors_headers(self):
        """_resp should include CORS headers"""
        response = _resp(200, {"message": "success"})

        headers = response["headers"]
        assert headers["Access-Control-Allow-Origin"] == "*"
        assert "GET,POST,DELETE,OPTIONS" in headers["Access-Control-Allow-Methods"]
        assert headers["Access-Control-Allow-Headers"] == "Content-Type"

    def test_resp_content_type(self):
        """_resp should set content-type to application/json"""
        response = _resp(200, {"message": "success"})

        assert response["headers"]["content-type"] == "application/json"

    def test_resp_body_serialization(self):
        """_resp should serialize body as JSON string"""
        body_dict = {"message": "success", "count": 42}
        response = _resp(200, body_dict)

        body = json.loads(response["body"])
        assert body["message"] == "success"
        assert body["count"] == 42

    def test_resp_different_status_codes(self):
        """_resp should handle different status codes"""
        responses = [
            _resp(200, {"message": "OK"}),
            _resp(201, {"message": "Created"}),
            _resp(400, {"error": "Bad Request"}),
            _resp(404, {"error": "Not Found"}),
            _resp(500, {"error": "Internal Error"}),
        ]

        assert responses[0]["statusCode"] == 200
        assert responses[1]["statusCode"] == 201
        assert responses[2]["statusCode"] == 400
        assert responses[3]["statusCode"] == 404
        assert responses[4]["statusCode"] == 500


class TestDecimalSerializer:
    """Tests for decimal_default() function"""

    def test_decimal_integer_conversion(self):
        """Decimal integers should convert to int"""
        result = decimal_default(Decimal("42"))
        assert result == 42
        assert isinstance(result, int)

    def test_decimal_float_conversion(self):
        """Decimal floats should convert to float"""
        result = decimal_default(Decimal("42.5"))
        assert result == 42.5
        assert isinstance(result, float)

    def test_decimal_zero_conversion(self):
        """Decimal zero should convert to int 0"""
        result = decimal_default(Decimal("0"))
        assert result == 0
        assert isinstance(result, int)

    def test_decimal_negative_integer(self):
        """Negative decimal integers should convert to int"""
        result = decimal_default(Decimal("-42"))
        assert result == -42
        assert isinstance(result, int)

    def test_decimal_negative_float(self):
        """Negative decimal floats should convert to float"""
        result = decimal_default(Decimal("-42.5"))
        assert result == -42.5
        assert isinstance(result, float)

    def test_non_decimal_raises_type_error(self):
        """Non-Decimal objects should raise TypeError"""
        with pytest.raises(TypeError):
            decimal_default("not a decimal")

        with pytest.raises(TypeError):
            decimal_default(42)

        with pytest.raises(TypeError):
            decimal_default([1, 2, 3])


class TestResponseWithDecimals:
    """Integration tests for _resp with Decimal values"""

    def test_resp_serializes_decimals(self):
        """_resp should serialize Decimal values in body"""
        body = {
            "price": Decimal("99.99"),
            "quantity": Decimal("5"),
            "total": Decimal("499.95"),
        }
        response = _resp(200, body)

        parsed_body = json.loads(response["body"])
        assert parsed_body["price"] == 99.99
        assert parsed_body["quantity"] == 5
        assert parsed_body["total"] == 499.95

    def test_resp_serializes_nested_decimals(self):
        """_resp should serialize nested Decimal values"""
        body = {
            "items": [
                {"price": Decimal("10.50"), "qty": Decimal("2")},
                {"price": Decimal("20.00"), "qty": Decimal("1")},
            ],
            "metadata": {"total": Decimal("41.00")},
        }
        response = _resp(200, body)

        parsed_body = json.loads(response["body"])
        assert parsed_body["items"][0]["price"] == 10.50
        assert parsed_body["items"][0]["qty"] == 2
        assert parsed_body["items"][1]["price"] == 20.00
        assert parsed_body["metadata"]["total"] == 41.00
