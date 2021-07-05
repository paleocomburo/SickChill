import abc

from sickchill import settings


class Indexer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.name: str = "Generic"
        self.slug: str = "generic"

        self.language: str = settings.INDEXER_DEFAULT_LANGUAGE
        self.indexer: int = settings.INDEXER_DEFAULT
        self.timeout: int = settings.INDEXER_TIMEOUT

    @abc.abstractmethod
    def search(self, name, language=None, exact=False, indexer_id=False):
        raise NotImplementedError

    @abc.abstractmethod
    def get_series_by_id(self, indexerid, language=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_series_by_name(self, name, language=None):
        raise NotImplementedError

    @abc.abstractmethod
    def episodes(self, show, season):
        raise NotImplementedError

    @abc.abstractmethod
    def episode(self, show, season, episode):
        raise NotImplementedError

    @property
    def languages(self):
        raise NotImplementedError

    @property
    def lang_dict(self):
        raise NotImplementedError
