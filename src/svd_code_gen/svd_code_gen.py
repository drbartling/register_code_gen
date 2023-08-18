from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

import click
import pysvd
from pysvd.element import Device, Peripheral


@click.command()
@click.option(
    "-s",
    "--svd-input",
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
def main(svd_input, output_dir):  # pragma: no cover
    """Generate C header and dir from CMSIS-SVD which is often used to provide register descriptions for microcontrollers"""
    node = ElementTree.parse(svd_input).getroot()
    device = Device(node)
    if output_dir is None:
        output_dir = Path(device.name.lower())
    output = OutputStructure(output_dir, device)
    output.main_header.parent.mkdir(parents=True, exist_ok=True)
    output.main_header.open("w", encoding="utf-8")
    write_header(output, device)
    write_peripherals(output, device)
    write_footer(output, device)


@dataclass
class OutputStructure:
    output_root: Path
    device: Device

    @property
    def src_dir(self) -> Path:
        return self.output_root / "src"

    @property
    def include_dir(self) -> Path:
        return self.output_root / "include" / self.device.name.lower()

    @property
    def main_header(self) -> Path:
        return self.include_dir / f"{self.device.name.lower()}.h"


def write_header(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        f.write("/**\n")
        f.write("* @file\n")
        try:
            f.write(f"* @version {device.version}\n")
        except Exception:
            pass
        try:
            f.write(
                f"* @brief Register access structs for {device.vendor} {device.name}\n"
            )
        except Exception:
            pass
        f.write("*\n")
        try:
            f.write(f"* {device.description}\n*\n")
        except Exception:
            pass
        f.write(
            f"* @note This file is autogenerated using pysvd {pysvd.__version__}\n"
        )
        f.write("*/\n")
        f.write("\n")
        f.write(f"#ifndef {device.name}_H_\n")
        f.write(f"#define {device.name}_H_\n")
        f.write("\n")
        f.write("#ifdef __cplusplus\n")
        f.write('extern "C" {\n')
        f.write("#endif\n")
        f.write("\n")


def write_footer(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        f.write("#ifdef __cplusplus\n")
        f.write("}\n")
        f.write("#endif\n")
        f.write(f"#endif // {device.name}_H_\n")


def write_peripherals(output: OutputStructure, device: Device):
    with output.main_header.open("a", encoding="utf-8") as f:
        for p in sorted(
            device.peripherals, key=lambda peripheral: peripheral.name
        ):
            f.write(f'#include "{p.name.lower()}.h"\n')
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
    def include_dir(self) -> Path:
        return self.output_root / "include" / self.device.name.lower()

    @property
    def header(self) -> Path:
        return self.src_dir / f"{self.peripheral.name.lower()}.h"


def write_peripheral(output: OutputStructure, peripheral: Peripheral):
    p_out = PeripheralOutputStructure(output.output_root, peripheral)
    p_out.header.parent.mkdir(parents=True, exist_ok=True)
    p_out.header.open("w", encoding="utf-8")
    write_peripheral_header(p_out, peripheral)
    write_peripheral_footer(p_out, peripheral)


def write_peripheral_header(
    output: PeripheralOutputStructure, peripheral: Peripheral
):
    with output.header.open("w", encoding="utf-8") as f:
        f.write("/**\n")
        f.write("* @file\n")
        try:
            f.write(f"* @version {peripheral.parent.version}\n")
        except Exception:
            pass
        try:
            f.write(
                f"* @brief Register access structs for {peripheral.parent.vendor} {peripheral.name}\n"
            )
        except Exception:
            pass
        f.write("*\n")
        try:
            f.write(f"* {peripheral.description}\n")
        except Exception:
            pass
        try:
            f.write(f"* Derived From: {peripheral.derivedFrom.name}\n")
        except Exception:
            pass
        f.write("*\n")
        f.write(
            f"* @note This file is autogenerated using pysvd {pysvd.__version__}\n"
        )
        f.write("*/\n")
        f.write("\n")
        f.write(f"#ifndef {peripheral.name}_H_\n")
        f.write(f"#define {peripheral.name}_H_\n")
        f.write("\n")
        f.write("#ifdef __cplusplus\n")
        f.write('extern "C" {\n')
        f.write("#endif\n")
        f.write("\n")


def write_peripheral_footer(output: OutputStructure, peripheral: Peripheral):
    with output.header.open("a", encoding="utf-8") as f:
        f.write("#ifdef __cplusplus\n")
        f.write("}\n")
        f.write("#endif\n")
        f.write(f"#endif // {peripheral.name}_H_\n")


if __name__ == "__main__":  # pragma: no cover
    # Ignored missing parameter lint, since the click library passes the
    # arguments in from the command line for us
    main()  # pylint:disable=no-value-for-parameter
