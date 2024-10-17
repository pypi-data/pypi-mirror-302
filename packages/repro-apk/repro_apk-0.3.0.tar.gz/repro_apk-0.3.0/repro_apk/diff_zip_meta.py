#!/usr/bin/python3
# encoding: utf-8
# SPDX-FileCopyrightText: 2024 FC (Fay) Stegerman <flx@obfusk.net>
# SPDX-License-Identifier: AGPL-3.0-or-later

import binascii
import difflib
import os
import struct
import textwrap
import time
import zipfile
import zlib

from dataclasses import dataclass
from typing import Any, BinaryIO, Dict, List, Optional, Tuple

CDH_ATTRS = (
    "create_version",
    "create_system",
    "extract_version",
    "reserved",
    "flag_bits",
    "compress_type",
    "date_time",
    "CRC",
    "compress_size",
    "file_size",
    "volume",
    "internal_attr",
    "external_attr",
    "header_offset",
    "filename",
    "extra",
    "comment",
)
LFH_ATTRS = (
    # from LFH
    "extract_version",
    "flag_bits",
    "compress_type",
    "date_time",
    "CRC",
    "compress_size",
    "file_size",
    "filename",
    "extra",
    # extra metadata
    # skip redundant .offset, .size
    "data_descriptor",
    "data_before",
)
LEVELS = (9, 6, 4, 1)


class Error(RuntimeError):
    pass


@dataclass(frozen=True)
class Verbosity:
    additional: bool = True
    lfh_extra: bool = True
    offsets: bool = True
    ordering: bool = True


@dataclass(frozen=True)
class Entry:
    # from LFH
    extract_version: int
    flag_bits: int
    compress_type: int
    date_time: Tuple[int, int, int, int, int, int]
    CRC: int
    compress_size: int
    file_size: int
    filename: str
    extra: bytes
    # extra metadata
    offset: int
    size: int
    data_descriptor: Optional[bytes]
    data_before: Optional[bytes]


@dataclass(frozen=True)
class Time:
    """Unix time from extra field (UT or UX)."""
    mtime: Optional[int] = None
    atime: Optional[int] = None
    ctime: Optional[int] = None


