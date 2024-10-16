from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1429() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Person.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Person", string_type), ("first_name", string_type), ("last_name", string_type), ("mid_initials", string_type), ("email", string_type), ("address", string_type), ("phone", string_type), ("fax", string_type), ("comments", string_type), ("roles", string_type), ("affiliation", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Person: str
    first_name: str
    last_name: str
    mid_initials: str
    email: str
    address: str
    phone: str
    fax: str
    comments: str
    roles: str
    affiliation: str

IContext_reflection = _expr1429

def _arrow1444(__unit: None=None) -> IEncodable:
    class ObjectExpr1430(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1431(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:Person")

    class ObjectExpr1432(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:identifier")

    class ObjectExpr1433(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:givenName")

    class ObjectExpr1434(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:familyName")

    class ObjectExpr1435(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:additionalName")

    class ObjectExpr1436(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:email")

    class ObjectExpr1437(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("sdo:address")

    class ObjectExpr1438(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("sdo:telephone")

    class ObjectExpr1439(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("sdo:faxNumber")

    class ObjectExpr1440(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            return helpers_10.encode_string("sdo:disambiguatingDescription")

    class ObjectExpr1441(IEncodable):
        def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
            return helpers_11.encode_string("sdo:jobTitle")

    class ObjectExpr1442(IEncodable):
        def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
            return helpers_12.encode_string("sdo:affiliation")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1430()), ("Person", ObjectExpr1431()), ("orcid", ObjectExpr1432()), ("firstName", ObjectExpr1433()), ("lastName", ObjectExpr1434()), ("midInitials", ObjectExpr1435()), ("email", ObjectExpr1436()), ("address", ObjectExpr1437()), ("phone", ObjectExpr1438()), ("fax", ObjectExpr1439()), ("comments", ObjectExpr1440()), ("roles", ObjectExpr1441()), ("affiliation", ObjectExpr1442())])
    class ObjectExpr1443(IEncodable):
        def Encode(self, helpers_13: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_13))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_13.encode_object(arg)

    return ObjectExpr1443()


context_jsonvalue: IEncodable = _arrow1444()

def _arrow1449(__unit: None=None) -> IEncodable:
    class ObjectExpr1445(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1446(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:Person")

    class ObjectExpr1447(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:name")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1445()), ("Person", ObjectExpr1446()), ("name", ObjectExpr1447())])
    class ObjectExpr1448(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr1448()


context_minimal_json_value: IEncodable = _arrow1449()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"Person\": \"sdo:Person\",\r\n    \"firstName\": \"sdo:givenName\",\r\n    \"lastName\": \"sdo:familyName\",\r\n    \"midInitials\": \"sdo:additionalName\",\r\n    \"email\": \"sdo:email\",\r\n    \"address\": \"sdo:address\",\r\n    \"phone\": \"sdo:telephone\",\r\n    \"fax\": \"sdo:faxNumber\",\r\n    \"comments\": \"sdo:disambiguatingDescription\",\r\n    \"roles\": \"sdo:jobTitle\",\r\n    \"affiliation\": \"sdo:affiliation\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_minimal_json_value", "context_str"]

