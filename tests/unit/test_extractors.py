import pytest
from src.utils.Extractors import extract_price, extract_health_flag, extract_channel_products

def test_extract_price_basic():
    text = "This product costs $10 or 500 birr."
    prices = extract_price(text)
    assert any(p in prices for p in [10, 500])

def test_extract_health_flag_true():
    text = "This is a health-related product for diabetes."
    assert extract_health_flag(text) is True

def test_extract_health_flag_false():
    text = "This is a regular product."
    assert extract_health_flag(text) is False

def test_extract_channel_products():
    text = "Aspirin and Paracetamol are available."
    channel = "test_channel"
    products = extract_channel_products(text, channel)
    assert isinstance(products, list) 