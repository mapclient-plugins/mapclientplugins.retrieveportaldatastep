import zlib
from base64 import urlsafe_b64decode as b64d


def undo_change(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))


DEFAULT_VALUE = undo_change(b'eNqrcPIv8kzLiwop8wosyU9yz7eI8AgqC8lI8Y10D6koSQMAv6ULpg==').decode()

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json; charset=utf-8",
}
