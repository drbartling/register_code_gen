import pytest

from svd.basic_elements import Access
from svd.field import Field

field_init_params = [
    (
        "foo",
        2,
        1,
        "foo enable",
        "read-write",
        None,
        None,
        None,
        None,
    ),
]


@pytest.mark.parametrize(
    "name, bit_offset, bit_width, description, access, modified_write_values, write_constraint, read_action, enumerated_values",
    field_init_params,
)
# pylint: disable=too-many-arguments
def test_field_init(
    name,
    bit_offset,
    bit_width,
    description,
    access,
    modified_write_values,
    write_constraint,
    read_action,
    enumerated_values,
):
    result = Field(
        name,
        bit_offset,
        bit_width,
        description,
        access,
        modified_write_values,
        write_constraint,
        read_action,
        enumerated_values,
    )
    assert name == result.name
    assert description == result.description
    assert bit_offset == result.bit_offset
    assert bit_width == result.bit_width
    assert Access(access) == result.access
    assert modified_write_values == result.modified_write_values
    assert read_action == result.read_action
    assert enumerated_values == result.enumerated_values


field_from_dict_params = [
    (
        {
            "name": "STATTX",
            "description": "Status bits, for transmission",
            "bitOffset": "4",
            "bitWidth": "2",
            "access": "write-only",
        },
        {
            "name": "STATTX",
            "description": "Status bits, for transmission",
            "bit_offset": 4,
            "bit_width": 2,
            "access": Access.WRITE_ONLY,
        },
    ),
    (
        {
            "name": "RP",
            "description": "Receive error passive",
            "bitOffset": "15",
            "bitWidth": "1",
            "access": "read-only",
            "enumeratedValues": {
                "enumeratedValue": [
                    {
                        "name": "B_0x0",
                        "description": "The receive error counter is below",
                        "value": "0x0",
                    },
                    {
                        "name": "B_0x1",
                        "description": "The receive error counter has reached",
                        "value": "0x1",
                    },
                ]
            },
        },
        {
            "name": "RP",
            "description": "Receive error passive",
            "bit_offset": 15,
            "bit_width": 1,
            "access": Access.READ_ONLY,
            "enumerated_values": [
                {
                    "name": "B_0x0",
                    "description": "The receive error counter is below",
                    "value": 0,
                },
                {
                    "name": "B_0x1",
                    "description": "The receive error counter has reached",
                    "value": 1,
                },
            ],
        },
    ),
]


@pytest.mark.parametrize("field_dict, expected", field_from_dict_params)
def test_field_from_dict(field_dict, expected):
    result = Field.from_dict(field_dict)

    assert expected.get("name") == result.name
    assert expected.get("description") == result.description
    assert expected.get("bit_offset") == result.bit_offset
    assert expected.get("bit_width") == result.bit_width
    assert expected.get("access") == result.access
    assert expected.get("modified_write_values") == result.modified_write_values
    assert expected.get("read_action") == result.read_action
    if expected_enums := expected.get("enumerated_values"):
        assert result.enumerated_values.parent is result
        for i, result_enum in enumerate(result.enumerated_values):
            assert expected_enums[i].get("name") == result_enum.name
            assert (
                expected_enums[i].get("description") == result_enum.description
            )
            assert expected_enums[i].get("value") == result_enum.value
