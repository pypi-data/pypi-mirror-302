import diffsync


class Airline(diffsync.DiffSyncModel):
    iata: str

    label: str
    icao: str

    _modelname = "Airline"
    _identifiers = ("iata",)
    _attributes = (
        "label",
        "icao",
    )

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Airline":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Airline":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Airline":
        raise NotImplementedError
