import rdflib
from partial_date import PartialDate


class CourseMixin:
    def get_courses_query(
        self,
    ) -> str:
        return f"""
SELECT ?Start ?Finish ?Label ?Institution ?Street ?Locality ?Region ?PostalCode ?Country ?OLC WHERE {{
    <{ self.rdf_root }> ip:attendedCourse ?attendedCourse .
    OPTIONAL {{ ?attendedCourse ip:startTime ?Start }} .
    OPTIONAL {{ ?attendedCourse ip:endTime ?Finish }} .
    ?attendedCourse rdfs:label ?Label .
    ?attendedCourse ip:atInstitution ?atInstitution .

    OPTIONAL {{ ?atInstitution rdfs:label ?Institution . }}

    OPTIONAL {{ ?atInstitution v:Address ?address
        OPTIONAL {{ ?address v:street-address ?Street }}
        OPTIONAL {{ ?address v:locality ?Locality }}
        OPTIONAL {{ ?address v:region ?Region }}
        OPTIONAL {{ ?address v:postal-code ?PostalCode }}
        OPTIONAL {{ ?address v:country-name ?Country }}
    }}
    OPTIONAL {{ ?atInstitution ip:olc ?OLC }} .
}}
"""

    def get_courses(
        self,
        *args: list,
        **kwargs: dict,
    ) -> rdflib.Graph:
        result = self.graph.query(
            self.get_courses_query(
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
