from car_price.api import health


def test_health() -> None:
    assert health() == {"status": "ok"}
