from svd.basic_elements import AddressBlockUsage
from svd.peripheral import AddressBlock, Peripheral


def test_peripheral_basic_init():
    address_block = AddressBlock(0x0, 0x400, AddressBlockUsage.REGISTERS)
    result = Peripheral(
        name="TIM1",
        base_address=0x0,
        address_block=address_block,
    )
    address_block.parent = result

    assert None is result.parent

    assert None is result.derived_from

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
