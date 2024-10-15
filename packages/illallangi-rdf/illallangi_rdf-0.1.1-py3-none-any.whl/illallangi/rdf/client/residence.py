import rdflib
from partial_date import PartialDate


class ResidenceMixin:
    def get_residences_query(
        self,
    ) -> str:
        return f"""
PREFIX i: <http://data.coley.au/rdf/entity#>
PREFIX ip: <http://data.coley.au/rdf/property#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX v: <http://www.w3.org/2006/vcard/ns#>


SELECT ?Start ?Finish ?Label ?Street ?Locality ?Region ?PostalCode ?Country ?OLC WHERE {{
    <{ self.rdf_root }> ip:residedAt ?residedAt .
    OPTIONAL {{ ?residedAt ip:startTime ?Start }} .
    OPTIONAL {{ ?residedAt ip:endTime ?Finish }} .
    ?residedAt ip:atResidence ?atResidence .

    OPTIONAL {{ ?atResidence rdfs:label ?Label . }}

    OPTIONAL {{ ?atResidence v:Address ?address
        OPTIONAL {{ ?address v:street-address ?Street }}
        OPTIONAL {{ ?address v:locality ?Locality }}
        OPTIONAL {{ ?address v:region ?Region }}
        OPTIONAL {{ ?address v:postal-code ?PostalCode }}
        OPTIONAL {{ ?address v:country-name ?Country }}
    }}
    OPTIONAL {{ ?atResidence ip:olc ?OLC }} .
}}
"""

    def get_residences(
        self,
        *args: list,
        **kwargs: dict,
    ) -> rdflib.Graph:
        result = self.graph.query(
            self.get_residences_query(
                *args,
                **kwargs,
            ),
        )

        return sorted(
            [
                {
                    **{
                        str(k): b[str(k)].value if str(k) in b else None
                        for k in result.vars
                    },
                    "Start": PartialDate(b["Start"].value)
                    if "Start" in b and b["Start"].value not in ["Unknown"]
                    else None,
                    "Finish": PartialDate(b["Finish"].value)
                    if "Finish" in b and b["Finish"].value not in ["Unknown"]
                    else None,
                }
                for b in result.bindings
            ],
            key=lambda x: str(x["Start"]),
        )
