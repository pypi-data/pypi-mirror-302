import diffsync
from partial_date import PartialDate


class Residence(diffsync.DiffSyncModel):
    Label: str

    Country: str
    Finish: PartialDate | None
    Locality: str
    OLC: str
    PostalCode: str
    Region: str
    Start: PartialDate | None
    Street: str

    _modelname = "Residence"
    _identifiers = ("Label",)
    _attributes = (
        "Country",
        "Finish",
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
    ) -> "Residence":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Residence":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Residence":
        raise NotImplementedError
