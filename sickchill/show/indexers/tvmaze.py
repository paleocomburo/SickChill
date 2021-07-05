from typing import TYPE_CHECKING

import tvmaze.api
from tvmaze.expections import TvMazeException

import sickchill.start

from .base import Indexer
from .wrappers import ExceptionDecorator

if TYPE_CHECKING:
    from sickchill.tv import TVEpisode, TVShow


class TVMAZE(Indexer):
    def __init__(self):
        super(TVMAZE, self).__init__()
        self.name = "tvmaze"
        self.slug = "tvmaze"
        self.icon = "images/indexers/tvmaze.png"
        self.api: "tvmaze.api.Api" = tvmaze.api.Api()

    def search(self, name: str, language=None):
        return self.api.search.shows(name)

    def get_series_by_id(self, indexerid: int, language=None):
        return self.api.show.get(indexerid)

    def get_series_by_name(self, name: str, language=None):
        return self.api.search.single_show(name)

    def episodes(self, show: "TVShow", season: int):
        return self.api.show.seasons(show.indexerid)

    def episode(self, show: "TVShow", season: int, episode: int):
        return self.api.show.episode_by_number(show.indexerid, season, episode)

    @property
    def languages(self):
        pass

    @property
    def lang_dict(self):
        pass

    def get_show_by_tvdb_id(self, show: "TVShow"):
        if show.indexer == sickchill.indexer.TVDB:
            return self.api.search.lookup_show(lookup_option="thetvdb", lookup_id=show.indexerid)
        return None

    def get_show_by_imdb_id(self, show: "TVShow"):
        if show.imdb_id:
            return self.api.search.lookup_show(lookup_option="imdb", lookup_id=show.imdb_id)
        return None

    def get_akas(self, show: "TVShow"):
        series = None
        for attempt in self.get_show_by_tvdb_id, self.get_show_by_imdb_id:
            try:
                series = attempt(show)
                if series:
                    break
            except TvMazeException:
                pass

        if series:
            try:
                return {aka.name for aka in sickchill.indexer["tvmaze"].api.show.akas(series.id)}
            except TvMazeException:
                pass

        return series
