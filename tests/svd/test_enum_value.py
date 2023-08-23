import pytest

from svd.enum_value import EnumeratedValue

enum_value_init_params = [
    ("foo", "We use the foo option", 0, 0),
    ("bar", "We use the bar option", "0x1", 1),
    ("bar", "We use the bar option", "0xf", 15),
    ("bar", "We use the bar option", "0xF", 15),
]


@pytest.mark.parametrize(
    "name, description, value, expected_value", enum_value_init_params
)
def test_enum_value_init(name, description, value, expected_value):
    result = EnumeratedValue(None, None, name, description, value, None)
    assert result.derived_from is None
    assert result.parent is None
    assert result.name is name
    assert result.description is description
    assert result.value is expected_value
    assert result.is_default is None