def diff_zip_meta(zipfile1: str, zipfile2: str, verbosity: Verbosity = Verbosity()) -> bool:
    def show(x: Any) -> str:
        return x if isinstance(x, str) and x.isprintable() else repr(x)

    def diff_bytes(a: bytes, b: bytes, attr: str) -> None:
        a_lines = textwrap.wrap(binascii.hexlify(a).decode(), 76)
        b_lines = textwrap.wrap(binascii.hexlify(b).decode(), 76)
        d = difflib.unified_diff(a_lines, b_lines, n=0, lineterm="")
        print(f"  {attr}:")
        for i, line in enumerate(d):
            if i > 2 and not line.startswith("@"):
                print(f"{line[0]}   {line[1:]}")
        if len(a) != len(b):
            print(f"- {attr} size={len(a)}")
            print(f"+ {attr} size={len(b)}")

    def diff_entries(a: List[str], b: List[str]) -> None:
        d = difflib.unified_diff(a, b, n=0, lineterm="")
        for i, line in enumerate(d):
            if i > 2 and not line.startswith("@"):
                print(f"{line[0]} filename={line[1:]}")

    differ = False
    with open(zipfile1, "rb") as fh1, open(zipfile2, "rb") as fh2:
        with zipfile.ZipFile(zipfile1) as zf1, zipfile.ZipFile(zipfile2) as zf2:
            info1 = zf1.infolist()
            info2 = zf2.infolist()
            ftoi1 = {i.filename: i for i in info1}
            ftoi2 = {i.filename: i for i in info2}
            name1 = zf1.namelist()
            name2 = zf2.namelist()
            nset1 = set(name1)
            nset2 = set(name2)
            data_before_cd1, ents1 = read_entries(fh1, ftoi1, verbosity.additional)
            data_before_cd2, ents2 = read_entries(fh2, ftoi2, verbosity.additional)
            print(f"--- {show(zipfile1)}")
            print(f"+++ {show(zipfile2)}")
            if nset1 != nset2:
                differ = True
                rname1 = [show(n) for n in sorted(name1)]
                rname2 = [show(n) for n in sorted(name2)]
                print("entries (sorted by filename):")
                diff_entries(rname1, rname2)
            if verbosity.ordering:
                if name1 != name2:
                    differ = True
                    rname1 = [show(n) for n in name1]
                    rname2 = [show(n) for n in name2]
                    print("entries (unsorted):")
                    diff_entries(rname1, rname2)
                ename1 = list(ents1)
                ename2 = list(ents2)
                if ename1 != ename2 and not (ename1 == name1 and ename2 == name2):
                    differ = True
                    rname1 = [show(n) for n in ename1]
                    rname2 = [show(n) for n in ename2]
                    print("entries (sorted by header_offset):")
                    diff_entries(rname1, rname2)
            if data_before_cd1 != data_before_cd2:
                assert data_before_cd1 is not None
                assert data_before_cd2 is not None
                differ = True
                print("central directory:")
                diff_bytes(data_before_cd1, data_before_cd2, "data_before")
            if zf1.comment != zf2.comment:
                differ = True
                print("end of central directory:")
                diff_bytes(zf1.comment, zf2.comment, "comment")
            for n in sorted(nset1 & nset2):
                diff = []
                for a in CDH_ATTRS:
                    if a == "header_offset" and not verbosity.offsets:
                        continue
                    v1 = getattr(ftoi1[n], a)
                    v2 = getattr(ftoi2[n], a)
                    if v1 != v2:
                        diff.append((a, v1, v2))
                if verbosity.additional:
                    cl1, crc1 = get_compresslevel(fh1, zf1, ftoi1[n])
                    cl2, crc2 = get_compresslevel(fh2, zf2, ftoi2[n])
                    if cl1 != cl2:
                        diff.append(("compresslevel", cl1, cl2))
                    if crc1 != crc2:
                        diff.append(("compress_crc", hex(crc1), hex(crc2)))
                ent1 = ents1[n]
                ent2 = ents2[n]
                if ent1 != ent2:
                    for a in LFH_ATTRS:
                        if a == "extra" and not verbosity.lfh_extra:
                            continue
                        v1 = getattr(ent1, a)
                        v2 = getattr(ent2, a)
                        if v1 != v2:
                            if a in CDH_ATTRS:
                                w1 = getattr(ftoi1[n], a)
                                w2 = getattr(ftoi2[n], a)
                                if v1 == w1 and v2 == w2:
                                    # don't show same difference twice
                                    continue
                            diff.append((f"{a} (entry)", v1, v2))
                if diff:
                    differ = True
                    print(f"entry {show(n)}:")
                    for a, v1, v2 in diff:
                        s = a.split()[0]
                        if s == "data_before":
                            diff_bytes(v1, v2, a)
                        elif s == "extra" and (len(v1) > 16 or len(v2) > 16):
                            diff_bytes(v1, v2, a)
                        else:
                            if s in ("flag_bits", "CRC") or s.endswith("_attr"):
                                v1 = hex(v1)
                                v2 = hex(v2)
                            print(f"- {a}={show(v1)}")
                            print(f"+ {a}={show(v2)}")
                        if s == "extra":
                            lo = a.endswith("(entry)")
                            t1 = extra_field_time(v1, local=lo) or Time()
                            t2 = extra_field_time(v2, local=lo) or Time()
                            for k in ("mtime", "atime", "ctime"):
                                tv1 = getattr(t1, k)
                                tv2 = getattr(t2, k)
                                if tv1 != tv2:
                                    print(f"- {a} {k}={fmt_time(tv1)}")
                                    print(f"+ {a} {k}={fmt_time(tv2)}")
    return differ


