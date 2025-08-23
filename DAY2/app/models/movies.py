_db = {}
_id_counter = 0


class MovieModel:
    def __init__(self, id: int, title: str, playtime: int, genre: str):
        self.id = id
        self.title = title
        self.playtime = playtime
        self.genre = genre

    @classmethod
    def create(cls, title: str, playtime: int, genre: str):
        global _id_counter
        _id_counter += 1
        new_movie = cls(id=_id_counter, title=title, playtime=playtime, genre=genre)
        _db[new_movie.id] = new_movie
        return new_movie

    @classmethod
    def all(cls):
        return list(_db.values())

    @classmethod
    def search(cls, title: str | None = None, genre: str | None = None):
        results = []
        for movie in _db.values():
            match = True
            if title is not None and title.lower() not in movie.title.lower():
                match = False
            if genre is not None and genre.lower() not in movie.genre.lower():
                match = False

            if match:
                results.append(movie)

        return results

    @classmethod
    def get_by_id(cls, movie_id: int):
        return _db.get(movie_id)

    def update(self, title: str, playtime: int, genre: str):
        self.title = title
        self.playtime = playtime
        self.genre = genre

    @classmethod
    def delete(cls, movie_id: int):
        if movie_id in _db:
            del _db[movie_id]
            return True
        return False