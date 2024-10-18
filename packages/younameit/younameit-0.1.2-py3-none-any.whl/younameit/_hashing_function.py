from _hashlib import HASH
from hashlib import sha256
from typing import Any, Union

from younameit import THashingResult


class FailedToHash(ValueError):
    pass


def from_any_to_hash(anything: Union[bytes, str, Any]) -> THashingResult:
    m = sha256()
    if isinstance(anything, bytes):
        blob = anything
    elif isinstance(anything, HASH):
        return anything.digest()
    else:
        try:
            blob = bytes(anything, "utf-8")
        except Exception as error:
            msg = (
                f"Failed to calculate hash out of the argument of type: {type(anything)}.\n"
                f"Unhandled bytes conversion method.\nYou can fix this by passing bytes as an argument.\n"
                f"Got {type(error).__name__!r}:\n{error}\n"
            )
            raise FailedToHash(msg)

    m.update(blob)
    digest_bytes: bytes = m.digest()
    return digest_bytes
