import pytest

from svd.basic_elements import Access
from svd.field import Field

field_init_params = [
    (
        "foo",
        "foo enable",
        2,
        1,
        "read-write",
        None,
        None,
        None,
        None,
    ),
]


@pytest.mark.parametrize(
    "name, description, bit_offset, bit_width, access, modified_write_values, write_constraint, read_action, enumerated_values",
    field_init_params,
)
# pylint: disable=too-many-arguments
def test_field_init(
    name,
    description,
    bit_offset,
    bit_width,
    access,
    modified_write_values,
    write_constraint,
    read_action,
    enumerated_values,
):
    result = Field(
        name,
        description,
        bit_offset,
        bit_width,
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
