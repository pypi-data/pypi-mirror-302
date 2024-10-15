from typing import ClassVar

import diffsync

from illallangi.rdf import RDFClient
from illallangi.rdf.models import Airline, Airport


class AviationAdapter(diffsync.Adapter):
    Airline = Airline
    Airport = Airport

    top_level: ClassVar = [
        "Airline",
        "Airport",
    ]

    type = "rdf_aviation"

    def load(
        self,
        airline_iata: list[str] | None = None,
        airport_iata: list[str] | None = None,
    ) -> None:
        airline_iata = airline_iata or []
        airport_iata = airport_iata or []

        for obj in self.client.get_airlines(
            airline_iata,
        ):
            self.add(
                Airline(
                    iata=obj["iata"],
                    label=obj["label"],
                    icao=obj["icao"],
                ),
            )

        for obj in self.client.get_airports(
            airport_iata,
        ):
            self.add(
                Airport(
                    iata=obj["iata"],
                    label=obj["label"],
                    icao=obj["icao"],
                ),
            )

    def __init__(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        super().__init__()
        self.client = RDFClient(
            *args,
            **kwargs,
        )
