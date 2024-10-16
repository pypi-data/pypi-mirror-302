from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IRequiredGetter, IOptionalGetter, string, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.data import Data
from ...Core.data_context import (DataContext__get_Explication, DataContext__get_Unit, DataContext__get_ObjectType, DataContext__get_Description, DataContext__get_GeneratedBy, DataContext__get_Label, DataContext, DataContext__ctor_Z780A8A2A)
from ...Core.ontology_annotation import OntologyAnnotation
from ..data import (encoder as encoder_1, decoder as decoder_1)
from ..encode import try_include
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)

__A_ = TypeVar("__A_")

def encoder(dc: DataContext) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], dc: Any=dc) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2401(oa: OntologyAnnotation, dc: Any=dc) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2402(oa_1: OntologyAnnotation, dc: Any=dc) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2405(oa_2: OntologyAnnotation, dc: Any=dc) -> IEncodable:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow2407(value: str, dc: Any=dc) -> IEncodable:
        class ObjectExpr2406(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2406()

    def _arrow2411(value_2: str, dc: Any=dc) -> IEncodable:
        class ObjectExpr2409(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2409()

    def _arrow2415(value_4: str, dc: Any=dc) -> IEncodable:
        class ObjectExpr2414(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2414()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("data", encoder_1(dc)), try_include("explication", _arrow2401, DataContext__get_Explication(dc)), try_include("unit", _arrow2402, DataContext__get_Unit(dc)), try_include("objectType", _arrow2405, DataContext__get_ObjectType(dc)), try_include("description", _arrow2407, DataContext__get_Description(dc)), try_include("generatedBy", _arrow2411, DataContext__get_GeneratedBy(dc)), try_include("label", _arrow2415, DataContext__get_Label(dc))]))
    class ObjectExpr2417(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], dc: Any=dc) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2417()


def _arrow2426(get: IGetters) -> DataContext:
    data: Data
    object_arg: IRequiredGetter = get.Required
    data = object_arg.Field("data", decoder_1)
    def _arrow2418(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("explication", OntologyAnnotation_decoder)

    def _arrow2419(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("unit", OntologyAnnotation_decoder)

    def _arrow2420(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("objectType", OntologyAnnotation_decoder)

    def _arrow2422(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("label", string)

    def _arrow2424(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("description", string)

    def _arrow2425(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("generatedBy", string)

    return DataContext__ctor_Z780A8A2A(data.ID, data.Name, data.DataType, data.Format, data.SelectorFormat, _arrow2418(), _arrow2419(), _arrow2420(), _arrow2422(), _arrow2424(), _arrow2425(), data.Comments)


decoder: Decoder_1[DataContext] = object(_arrow2426)

__all__ = ["encoder", "decoder"]