def get_compresslevel(fh_raw: BinaryIO, zf: zipfile.ZipFile,
                      info: zipfile.ZipInfo) -> Tuple[Optional[str], int]:
    fh_raw.seek(info.header_offset)
    n, m = struct.unpack("<HH", fh_raw.read(30)[26:30])
    fh_raw.seek(info.header_offset + 30 + m + n)
    ccrc = 0
    size = info.compress_size
    while size > 0:
        ccrc = zlib.crc32(fh_raw.read(min(size, 4096)), ccrc)
        size -= 4096
    levels = []
    if info.compress_type == 8:
        with zf.open(info) as fh:
            comps = {lvl: zlib.compressobj(lvl, 8, -15) for lvl in LEVELS}
            ccrcs = {lvl: 0 for lvl in LEVELS}
            while True:
                data = fh.read(4096)
                if not data:
                    break
                for lvl in LEVELS:
                    ccrcs[lvl] = zlib.crc32(comps[lvl].compress(data), ccrcs[lvl])
            for lvl in LEVELS:
                if ccrc == zlib.crc32(comps[lvl].flush(), ccrcs[lvl]):
                    levels.append(lvl)
            result = "|".join(map(str, levels)) if levels else "unknown"
            return result, ccrc
    elif info.compress_type != 0:
        return "unsupported", ccrc
    return None, ccrc


def read_entries(fh: BinaryIO, ftoi: Dict[str, zipfile.ZipInfo], additional: bool) \
        -> Tuple[Optional[bytes], Dict[str, Entry]]:
    infos = sorted(ftoi.values(), key=lambda i: i.header_offset)
    ents: Dict[str, Entry] = {}
    ent = None
    for p, i in zip([None] + infos[:-1], infos):  # type: ignore[operator]
        prev = ents[p.filename] if p is not None else None
        ents[i.filename] = ent = read_entry(fh, i, prev, additional)
    if additional:
        # FIXME
        cd_offset = zipfile._EndRecData(fh)[zipfile._ECD_OFFSET]    # type: ignore[attr-defined]
        ent_end = ent.offset + ent.size if ent is not None else 0
        fh.seek(ent_end)
        data_before_cd = fh.read(cd_offset - ent_end)
    else:
        data_before_cd = None
    return data_before_cd, ents


# FIXME: non-utf8 filenames?
def read_entry(fh: BinaryIO, info: zipfile.ZipInfo, prev: Optional[Entry],
               additional: bool) -> Entry:
    fh.seek(info.header_offset)
    hdr = fh.read(30)
    if hdr[:4] != b"PK\x03\x04":
        raise Error("Expected local file header signature")
    extract_version, flag_bits, compress_type = struct.unpack("<HHH", hdr[4:10])
    t, d = struct.unpack("<HH", hdr[10:14])
    CRC, compress_size, file_size = struct.unpack("<III", hdr[14:26])
    n, m = struct.unpack("<HH", hdr[26:30])
    date_time = ((d >> 9) + 1980, (d >> 5) & 0xF, d & 0x1F,
                 t >> 11, (t >> 5) & 0x3F, (t & 0x1F) * 2)
    filename = fh.read(n).decode()
    extra = fh.read(m)
    # NB: compress_size in the LFH is zero if there's a data descriptor
    fh.seek(info.compress_size, os.SEEK_CUR)
    if info.flag_bits & 0x08:
        data_descriptor = fh.read(12)
        if data_descriptor[:4] == b"\x50\x4b\x07\x08":
            data_descriptor += fh.read(4)
    else:
        data_descriptor = None
    size = fh.tell() - info.header_offset
    if additional:
        prev_end = prev.offset + prev.size if prev is not None else 0
        fh.seek(prev_end)
        data_before = fh.read(info.header_offset - prev_end)
    else:
        data_before = None
    return Entry(
        extract_version=extract_version,
        flag_bits=flag_bits,
        compress_type=compress_type,
        date_time=date_time,
        CRC=CRC,
        compress_size=compress_size,
        file_size=file_size,
        filename=filename,
        extra=extra,
        offset=info.header_offset,
        size=size,
        data_descriptor=data_descriptor,
        data_before=data_before,
    )


