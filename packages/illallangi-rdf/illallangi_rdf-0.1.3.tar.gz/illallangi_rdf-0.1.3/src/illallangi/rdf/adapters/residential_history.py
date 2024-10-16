from functools import cached_property
from typing import ClassVar

import diffsync

from illallangi.rdf import RDFClient
from illallangi.rdf.models import Residence


class ResidentialHistoryAdapter(diffsync.Adapter):
    def __init__(
        self,
        github_file_path: str,
        github_repo_name: str,
        github_repo_owner: str,
        github_token: str,
        rdf_root: str,
        *args: list,
        **kwargs: dict,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.github_file_path = github_file_path
        self.github_repo_name = github_repo_name
        self.github_repo_owner = github_repo_owner
        self.github_token = github_token
        self.rdf_root = rdf_root

    Residence = Residence

    top_level: ClassVar = [
        "Residence",
    ]

    type = "rdf_residencehistory"

    @cached_property
    def client(self) -> RDFClient:
        return RDFClient(
            github_file_path=self.github_file_path,
            github_repo_name=self.github_repo_name,
            github_repo_owner=self.github_repo_owner,
            github_token=self.github_token,
            rdf_root=self.rdf_root,
        )

    def load(
        self,
    ) -> None:
        if self.count() > 0:
            return

        for obj in self.client.get_residences():
            self.add(
                Residence(
                    label=obj["label"],
                    start=obj["start"],
                    finish=obj["finish"],
                ),
            )
