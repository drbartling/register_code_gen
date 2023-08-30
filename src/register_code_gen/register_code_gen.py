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
from templating import Template, default_template

install()

# pylint: disable=invalid-name
templates = None


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
    "-t",
    "--template-file",
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
def main(input_file: Path, template_file: Path, output_dir: Path):
    """Generate C header and dir from CMSIS-SVD which is often used to provide register descriptions for microcontrollers"""
    global templates  # pylint: disable=global-statement
    if template_file:
        with template_file.open("rb") as f:
            templates = tomllib.load(f)
    else:
        templates = default_template.default_templates()
    templates = templating.named_tuple_from_dict("Templates", templates)

    with input_file.open("r", encoding="utf-8") as f:
        data = f.read()
    svd_dict = xmltodict.parse(data)
    device = Device.from_dict(svd_dict["device"])

    if output_dir is None:
        output_dir = Path(device.name.lower())  # pylint: disable=no-member
    output = OutputStructure(output_dir, device)

    output.main_header.parent.mkdir(parents=True, exist_ok=True)
    output.main_header.open("w", encoding="utf-8")
    output.main_source.parent.mkdir(parents=True, exist_ok=True)
    output.main_source.open("w", encoding="utf-8")

    with output.json_file.open("w", encoding="utf-8") as f:
        json.dump(svd_dict, f, indent=2)

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
        f.write(Template(templates.device.header.top).substitute(device=device))


def write_main_source(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as h:
        with output.main_source.open("a", encoding="utf-8") as c:
            c.write(
                Template(templates.device.include).substitute(device=device)
            )
            c.write("\n")
            for peripheral in sorted(
                device.peripherals,
                key=lambda peripheral: peripheral.base_address,
            ):
                c.write(
                    Template(templates.peripheral.definition).substitute(
                        Device=device,
                        peripheral=peripheral,
                        templates=templates,
                    )
                )

                h.write(
                    Template(templates.peripheral.declaration).substitute(
                        Device=device,
                        peripheral=peripheral,
                        templates=templates,
                    )
                )
            h.write("\n")


def write_footer(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        f.write(
            Template(templates.device.header.bottom).substitute(device=device)
        )


def write_peripherals(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        for p in sorted(
            device.peripherals, key=lambda peripheral: peripheral.name
        ):
            if p.derived_from is p:
                f.write(
                    Template(templates.peripheral.include).substitute(
                        device=device, peripheral=p, templates=templates
                    )
                )
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
        f.write(
            Template(templates.peripheral.header.top).substitute(
                peripheral=peripheral, device=peripheral.parent
            )
        )


def write_peripheral_footer(output: OutputStructure, peripheral: Peripheral):
    with output.header.open("a", encoding="utf-8") as f:
        f.write(
            Template(templates.peripheral.header.bottom).substitute(
                peripheral=peripheral,
                templates=templates,
                device=peripheral.parent,
            )
        )


def write_peripheral_registers(output: OutputStructure, peripheral: Peripheral):
    for r in sorted(
        peripheral.registers, key=lambda register: register.address_offset
    ):
        write_register(output, r)


def write_peripheral_struct(output: OutputStructure, peripheral: Peripheral):
    with output.header.open("a", encoding="utf-8") as f:
        f.write(
            Template(templates.peripheral.structure.top).substitute(
                peripheral=peripheral,
                templates=templates,
                device=peripheral.parent,
            )
        )

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
                    Template(
                        templates.peripheral.structure.reserved
                    ).substitute(offset=current_offset, size=reserved_bytes)
                )
                current_offset += reserved_bytes
            registers = addressed_registers[address]
            if 1 < len(registers):
                f.write("union{\n")

            for register in sorted(
                registers, key=lambda register: register.name
            ):
                f.write(
                    Template(templates.register.definition).substitute(
                        peripheral=peripheral,
                        templates=templates,
                        device=peripheral.parent,
                        register=register,
                    )
                )

                current_offset = register.address_offset + int(
                    register.size / 8
                )

            if 1 < len(registers):
                f.write("};\n")

        f.write(
            Template(templates.peripheral.structure.bottom).substitute(
                peripheral=peripheral,
                templates=templates,
                device=peripheral.parent,
            )
        )
        for register in sorted(
            peripheral.registers, key=lambda register: register.address_offset
        ):
            f.write(
                Template(templates.register.offset_assert).substitute(
                    peripheral=peripheral,
                    templates=templates,
                    device=peripheral.parent,
                    register=register,
                )
            )
        f.write("\n")


def write_register(output: PeripheralOutputStructure, register: Register):
    write_enums(output, register)
    with output.header.open("a", encoding="utf-8") as f:
        f.write(
            Template(templates.register.structure.top).substitute(
                register=register,
                templates=templates,
                peripheral=register.parent,
            )
        )
        current_offset = 0
        for field in sorted(
            register.fields, key=lambda register: register.bit_offset
        ):
            if current_offset < field.bit_offset:
                reserved_offset = current_offset
                reserved_width = field.bit_offset - reserved_offset
                write_reserved(f, register, reserved_offset, reserved_width)
                current_offset = reserved_offset + reserved_width
            write_field(f, field)
            current_offset = field.bit_offset + field.bit_width

        f.write(
            Template(templates.register.structure.bottom).substitute(
                register=register,
                templates=templates,
                peripheral=register.parent,
            )
        )
        f.write(
            Template(templates.register.size_assert).substitute(
                register=register,
                templates=templates,
                peripheral=register.parent,
            )
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
            if field_name in written_enums:
                continue
            written_enums.add(field_name)

            f.write(
                Template(templates.enum.definition.top).substitute(
                    peripheral=register.parent,
                    register=register,
                    field=field,
                    enum=field.enumerated_values,
                    templates=templates,
                )
            )

            for enum_value in field.enumerated_values:
                f.write(
                    Template(templates.enum.value).substitute(
                        peripheral=register.parent,
                        register=register,
                        field=field,
                        enum=enum_value,
                        templates=templates,
                    )
                )

            f.write(
                Template(templates.enum.definition.bottom).substitute(
                    peripheral=register.parent,
                    register=register,
                    field=field,
                    enum=field.enumerated_values,
                    templates=templates,
                )
            )
            f.write("\n")


def write_field(f, field: Field):
    if field.derived_from is not None:
        type_field = field.derived_from
    else:
        type_field = field

    const = "const" if field.access == Access.READ_ONLY else ""
    if type_field.enumerated_values:
        f.write(
            Template(templates.field.enum_definition).substitute(
                peripheral=field.parent.parent,
                register=field.parent,
                field=field,
                enum=field.enumerated_values,
                templates=templates,
                const=const,
            )
        )
    else:
        f.write(
            Template(templates.field.int_definition).substitute(
                peripheral=field.parent.parent,
                register=field.parent,
                field=field,
                enum=field.enumerated_values,
                templates=templates,
                const=const,
            )
        )


def write_reserved(f, register, offset, width):
    f.write(
        Template(templates.register.structure.reserved).substitute(
            register=register, offset=offset, width=width
        )
    )


if __name__ == "__main__":  # pragma: no cover
    # Ignored missing parameter lint, since the click library passes the
    # arguments in from the command line for us
    main()  # pylint:disable=no-value-for-parameter
