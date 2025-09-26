from __future__ import annotations

from doku_gpt.abstact_root_folder import AbstractRootFolder
from doku_gpt.finder.copier import Copier
from pathlib import Path

class PrepareDokuHandler(AbstractRootFolder):

    PREPARE_DESTINATION = Path("/tmp/doku_gpt_prepare")

    def copy(self) -> None:
        copier = Copier(
            root_folder=self.root_folder, excluded_folders=self.excluded_folders, excluded_files=self.excluded_files
        )

        copier.prepare()
