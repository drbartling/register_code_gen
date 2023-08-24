import pytest

from svd.basic_elements import Usage
from svd.enum_value import EnumeratedValue, EnumeratedValues


def test_enumerated_values_from_dict():
    enums_dict = {
        "name": "DMAEN1",
        "enumeratedValue": [
            {
                "name": "B_0x0",
                "description": "DAC channel1 DMA mode disabled",
                "value": "0x0",
            },
            {
                "name": "B_0x1",
                "description": "DAC channel1 DMA mode enabled",
                "value": "0x1",
            },
        ],
    }

    result = EnumeratedValues.from_dict(enums_dict)

    assert None is result.parent
    assert None is result.derived_from
    assert "DMAEN1" == result.name
    assert None is result.header_enum_name
    assert Usage.READ_WRITE == result.usage
    for enum_value in result.enumerated_values:
        assert enum_value.parent is result
        assert "DMAEN1" == enum_value.parent.name
    assert "B_0x0" == result.enumerated_values[0].name
    assert 0 == result.enumerated_values[0].value
    assert "disabled" in result.enumerated_values[0].description
    assert "B_0x1" == result.enumerated_values[1].name
    assert 1 == result.enumerated_values[1].value
    assert "enabled" in result.enumerated_values[1].description


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
    result = EnumeratedValue(None, name, description, value, None)
    assert result.parent is None
    assert result.name is name
    assert result.description is description
    assert result.value is expected_value
    assert result.is_default is None


enum_value_from_dict_params = [
    (
        {"name": "B_0x1", "description": "dac_ch1_trg1", "value": "0x1"},
        EnumeratedValue(None, "B_0x1", "dac_ch1_trg1", "0x1", None),
    ),
]


@pytest.mark.parametrize("enum_dict, expected", enum_value_from_dict_params)
def test_enum_value_from_dict(enum_dict, expected):
    result = EnumeratedValue.from_dict(enum_dict)
    assert expected == result


def test_enum_value_is_invalid():
    # This call works
    _ = (EnumeratedValue(None, "B_0x1", "dac_ch1_trg1", "0x1", None),)
    with pytest.raises(ValueError):
        # This one fails to parse
        _ = (EnumeratedValue(None, "B_0x1", "dac_ch1_trg1", "01", None),)
