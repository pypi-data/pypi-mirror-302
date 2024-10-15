import diffsync
from partial_date import PartialDate


class Course(diffsync.DiffSyncModel):
    Label: str

    Country: str
    Finish: PartialDate | None
    Institution: str
    Locality: str
    OLC: str
    PostalCode: str
    Region: str
    Start: PartialDate | None
    Street: str

    _modelname = "Course"
    _identifiers = ("Label",)
    _attributes = (
        "Country",
        "Finish",
        "Institution",
        "Locality",
        "OLC",
        "PostalCode",
        "Region",
        "Start",
        "Street",
    )

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Course":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Course":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Course":
        raise NotImplementedError
