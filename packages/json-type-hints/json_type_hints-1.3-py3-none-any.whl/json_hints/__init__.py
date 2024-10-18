import base64
import json
from collections.abc import Callable
from typing import Any

from .encoder import ExtendedJSONEncoder


def dumps(
    obj: Any,
    *,
    encode_types: Callable[[Any], Any] | None = None,
    default: Callable[[Any], Any] | None = None,
    separators: tuple[str, str] = (",", ":"),
) -> str:
    """
    Serialize ``obj`` to a JSON formatted ``str``. Encode ``tuple`` to
    ``{'__type__': 'tuple', '__data__': [...]}`` and ``bytes`` to
    ``{'__type__': 'bytes', '__data__': 'base64 encoded bytes'}``.
    :param obj: a Python object.
    :param encode_types: a function that should convert ``obj`` into a
        ``{'__type__': 'name', '__data__': ...}`` dict or return it unchanged. ``'__data__'`` can
        be omitted. If present, it will be encoded recursively. For types where a simple convertion
        to a JSON serializable type is needed, ``default`` must be used instead.
    :param default: a function that should return a serializable version of ``obj`` or raise
        ``TypeError``. The default simply raises ``TypeError``.
    :param separators: ``(item_separator, key_separator)`` tuple. The default is ``(',', ':')``.
    :return: ``obj`` as a JSON formatted ``str``.
    """
    return json.dumps(
        obj=obj,
        cls=ExtendedJSONEncoder,
        default=default,
        separators=separators,
        encode_types=encode_types,
    )


def loads(
    s: str | bytes | bytearray,
    *,
    raise_on_unknown: bool = True,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    hinted_types: dict[str, type] | None = None,
) -> Any:
    """
    Deserialize a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document
    to a Python object. Decode objects encoded to ``{'__type__': 'name', '__data__': ...}`` dict
    if ``'__type__'`` is ``'tuple'`` or ``'bytes'``.
    :param s: a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document.
    :param raise_on_unknown: ``True`` - a ``TypeError`` will be raised when a ``'__type__'`` can't
        be decoded (not in ``hinted_types`` and not decoded by ``object_hook``), ``False`` - the
        ``{'__type__': 'name', '__data__': ...}`` dict will be left as is.
    :param object_hook: an optional function that will be called with the result of any object
        literal decode (a ``dict``). The return value of ``object_hook`` will be used instead of the
        ``dict``. This feature can be used to implement custom decoders (e.g. for types encoded to
        ``{'__type__': 'name', '__data__': ...}`` dict).
    :param hinted_types: a ``{'name': class}`` dict, used to decode
        ``{'__type__': 'name', '__data__': ...}`` dict. Objects will be created by unpacking
        ``'__data__'`` into keyword arguments, or using it as a positional argument,
        if ``'__data__'`` is not a dict. When there is no ``'__data__'``, the object will be
        created without any arguments.
    :return: a Python object.
    """

    def decode_hinted(obj):
        if object_hook:
            backup = obj
            obj = object_hook(obj)
            if obj != backup:
                return obj
        if "__type__" not in obj:
            return obj
        _type = obj["__type__"]
        _data = obj.get("__data__", {})
        _hinted_types = {"tuple": tuple}
        if hinted_types:
            _hinted_types.update(hinted_types)
        try:
            if _type == "bytes":
                return base64.b64decode(_data)
            if _type in _hinted_types:
                if isinstance(_data, dict):
                    return _hinted_types[_type](**_data)
                return _hinted_types[_type](_data)
        except TypeError as e:
            raise TypeError(f"invalid '__data__' for '__type__':'{_type}'. {e}")
        if not raise_on_unknown:
            return obj
        raise TypeError(f"'__type__':'{_type}' is not a supported data type")

    return json.loads(s=s, object_hook=decode_hinted)
