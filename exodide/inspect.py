"""
exodide.inspect module

This module provides functionalities
to inspect shared object (.so) in extension package (.whl)

Examples
--------
>>> from exodide.inspect import MetaData
>>> metadata = MetaData("example-module.so")
>>> print(metadata)

This module can be run from command line, too.
`python3 -m exodide.inspect example-module.so`
"""

import os
import sys

import numpy as np

class MetaData:
    def __init__(self, file: str):
        self.valid: bool = True
        self.msg: str = ""

        if not os.path.exists(file):
            self.valid = False
            self.msg += f"Error: '{file}' doesn't exist."
            return

        try:
            self.mem = np.memmap(file, dtype=np.uint8)
        except e:
            self.valid = False
            self.msg += f"Error: Fail to open: {e}"
            return

        self.file_size = self.mem.shape[0]
        self.msg += f"File Size: {self.file_size}\n"

        self.endian: int = self.mem[0:4].view(np.uint32)
        self.msg += f"Endian: {int(self.endian): x}\n"
        self.is_LE: bool = True
        if self.endian == 0x6d736100:
            self.is_LE = True
            self.msg += "  Little Endian\n"
        elif self.endian == 0x0061736d:
            self.is_LE = False
            self.msg += "  Big Endian\n"
        else:
            self.valid = False
            self.msg += f"  Error: Unknown Endian: {self.endian}"
            return

        if self.mem[8] != 0:
            self.valid = False
            self.msg = f"Error: First section must be dylink."
            return

        self.idx: int = 9
        section_size: int = self.getLEB()
        self.end: int = self.idx + section_size
        self.name: str = self.getString()
        self.msg += f"Section: {self.name}\n"
        self.msg += f"  Address: [{self.end-section_size}, {self.end}) byte\n"

        if self.name == "dylink":
            self.dylink()
        elif self.name == "dylink.0":
            self.dylink0()
        else:
            self.valid = False
            self.msg += f"Error: First Section must be dylink/dylink.0"
            return

        align = getattr(self, "table_align", None)
        if align != 0:
            self.valid = False
            self.msg += f"Error: Invalid Table Align: {align}"
            return

        if self.idx != self.end:
            self.valid = False
            self.msg += f"Error: idx!=end ({self.idx} != {self.end})"

    def dylink(self):
        self.memory_size: int = self.getLEB()
        self.memory_align: int = self.getLEB()
        self.msg += f"  Memory:\n"
        self.msg += f"    Size: {self.memory_size}\n"
        self.msg += f"    Align: {self.memory_align}\n"

        self.table_size: int = self.getLEB()
        self.table_align: int = self.getLEB()
        self.msg += f"  Table:\n"
        self.msg += f"    Size: {self.table_size}\n"
        self.msg += f"    Align: {self.table_align}\n"

        necessary_count: int = self.getLEB()
        self.necessary_libs = [self.getString() for _ in range(necessary_count)]
        self.msg += f"  Necessary Dynamic Libs: {self.necessary_libs}\n"


    def dylink0(self):
        WASM_DYLINK_MEM_INFO: int = 0x1
        WASM_DYLINK_MEM_NEEDED: int = 0x2
        WASM_DYLINK_EXPORT_INFO: int = 0x3
        WASM_DYLINK_IMPORT_INFO: int = 0x4
        WASM_SYMBOL_TLS: int = 0x100
        WASM_SYMBOL_BINDING_MASK: int = 0x3
        WASM_SYMBOL_BINDING_WEAK: int = 0x1

        self.necessary_libs = []
        self.tls_export = set()
        self.weak_import = set()
        while self.idx < self.end:
            subsection_type: int = self.getU8()
            subsection_size: int = self.getLEB()
            if subsection_type == WASM_DYLINK_MEM_INFO:
                self.msg += f"  Sub-Section: WASM_DYLINK_MEM_INFO\n"

                self.memory_size: int = self.getLEB()
                self.memory_align: int = self.getLEB()
                self.msg += f"  Memory:\n"
                self.msg += f"    Size: {self.memory_size}\n"
                self.msg += f"    Align: {self.memory_align}\n"

                self.table_size: int = self.getLEB()
                self.table_align: int = self.getLEB()
                self.msg += f"  Table:\n"
                self.msg += f"    Size: {self.table_size}\n"
                self.msg += f"    Align: {self.table_align}\n"
            elif subsection_type == WASM_DYLINK_MEM_NEEDED:
                self.msg += f"  Sub-Section: WASM_DYLINK_MEM_NEEDED\n"

                necessary_count: int = self.getLEB()
                self.necessary_libs.extend([self.getString()
                                            for _ in range(necessary_count)])
            elif subsection_type == WASM_DYLINK_EXPORT_INFO:
                self.msg += f"  Sub-Section: WASM_DYLINK_EXPORT_INFO\n"

                cnt: int = self.getLEB()
                while cnt > 0:
                    cnt -= 1
                    sym = self.getString()
                    if (getLEB() & WASM_SYMBOL_TLS):
                        self.tls_export.add(sym)
            elif subsection_type == WASM_DYLINK_IMPORT_INFO:
                self.msg += f"  Sub-Section: WASM_DYLINK_IMPORT_INFO\n"

                cnt: int = self.getLEB()
                while cnt > 0:
                    cnt -= 1
                    mod = self.getString()
                    sym = self.getString()
                    if ((getLEB() & WASM_SYMBOL_BINDING_MASK) ==
                        WASM_SYMBOL_BINDING_WEAK):
                        self.weak_import.add(sym)
            else:
                self.msg += f"  Sub-Section: Unknown: {subsection_type}\n"
                self.idx += subsection_size

        self.msg += f"  Necessary Dynamic Libs: {self.necessary_libs}\n"
        self.msg += f"  TLS Export: {self.tls_export}\n"
        self.msg += f"  Weak Import: {self.weak_import}\n"


    def getU8(self) -> int:
        v: int = self.mem[self.idx]
        self.idx += 1
        return v


    def getLEB(self) -> int:
        ret: int = 0
        digit: int = 0

        while True:
            b: int = self.mem[self.idx]
            self.idx += 1
            ret += ((b & 0x7f) << digit)
            digit += 7

            if b < 0x80:
                break

        return ret

    def getString(self) -> str:
        length: int = self.getLEB()
        s: str = str(self.mem[self.idx:self.idx+length]
                     .view(dtype=np.dtype(f"a{length}"))[0],
                     encoding="utf-8")
        self.idx += length
        return s

    def __repr__(self):
        return self.msg



def cli() -> None:
    meta: MetaData = MetaData(sys.argv[1])
    print(meta)


if __name__ == "__main__":
    cli()