# https://sources.debian.org/src/zip/3.0-12/zip.h/#L217
# https://sources.debian.org/src/zip/3.0-12/zipfile.c/#L6544
def extra_field_time(extra: bytes, local: bool = False) -> Optional[Time]:
    r"""
    Get unix time from extra field (UT or UX).

    >>> t = extra_field_time(b'UT\x05\x00\x01\x00\x00\x00\x00')
    >>> t
    Time(mtime=0, atime=None, ctime=None)
    >>> tuple(time.localtime(t.mtime))
    (1970, 1, 1, 0, 0, 0, 3, 1, 0)
    >>> t = extra_field_time(b'UT\x05\x00\x01\xda\xe9\xe36')
    >>> t
    Time(mtime=920906202, atime=None, ctime=None)
    >>> tuple(time.localtime(t.mtime))
    (1999, 3, 8, 15, 16, 42, 0, 67, 0)
    >>> t = extra_field_time(b'UX\x08\x00\x80h\x9e>|h\x9e>')
    >>> t
    Time(mtime=1050568828, atime=1050568832, ctime=None)
    >>> tuple(time.localtime(t.mtime))
    (2003, 4, 17, 8, 40, 28, 3, 107, 0)
    >>> tuple(time.localtime(t.atime))
    (2003, 4, 17, 8, 40, 32, 3, 107, 0)
    >>> t = extra_field_time(b'UX\x08\x00\xda\xe9\xe36\xda\xe9\xe36')
    >>> t
    Time(mtime=920906202, atime=920906202, ctime=None)
    >>> tuple(time.localtime(t.mtime))
    (1999, 3, 8, 15, 16, 42, 0, 67, 0)
    >>> tuple(time.localtime(t.atime))
    (1999, 3, 8, 15, 16, 42, 0, 67, 0)

    """
    while len(extra) >= 4:
        hdr_id, size = struct.unpack("<HH", extra[:4])
        if size > len(extra) - 4:
            break
        if hdr_id == 0x5455 and size >= 1:
            flags = extra[4]
            if flags & 0x1 and size >= 5:
                mtime = int.from_bytes(extra[5:9], "little")
                atime = ctime = None
                if local:
                    if flags & 0x2 and size >= 9:
                        atime = int.from_bytes(extra[9:13], "little")
                    if flags & 0x4 and size >= 13:
                        ctime = int.from_bytes(extra[13:17], "little")
                return Time(mtime, atime, ctime)
        elif hdr_id == 0x5855 and size >= 8:
            atime = int.from_bytes(extra[4:8], "little")
            mtime = int.from_bytes(extra[8:12], "little")
            return Time(mtime, atime, None)
        extra = extra[size + 4:]
    return None


def fmt_time(t: Optional[int]) -> str:
    return "" if t is None else time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t))


if __name__ == "__main__":
    import argparse
    import sys
    parser = argparse.ArgumentParser(prog="diff-zip-meta.py")
    parser.add_argument("--no-additional", action="store_true")
    parser.add_argument("--no-lfh-extra", action="store_true")
    parser.add_argument("--no-offsets", action="store_true")
    parser.add_argument("--no-ordering", action="store_true")
    parser.add_argument("zipfile1", metavar="ZIPFILE1")
    parser.add_argument("zipfile2", metavar="ZIPFILE2")
    args = parser.parse_args()
    verbosity = Verbosity(
        additional=not args.no_additional,
        lfh_extra=not args.no_lfh_extra,
        offsets=not args.no_offsets,
        ordering=not args.no_ordering,
    )
    if diff_zip_meta(args.zipfile1, args.zipfile2, verbosity=verbosity):
        sys.exit(1)

# vim: set tw=80 sw=4 sts=4 et fdm=marker :
