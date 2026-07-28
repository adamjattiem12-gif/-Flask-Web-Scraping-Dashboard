from models.item import Item


def test_item_to_dict_contains_all_fields():
    item = Item(
        id=1,
        name="Test Product",
        price=19.99,
        price_display="$19.99",
        currency="USD",
        source="unit-test",
        market="Retail Goods",
        scraped_at="2026-01-01T00:00:00",
    )
    d = item.to_dict()
    assert d["id"] == 1
    assert d["name"] == "Test Product"
    assert d["price"] == 19.99
    assert d["extra"] == {}


def test_item_extra_defaults_to_empty_dict_not_shared_between_instances():
    item_a = Item(1, "A", 1.0, "$1.00", "USD", "src", "mkt", "ts")
    item_b = Item(2, "B", 2.0, "$2.00", "USD", "src", "mkt", "ts")
    item_a.extra["rating"] = 5
    assert item_b.extra == {}
