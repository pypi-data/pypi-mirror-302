import rdflib


class AirportMixin:
    def get_airports_query(
        self,
        iata: list[str] | None = None,
    ) -> str:
        return f"""
SELECT ?label ?iata ?icao WHERE {{
    VALUES (?value) {{ ( "{'" ) ( "'.join([i.upper() for i in iata])}" ) }}
    ?href ip:airportIataCode ?value.
    ?href rdfs:label ?label .
    ?href ip:airportIataCode ?iata .
    ?href ip:airportIcaoCode ?icao .
    ?href a ic:airport .
}}
"""

    def get_airports(
        self,
        *args: list,
        **kwargs: dict,
    ) -> rdflib.Graph:
        result = self.graph.query(
            self.get_airports_query(
                *args,
                **kwargs,
            ),
        )

        return [
            {str(k): str(b[str(k)]) if str(k) in b else None for k in result.vars}
            for b in result.bindings
        ]
