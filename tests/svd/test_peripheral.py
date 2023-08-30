# pylint: disable=duplicate-code

from svd.basic_elements import AddressBlockUsage
from svd.peripheral import AddressBlock, Peripheral
from svd.register import Register


def test_peripheral_basic_init():
    address_block = AddressBlock(0x0, 0x400, AddressBlockUsage.REGISTERS)
    result = Peripheral(
        name="TIM1",
        base_address=0x0,
        address_block=address_block,
    )
    address_block.parent = result

    assert None is result.parent

    assert result is result.derived_from

    assert "TIM1" == result.name
    assert None is result.version
    assert None is result.description
    assert None is result.alternate_peripheral
    assert None is result.group_name
    assert None is result.prepend_to_name
    assert None is result.append_to_name
    assert None is result.header_struct_name
    assert None is result.disable_condition
    assert 0x0 == result.base_address
    assert None is result.size
    assert None is result.access
    assert None is result.protection
    assert None is result.reset_value
    assert None is result.reset_mask
    assert address_block is result.address_block
    assert None is result.interrupt
    assert None is result.registers


def test_peripheral_from_dict():
    peripheral_dict = {
        "name": "CRC",
        "description": "Cyclic redundancy check",
        "groupName": "CRC",
        "baseAddress": "0x40023000",
        "addressBlock": {
            "offset": "0x0",
            "size": "0x400",
            "usage": "registers",
        },
        "registers": {
            "register": [
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
                    "name": "CRC_IDR",
                    "displayName": "CRC_IDR",
                    "description": "Independent data register",
                    "addressOffset": "0x4",
                    "size": "0x20",
                    "access": "read-write",
                    "resetValue": "0x00000000",
                    "fields": {
                        "field": {
                            "name": "IDR",
                            "description": "General-purpose 32-bit data register\n              bits",
                            "bitOffset": "0",
                            "bitWidth": "32",
                        }
                    },
                },
            ]
        },
    }
    result = Peripheral.from_dict(peripheral_dict)

    assert "CRC" == result.name
    assert 0x40023000 == result.base_address
    assert (
        AddressBlock.from_dict(
            {
                "offset": "0x0",
                "size": "0x400",
                "usage": "registers",
            }
        )
        == result.address_block
    )
    assert None is result.version
    assert "Cyclic redundancy check" == result.description
    assert None is result.alternate_peripheral
    assert None is result.group_name
    assert None is result.prepend_to_name
    assert None is result.append_to_name
    assert None is result.header_struct_name
    assert None is result.disable_condition
    assert None is result.size
    assert None is result.access
    assert None is result.protection
    assert None is result.reset_value
    assert None is result.reset_mask
    assert None is result.interrupt
    assert result is result.derived_from
    assert None is result.parent

    for register in result.registers:
        assert result is register.parent
        assert isinstance(register, Register)
