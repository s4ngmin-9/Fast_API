# app/models/users.py

_db = {}
_id_counter = 0


class UserModel:
    def __init__(self, user_id: int, username: str, age: int, gender):
        self.id = user_id
        self.username = username
        self.age = age
        self.gender = gender

    @classmethod
    def create(cls, username: str, age: int, gender):
        global _id_counter
        _id_counter += 1
        new_user = cls(user_id=_id_counter, username=username, age=age, gender=gender)
        _db[new_user.id] = new_user
        return new_user

    @classmethod
    def get_by_id(cls, user_id: int):
        return _db.get(user_id)

    @classmethod
    def all(cls):
        return list(_db.values())

    def update(self, user_data):
        if user_data.username is not None:
            self.username = user_data.username
        if user_data.age is not None:
            self.age = user_data.age

    @classmethod
    def delete(cls, user_id: int):
        if user_id in _db:
            del _db[user_id]
            return True
        return False

    @classmethod
    def search(cls, username: str | None = None, age: int | None = None, gender=None):
        results = []
        for user in _db.values():
            match = True
            if username is not None and username.lower() not in user.username.lower():
                match = False
            if age is not None and user.age != age:
                match = False
            if gender is not None and user.gender != gender:
                match = False

            if match:
                results.append(user)

        return results