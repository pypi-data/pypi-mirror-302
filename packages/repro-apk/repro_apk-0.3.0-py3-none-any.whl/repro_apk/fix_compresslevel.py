#!/usr/bin/python3
# encoding: utf-8
# SPDX-FileCopyrightText: 2024 FC (Fay) Stegerman <flx@obfusk.net>
# SPDX-License-Identifier: AGPL-3.0-or-later

import struct
import zipfile
import zlib

from fnmatch import fnmatch
from typing import Any, Dict

ATTRS = ("compress_type", "create_system", "create_version", "date_time",
         "external_attr", "extract_version", "flag_bits")
LEVELS = (9, 6, 4, 1)


class Error(RuntimeError):
    pass


# FIXME: is there a better alternative?
class ReproducibleZipInfo(zipfile.ZipInfo):
    """Reproducible ZipInfo hack."""

    if "_compresslevel" not in zipfile.ZipInfo.__slots__:       # type: ignore[attr-defined]
        if "compress_level" not in zipfile.ZipInfo.__slots__:   # type: ignore[attr-defined]
            raise Error("zipfile.ZipInfo has no ._compresslevel")

    _compresslevel: int
    _override: Dict[str, Any] = {}

    def __init__(self, zinfo: zipfile.ZipInfo, **override: Any) -> None:
        # pylint: disable=W0231
        if override:
            self._override = {**self._override, **override}
        for k in self.__slots__:
            if hasattr(zinfo, k):
                setattr(self, k, getattr(zinfo, k))

    def __getattribute__(self, name: str) -> Any:
        if name != "_override":
            try:
                return self._override[name]
            except KeyError:
                pass
        return object.__getattribute__(self, name)


def fix_compresslevel(input_apk: str, output_apk: str, compresslevel: int,
                      *patterns: str, verbose: bool = False) -> None:
    if not patterns:
        raise ValueError("No patterns")
    with open(input_apk, "rb") as fh_raw:
        with zipfile.ZipFile(input_apk) as zf_in:
            with zipfile.ZipFile(output_apk, "w") as zf_out:
                for info in zf_in.infolist():
                    attrs = {attr: getattr(info, attr) for attr in ATTRS}
                    zinfo = ReproducibleZipInfo(info, **attrs)
                    tofix = fnmatches_with_negation(info.filename, *patterns)
                    level = None
                    if info.compress_type not in (0, 8):
                        raise Error(f"Unsupported compress_type {info.compress_type}")
                    if info.compress_type == 0 and tofix:
                        raise Error("Expected compress_type 8 to fix compresslevel")
                    if info.compress_type == 8 and not tofix:
                        fh_raw.seek(info.header_offset)
                        n, m = struct.unpack("<HH", fh_raw.read(30)[26:30])
                        fh_raw.seek(info.header_offset + 30 + m + n)
                        ccrc = 0
                        size = info.compress_size
                        while size > 0:
                            ccrc = zlib.crc32(fh_raw.read(min(size, 4096)), ccrc)
                            size -= 4096
                        with zf_in.open(info) as fh_in:
                            comps = {lvl: zlib.compressobj(lvl, 8, -15) for lvl in LEVELS}
                            ccrcs = {lvl: 0 for lvl in LEVELS}
                            while True:
                                data = fh_in.read(4096)
                                if not data:
                                    break
                                for lvl in LEVELS:
                                    ccrcs[lvl] = zlib.crc32(comps[lvl].compress(data), ccrcs[lvl])
                            for lvl in LEVELS:
                                if ccrc == zlib.crc32(comps[lvl].flush(), ccrcs[lvl]):
                                    level = lvl
                                    break
                            else:
                                raise Error(f"Unable to determine compresslevel for {info.filename!r}")
                    if tofix:
                        print(f"fixing {info.filename!r}...")
                        zinfo._compresslevel = compresslevel
                    else:
                        if verbose:
                            print(f"copying {info.filename!r}...")
                        if level is not None:
                            zinfo._compresslevel = level
                    if verbose and level is not None:
                        print(f"  compresslevel={level}")
                    with zf_in.open(info) as fh_in:
                        with zf_out.open(zinfo, "w") as fh_out:
                            while True:
                                data = fh_in.read(4096)
                                if not data:
                                    break
                                fh_out.write(data)


def fnmatches_with_negation(filename: str, *patterns: str) -> bool:
    r"""
    Filename matching with shell patterns and negation.

    Checks whether filename matches any of the fnmatch patterns.

    An optional prefix "!" negates the pattern, invalidating a successful match
    by any preceding pattern; use a backslash ("\") in front of the first "!"
    for patterns that begin with a literal "!".

    >>> fnmatches_with_negation("foo.xml", "*", "!*.png")
    True
    >>> fnmatches_with_negation("foo.png", "*", "!*.png")
    False
    >>> fnmatches_with_negation("!foo.png", r"\!*.png")
    True

    """
    matches = False
    for p in patterns:
        if p.startswith("!"):
            if fnmatch(filename, p[1:]):
                matches = False
        else:
            if p.startswith(r"\!"):
                p = p[1:]
            if fnmatch(filename, p):
                matches = True
    return matches


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="fix-compresslevel.py")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("input_apk", metavar="INPUT_APK")
    parser.add_argument("output_apk", metavar="OUTPUT_APK")
    parser.add_argument("compresslevel", metavar="COMPRESSLEVEL", type=int)
    parser.add_argument("patterns", metavar="PATTERN", nargs="+")
    args = parser.parse_args()
    fix_compresslevel(args.input_apk, args.output_apk, args.compresslevel,
                      *args.patterns, verbose=args.verbose)

# vim: set tw=80 sw=4 sts=4 et fdm=marker :
