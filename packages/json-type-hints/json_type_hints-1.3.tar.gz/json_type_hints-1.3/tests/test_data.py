from dataclasses import dataclass


@dataclass
class MyClass1:
    prop1: int
    prop2: tuple[str, bytes]


@dataclass
class MyClass2:
    prop1: list[MyClass1]
    prop2: str


@dataclass
class MyClass3:
    prop1: int = 1


@dataclass
class MyClass4:
    value: int = 4

    def __eq__(self, other):
        return False


CLS_NAME_1 = "MyClass1"
CLS_NAME_2 = "MyClass2"
CLS_NAME_3 = "MyClass3"
TYPE_DICT_CLS1 = {CLS_NAME_1: MyClass1}
TYPE_DICT_CLS2 = {CLS_NAME_2: MyClass2}
TYPE_DICT_PARTIAL = {CLS_NAME_2: MyClass2, CLS_NAME_3: MyClass3}
TYPE_DICT_FULL = {CLS_NAME_1: MyClass1, CLS_NAME_2: MyClass2, CLS_NAME_3: MyClass3}
CLASS_1_OBJ_1 = MyClass1(prop1=1, prop2=("bytes1", b"\x01"))
CLASS_1_OBJ_2 = MyClass1(prop1=2, prop2=("bytes2", b"\x01\x00"))
CLASS_3_OBJ_1 = MyClass3()
CLASS_4_OBJ_1 = MyClass4()
CLASS_2_OBJ_1 = MyClass2(prop1=[CLASS_1_OBJ_1, CLASS_1_OBJ_2, CLASS_3_OBJ_1], prop2="cls2")
INPUT_DICT = {"key1": 1, "key2": CLASS_2_OBJ_1}
INPUT_DICT_2 = INPUT_DICT.copy()
INPUT_DICT_2["key1"] = CLASS_4_OBJ_1
DUMPS_STR = (
    '{"key1":1,"key2":{"__type__":"MyClass2","__data__":{"prop1":[{"__type__":"MyClass1",'
    '"__data__":{"prop1":1,"prop2":{"__type__":"tuple","__data__":["bytes1",'
    '{"__type__":"bytes","__data__":"AQ=="}]}}},{"__type__":"MyClass1",'
    '"__data__":{"prop1":2,"prop2":{"__type__":"tuple","__data__":["bytes2",'
    '{"__type__":"bytes","__data__":"AQA="}]}}},{"__type__":"MyClass3"}],"prop2":"cls2"}}}'
)
DUMPS_STR_2 = DUMPS_STR.replace('"key1":1', f'"key1":{CLASS_4_OBJ_1.value}')
LOADS_DEFAULT_ONLY = {
    "key1": 1,
    "key2": {
        "__type__": CLS_NAME_2,
        "__data__": {
            "prop1": [
                {"__type__": CLS_NAME_1, "__data__": {"prop1": 1, "prop2": ("bytes1", b"\x01")}},
                {
                    "__type__": CLS_NAME_1,
                    "__data__": {"prop1": 2, "prop2": ("bytes2", b"\x01\x00")},
                },
                {"__type__": CLS_NAME_3},
            ],
            "prop2": "cls2",
        },
    },
}
LOADS_CLS_1_ONLY = {
    "key1": 1,
    "key2": {
        "__type__": CLS_NAME_2,
        "__data__": {
            "prop1": [CLASS_1_OBJ_1, CLASS_1_OBJ_2, {"__type__": CLS_NAME_3}],
            "prop2": "cls2",
        },
    },
}
LOADS_STR_BAD_PROP = f'{{"__type__":"{CLS_NAME_1}","__data__":{{"bad_prop":1}}}}'
