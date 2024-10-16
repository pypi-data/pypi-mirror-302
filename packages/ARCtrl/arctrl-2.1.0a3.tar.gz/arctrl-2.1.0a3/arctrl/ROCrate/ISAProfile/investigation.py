from __future__ import annotations
from typing import Any
from ...fable_modules.dynamic_obj.dyn_obj import (set_property, set_optional_property)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from .dataset import (Dataset, Dataset_reflection)

def _expr1253() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Investigation", None, Investigation, Dataset_reflection())


class Investigation(Dataset):
    def __init__(self, id: str, identifier: Any=None, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, has_part: Any | None=None, headline: Any | None=None, mentions: Any | None=None, url: Any | None=None, description: Any | None=None) -> None:
        super().__init__(id, "Investigation")
        this: FSharpRef[Investigation] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("identifier", identifier, this.contents)
        set_optional_property("citation", citation, this.contents)
        set_optional_property("comment", comment, this.contents)
        set_optional_property("creator", creator, this.contents)
        set_optional_property("dateCreated", date_created, this.contents)
        set_optional_property("dateModified", date_modified, this.contents)
        set_optional_property("datePublished", date_published, this.contents)
        set_optional_property("hasPart", has_part, this.contents)
        set_optional_property("headline", headline, this.contents)
        set_optional_property("mentions", mentions, this.contents)
        set_optional_property("url", url, this.contents)
        set_optional_property("description", description, this.contents)


Investigation_reflection = _expr1253

def Investigation__ctor_Z3E174868(id: str, identifier: Any=None, citation: Any | None=None, comment: Any | None=None, creator: Any | None=None, date_created: Any | None=None, date_modified: Any | None=None, date_published: Any | None=None, has_part: Any | None=None, headline: Any | None=None, mentions: Any | None=None, url: Any | None=None, description: Any | None=None) -> Investigation:
    return Investigation(id, identifier, citation, comment, creator, date_created, date_modified, date_published, has_part, headline, mentions, url, description)


__all__ = ["Investigation_reflection"]

