from trx_utils import (
    add_0x_prefix,
    encode_hex,
    is_boolean,
    is_string,
    is_integer,
    remove_0x_prefix,
    decode_hex
)

from trx_utils.decorators import validate_conversion_arguments
from trx_utils.encoding import big_endian_to_int
from trx_utils.typing.misc import (
    Primitives,
    HexStr
)


@validate_conversion_arguments
def to_hex(
        primitive: Primitives = None, hexstr: HexStr = None, text: str = None
) -> HexStr:
    """
    Auto converts any supported value into its hex representation.
    Trims leading zeros, as defined in:
    https://github.com/ethereum/wiki/wiki/JSON-RPC#hex-value-encoding
    """
    if hexstr is not None:
        return HexStr(add_0x_prefix(hexstr.lower()))

    if text is not None:
        return HexStr(encode_hex(text.encode("utf-8")))

    if is_boolean(primitive):
        return HexStr("0x1") if primitive else HexStr("0x0")

    if isinstance(primitive, (bytes, bytearray)):
        return HexStr(encode_hex(primitive))
    elif is_string(primitive):
        raise TypeError(
            "Unsupported type: The primitive argument must be one of: bytes,"
            "bytearray, int or bool and not str"
        )

    if is_integer(primitive):
        return HexStr(hex(primitive))

    raise TypeError(
        "Unsupported type: '{0}'.  Must be one of: bool, str, bytes, bytearray"
        "or int.".format(repr(type(primitive)))
    )


@validate_conversion_arguments
def to_int(
    primitive: Primitives = None, hexstr: HexStr = None, text: str = None
) -> int:
    """
    Converts value to its integer representation.
    Values are converted this way:
     * primitive:
       * bytes, bytearrays: big-endian integer
       * bool: True => 1, False => 0
     * hexstr: interpret hex as integer
     * text: interpret as string of digits, like '12' => 12
    """
    if hexstr is not None:
        return int(hexstr, 16)
    elif text is not None:
        return int(text)
    elif isinstance(primitive, (bytes, bytearray)):
        return big_endian_to_int(primitive)
    elif isinstance(primitive, str):
        raise TypeError("Pass in strings with keyword hexstr or text")
    else:
        return int(primitive)


@validate_conversion_arguments
def to_bytes(
        primitive: Primitives = None, hexstr: HexStr = None, text: str = None
) -> bytes:
    if is_boolean(primitive):
        return b"\x01" if primitive else b"\x00"
    elif isinstance(primitive, bytearray):
        return bytes(primitive)
    elif isinstance(primitive, bytes):
        return primitive
    elif is_integer(primitive):
        return to_bytes(hexstr=to_hex(primitive))
    elif hexstr is not None:
        if len(hexstr) % 2:
            # type check ignored here because casting an Optional arg to str is not possible
            hexstr = "0x0" + remove_0x_prefix(hexstr)  # type: ignore
        return decode_hex(hexstr)
    elif text is not None:
        return text.encode("utf-8")
    raise TypeError(
        "expected a bool, int, byte or bytearray in first arg, or keyword of hexstr or text"
    )
