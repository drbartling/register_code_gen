import json
import tomllib
from dataclasses import dataclass
from pathlib import Path

import click
import xmltodict
from rich.traceback import install

import templating
from svd.basic_elements import Access
from svd.device import Device
from svd.field import Field
from svd.peripheral import Peripheral
from svd.register import Register
from templating import Template

install()

with open("c_template.toml", "rb") as toml_file:
    templates = tomllib.load(toml_file)
    templates = templating.named_tuple_from_dict("Templates", templates)


@click.command()
@click.option(
    "-i",
    "--input-file",
    prompt=True,
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
)
def main(input_file: Path, output_dir: Path):  # pragma: no cover
    """Generate C header and dir from CMSIS-SVD which is often used to provide register descriptions for microcontrollers"""

    with input_file.open("r", encoding="utf-8") as f:
        data = f.read()
    svd_dict = xmltodict.parse(data)
    device = Device.from_dict(svd_dict["device"])

    if output_dir is None:
        output_dir = Path(device.name.lower())  # pylint: disable=no-member
    output = OutputStructure(output_dir, device)

    with output.json_file.open("w", encoding="utf-8") as f:
        json.dump(svd_dict, f, indent=2)
    output.main_header.parent.mkdir(parents=True, exist_ok=True)
    output.main_header.open("w", encoding="utf-8")
    output.main_source.parent.mkdir(parents=True, exist_ok=True)
    output.main_source.open("w", encoding="utf-8")
    write_header(output, device)
    write_peripherals(output, device)
    write_main_source(output, device)
    write_footer(output, device)


@dataclass
class OutputStructure:
    output_root: Path
    device: Device

    @property
    def json_file(self) -> Path:
        # pylint: disable=no-member
        return self.output_root / f"{self.device.name.lower()}.json"

    @property
    def src_dir(self) -> Path:
        return self.output_root / "src"

    @property
    def include_root(self) -> Path:
        return self.output_root / "include"

    @property
    def include_dir(self) -> Path:
        # pylint: disable=no-member
        return self.include_root / self.device.name.lower()

    @property
    def main_header(self) -> Path:
        # pylint: disable=no-member
        return self.include_dir / f"{self.device.name.lower()}.h"

    @property
    def main_source(self) -> Path:
        # pylint: disable=no-member
        return self.src_dir / f"{self.device.name.lower()}.c"


