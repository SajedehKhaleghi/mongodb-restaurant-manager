import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import restaurant_manager as rm


class FakeResult:
    def __init__(self, n):
        self.deleted_count = n


class FakeCollection:
    """Tiny in-memory stand-in for a PyMongo collection (no MongoDB needed)."""

    def __init__(self):
        self.docs = []

    def replace_one(self, flt, doc, upsert=False):
        for i, d in enumerate(self.docs):
            if all(d.get(k) == v for k, v in flt.items()):
                self.docs[i] = dict(doc)
                return
        if upsert:
            self.docs.append(dict(doc))

    def find(self, flt=None):
        flt = flt or {}
        return iter([d for d in self.docs if all(d.get(k) == v for k, v in flt.items())])

    def delete_one(self, flt):
        for i, d in enumerate(self.docs):
            if all(d.get(k) == v for k, v in flt.items()):
                del self.docs[i]
                return FakeResult(1)
        return FakeResult(0)


def test_import_is_idempotent_search_and_delete():
    data = rm.read_json_file(rm.DEFAULT_JSON)
    assert len(data) == 15
    col = FakeCollection()
    rm.add_restaurants(col, data)
    rm.add_restaurants(col, data)           # second import must not duplicate
    assert len(col.docs) == 15
    assert len(rm.search_by_name(col, "112 Restaurant")) == 1
    assert rm.search_by_name(col, "nope") == []
    assert rm.delete_by_code(col, 1) == 1
    assert rm.delete_by_code(col, 1) == 0   # already deleted
    assert len(col.docs) == 14


if __name__ == "__main__":
    test_import_is_idempotent_search_and_delete()
    print("test passed")
