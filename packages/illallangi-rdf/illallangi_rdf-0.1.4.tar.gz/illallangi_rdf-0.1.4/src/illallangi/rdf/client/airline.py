import rdflib


class AirlineMixin:
    def get_airlines_query(
        self,
        iata: list[str] | None = None,
    ) -> str:
        return f"""
SELECT ?label ?iata ?icao WHERE {{
    VALUES (?value) {{ ( "{'" ) ( "'.join([i.upper() for i in iata])}" ) }}
    ?href ip:airlineIataCode ?value.
    ?href rdfs:label ?label .
    ?href ip:airlineIataCode ?iata .
    ?href ip:airlineIcaoCode ?icao .
    ?href a ic:airline .
}}
"""

    def get_airlines(
        self,
        *args: list,
        **kwargs: dict,
    ) -> rdflib.Graph:
        result = self.graph.query(
            self.get_airlines_query(
                *args,
                **kwargs,
            ),
        )

        return [
            {str(k): str(b[str(k)]) if str(k) in b else None for k in result.vars}
            for b in result.bindings
        ]
