import pytest

from svd.basic_elements import Access
from svd.register import Register


def test_register_basic_init():
    result = Register(
        name="CR",
        address_offset=0x0,
        size=0x20,
    )

    assert "CR" == result.name
    assert 0 == result.address_offset
    assert 32 == result.size
    assert None is result.display_name
    assert None is result.description
    assert None is result.alternate_group
    assert None is result.alternate_register
    assert None is result.access
    assert None is result.protection
    assert None is result.reset_value
    assert None is result.reset_mask
    assert None is result.data_type
    assert None is result.modified_write_values
    assert None is result.write_constraint
    assert None is result.read_action
    assert None is result.fields
    assert None is result.derived_from


register_from_dict_params = [
    (
        {
            "name": "CRC_DR",
            "displayName": "CRC_DR",
            "description": "Data register",
            "addressOffset": "0x0",
            "size": "0x20",
            "access": "read-write",
            "resetValue": "0xFFFFFFFF",
        },
        {
            "name": "CRC_DR",
            "display_name": "CRC_DR",
            "description": "Data register",
            "address_offset": 0x0,
            "size": 0x20,
            "access": Access.READ_WRITE,
            "reset_value": 0xFFFFFFFF,
        },
    ),
    (
        {
            "name": "CRC_DR",
            "displayName": "CRC_DR",
            "description": "Data register",
            "addressOffset": "0x0",
            "size": "0x20",
            "access": "read-write",
            "resetValue": "0xFFFFFFFF",
            "fields": {
                "field": {
                    "name": "DR",
                    "description": "Data register bits",
                    "bitOffset": "0",
                    "bitWidth": "32",
                }
            },
        },
        {
            "name": "CRC_DR",
            "display_name": "CRC_DR",
            "description": "Data register",
            "address_offset": 0x0,
            "size": 0x20,
            "access": Access.READ_WRITE,
            "reset_value": 0xFFFFFFFF,
            "fields": [
                {
                    "name": "DR",
                    "description": "Data register bits",
                    "bit_offset": 0,
                    "bit_width": 32,
                },
            ],
        },
    ),
    (
        {
            "name": "DAC_DHR12RD",
            "displayName": "DAC_DHR12RD",
            "description": "Dual DAC 12-bit right-aligned data",
            "addressOffset": "0x20",
            "size": "0x20",
            "access": "read-write",
            "resetValue": "0x00000000",
            "fields": {
                "field": [
                    {
                        "name": "DACC1DHR",
                        "description": "DAC channel1 12-bit right-aligned data ch1",
                        "bitOffset": "0",
                        "bitWidth": "12",
                        "access": "read-write",
                    },
                    {
                        "name": "DACC2DHR",
                        "description": "DAC channel1 12-bit right-aligned data ch2",
                        "bitOffset": "16",
                        "bitWidth": "12",
                        "access": "read-write",
                    },
                ]
            },
        },
        {
            "name": "DAC_DHR12RD",
            "display_name": "DAC_DHR12RD",
            "description": "Dual DAC 12-bit right-aligned data",
            "address_offset": 0x20,
            "size": 0x20,
            "access": Access.READ_WRITE,
            "reset_value": 0x00000000,
            "fields": [
                {
                    "name": "DACC1DHR",
                    "description": "DAC channel1 12-bit right-aligned data ch1",
                    "bit_offset": 0,
                    "bit_width": 12,
                    "access": Access.READ_WRITE,
                },
                {
                    "name": "DACC2DHR",
                    "description": "DAC channel1 12-bit right-aligned data ch2",
                    "bit_offset": 16,
                    "bit_width": 12,
                    "access": Access.READ_WRITE,
                },
            ],
        },
    ),
]


@pytest.mark.parametrize("register_dict, expected", register_from_dict_params)
def test_register_from_dict(register_dict, expected):
    result = Register.from_dict(register_dict)
    assert expected["name"] == result.name
    assert expected["display_name"] == result.display_name
    assert expected["description"] == result.description
    assert expected["address_offset"] == result.address_offset
    assert expected["size"] == result.size
    assert expected["access"] == result.access
    assert expected["reset_value"] == result.reset_value
    if expected_fields := expected.get("fields"):
        for i, result_field in enumerate(result.fields):
            assert result is result_field.parent
            assert expected_fields[i].get("name") == result_field.name
            assert (
                expected_fields[i].get("description")
                == result_field.description
            )
            assert (
                expected_fields[i].get("bit_offset") == result_field.bit_offset
            )
            assert expected_fields[i].get("bit_width") == result_field.bit_width
            assert expected_fields[i].get("access") == result_field.access
