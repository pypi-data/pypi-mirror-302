import os

STRING_ENCODING = "windows-1252"  # "utf-8"
DELETE_FLAG = b"\x91\x8b\x4a\x5c\xbc\xdb\x4f\x14\x63\x23\x7f\x78\xa6\x95\x0d\x27"
MIN_DELETE_LENGTH = 6

NULL_INT = -2147483647
NULL_DOUBLE = -1.7976931348623158e308
NULL_FLOAT = -3.4028234663852886e38
NULL_SHORT = -32767
NULL_TINY = 255

def _get_ffb_dictionary(ffb_file: str) -> str:
    return os.path.splitext(ffb_file)[0] + ".dcb"