import pytest

from svd.enum_value import EnumeratedValue

enum_value_init_params = [
    ("foo", "We use the foo option", 0, 0),
    ("bar", "We use the bar option", "0x1", 1),
    ("bar", "We use the bar option", "0xf", 15),
    ("bar", "We use the bar option", "0xF", 15),
    ("bar", "We use the bar option", "0b1111", 15),
    ("bar", "We use the bar option", "0b1010", 0xA),
    ("bar", "We use the bar option", "#1010", 0xA),
    ("bar", "We use the bar option", "#101x", 0xA),
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


enum_value_from_dict_params = [
    (
        {"name": "B_0x1", "description": "dac_ch1_trg1", "value": "0x1"},
        EnumeratedValue(None, None, "B_0x1", "dac_ch1_trg1", "0x1", None),
    ),
]


@pytest.mark.parametrize("enum_dict, expected", enum_value_from_dict_params)
def test_enum_value_from_dict(enum_dict, expected):
    result = EnumeratedValue.from_dict(enum_dict)
    assert expected == result