def write_header(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        s = Template(templates.device.header.top).substitute(device=device)
        f.write(s)


def write_main_source(output: OutputStructure, device: Device):
    include_path = output.main_header.relative_to(output.include_root)
    with output.main_header.open("a", encoding="utf-8") as h:
        with output.main_source.open("a", encoding="utf-8") as c:
            c.write(f'#include "{include_path}"\n\n')
            for peripheral in sorted(
                device.peripherals,
                key=lambda peripheral: peripheral.base_address,
            ):
                s = Template(templates.peripheral.definition).substitute(
                    Device=device, peripheral=peripheral, templates=templates
                )
                c.write(s)

                s = Template(templates.peripheral.declaration).substitute(
                    Device=device, peripheral=peripheral, templates=templates
                )
                h.write(s)
            h.write("\n")


def write_footer(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        s = Template(templates.device.header.bottom).substitute(device=device)
        f.write(s)


def write_peripherals(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        for p in sorted(
            device.peripherals, key=lambda peripheral: peripheral.name
        ):
            if p.derived_from is None:
                include_path = output.include_dir / f"{p.name.lower()}.h"
                include_path = include_path.relative_to(output.include_root)

                s = Template(templates.peripheral.include).substitute(
                    device=device, peripheral=p, templates=templates
                )
                f.write(s)
                write_peripheral(output, p)
        f.write("\n")


@dataclass
class PeripheralOutputStructure:
    output_root: Path
    peripheral: Peripheral

    @property
    def src_dir(self) -> Path:
        return self.output_root / "src"

    @property
    def include_root(self) -> Path:
        return self.output_root / "include"

    @property
    def include_dir(self) -> Path:
        return self.include_root / self.peripheral.parent.name.lower()

    @property
    def header(self) -> Path:
        return self.include_dir / f"{self.peripheral.name.lower()}.h"


def write_peripheral(output: OutputStructure, peripheral: Peripheral):
    p_out = PeripheralOutputStructure(output.output_root, peripheral)
    p_out.header.parent.mkdir(parents=True, exist_ok=True)
    p_out.header.open("w", encoding="utf-8")
    write_peripheral_header(p_out, peripheral)
    write_peripheral_registers(p_out, peripheral)
    write_peripheral_struct(p_out, peripheral)
    write_peripheral_footer(p_out, peripheral)


def write_peripheral_header(
    output: PeripheralOutputStructure, peripheral: Peripheral
):
    with output.header.open("w", encoding="utf-8") as f:
        s = Template(templates.peripheral.header.top).substitute(
            peripheral=peripheral
        )
        f.write(s)


def write_peripheral_footer(output: OutputStructure, peripheral: Peripheral):
    with output.header.open("a", encoding="utf-8") as f:
        s = Template(templates.peripheral.header.bottom).substitute(
            peripheral=peripheral
        )
        f.write(s)


def write_peripheral_registers(output: OutputStructure, peripheral: Peripheral):
    for r in sorted(
        peripheral.registers, key=lambda register: register.address_offset
    ):
        write_register(output, r)


def write_peripheral_struct(output: OutputStructure, peripheral: Peripheral):
    type_name = f"{peripheral.name.upper()}_peripheral_registers_t"
    struct_name = f"{peripheral.name.upper()}_peripheral_registers_s"
    with output.header.open("a", encoding="utf-8") as f:
        f.write(f"/**\n* {peripheral.description}\n*/\n")
        f.write(f"typedef struct {struct_name} {{\n")

        addressed_registers = {}
        for register in peripheral.registers:
            try:
                addressed_registers[register.address_offset].append(register)
            except KeyError:
                addressed_registers[register.address_offset] = list([register])

        current_offset = 0
        for address in sorted(list(addressed_registers.keys())):
            if current_offset < address:
                reserved_bytes = int(address - current_offset)
                f.write(
                    f"uint8_t const reserved_0x{current_offset:02X}[{reserved_bytes}];\n"
                )
                current_offset += reserved_bytes
            registers = addressed_registers[address]
            if 1 < len(registers):
                f.write("union{\n")

            for register in sorted(
                registers, key=lambda register: register.name
            ):
                reg_name: str = register_name(register)
                reg_type = (
                    f"{register.parent.name.upper()}_{reg_name.lower()}_t"
                )
                if hasattr(register, "description"):
                    f.write(f"///{register.description}\n")
                f.write(f"{reg_type} {reg_name.lower()};\n")
                current_offset = register.address_offset + int(
                    register.size / 8
                )

            if 1 < len(registers):
                f.write("};\n")
        f.write(f"}} {type_name};\n")
        for register in sorted(
            peripheral.registers, key=lambda register: register.address_offset
        ):
            reg_name: str = register_name(register)
            f.write(
                f"STATIC_ASSERT_MEMBER_OFFSET({type_name}, {reg_name.lower()}, 0x{register.address_offset:02X});\n"
            )

        f.write("\n")


def register_name(register: Register):
    name: str = register.name
    name = name.replace(f"{register.parent.name}_", "", 1)
    return name


def write_register(output: PeripheralOutputStructure, register: Register):
    write_enums(output, register)
    reg_name: str = register_name(register)
    with output.header.open("a", encoding="utf-8") as f:
        type_name = f"{register.parent.name.upper()}_{reg_name.lower()}_t"
        union_name = f"{register.parent.name.upper()}_{reg_name.lower()}_u"
        if hasattr(register, "description"):
            f.write(f"/**\n * {register.description} \n*/\n")
        f.write(f"typedef union {union_name} {{\n")
        f.write("struct {\n")

        current_offset = 0
        for field in sorted(
            register.fields, key=lambda register: register.bit_offset
        ):
            if current_offset < field.bit_offset:
                reserved_offset = current_offset
                reserved_width = field.bit_offset - reserved_offset
                write_reserved(
                    f, register.size, reserved_offset, reserved_width
                )
                current_offset = reserved_offset + reserved_width
            write_field(f, field)
            current_offset = field.bit_offset + field.bit_width

        f.write("};\n")
        f.write(f"uint{register.size}_t bits;\n")
        f.write(f"}} {type_name};\n")
        f.write(
            f"STATIC_ASSERT_TYPE_SIZE({type_name}, sizeof(uint{register.size}_t));\n"
        )
        f.write("\n")


written_enums = set()


def write_enums(output: PeripheralOutputStructure, register: Register):
    peripheral_name = register.parent.name

    with output.header.open("a", encoding="utf-8") as f:
        for field in sorted(
            register.fields, key=lambda register: register.bit_offset
        ):
            if None is field.enumerated_values:
                continue

            field_name = f"{peripheral_name}_{field.name.lower()}"
            type_name = f"{field_name}_t"
            enum_name = f"{field_name}_e"

            if type_name in written_enums:
                continue
            written_enums.add(type_name)

            f.write(f"/**\n * {field.description}\n */\n")
            f.write(f"typedef enum {enum_name} {{\n")
            width = str(int(field.bit_width / 4) + 1)

            for enum_value in field.enumerated_values:
                value = f"0x{enum_value.value:0{width}X}"
                desc = enum_value.description
                name = enum_value.name.lower()
                f.write(f"///{desc}\n")
                f.write(f"{field_name}_{name} = {value},\n")
            f.write(f"}}{type_name};\n")
            f.write("\n")


def write_field(f, field: Field):
    if field.derived_from is not None:
        type_field = field.derived_from
    else:
        type_field = field

    if type_field.enumerated_values:
        peripheral_name = type_field.parent.parent.name
        field_name = f"{peripheral_name}_{type_field.name.lower()}"
        field_type = f"{field_name}_t"
    else:
        size = type_field.parent.size
        field_type = f"uint{size}_t"

    const = "const" if field.access == Access.READ_ONLY else ""
    f.write(f"///{field.description}\n")
    f.write(f"{field_type} {const} {field.name.lower()}:{field.bit_width};\n")


def write_reserved(f, reg_size, offset, width):
    f.write(f"uint{reg_size}_t const reserved_{offset:02}:{width};\n")


if __name__ == "__main__":  # pragma: no cover
    # Ignored missing parameter lint, since the click library passes the
    # arguments in from the command line for us
    main()  # pylint:disable=no-value-for-parameter
