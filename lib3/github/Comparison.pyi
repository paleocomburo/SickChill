from typing import Any, Dict, List

from github.Commit import Commit
from github.File import File
from github.GithubObject import CompletableGithubObject

class Comparison(CompletableGithubObject):
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def ahead_by(self) -> int: ...
    @property
    def base_commit(self) -> Commit: ...
    @property
    def behind_by(self) -> int: ...
    @property
    def commits(self) -> List[Commit]: ...
    @property
    def diff_url(self) -> str: ...
    @property
    def files(self) -> List[File]: ...
    @property
    def html_url(self) -> str: ...
    @property
    def merge_base_commit(self) -> Commit: ...
    @property
    def patch_url(self) -> str: ...
    @property
    def permalink_url(self) -> str: ...
    @property
    def status(self) -> str: ...
    @property
    def total_commits(self) -> int: ...
    @property
    def url(self) -> str: ...