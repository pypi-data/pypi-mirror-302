import json

import ggps

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_trackpoint.py


def test_str():
    t = ggps.Trackpoint()
    assert str(t) == "<Trackpoint values count:1>"


def test_to_numeric():
    t = ggps.Trackpoint()

    try:
        t.set("bad_int", "nine")
        t.to_int("bad_int")
        assert "exception not thrown in to_int" == ""
    except:
        assert 1 == 1

    try:
        t.set("bad_float", "nine point nine")
        t.to_float("bad_float")
        assert "exception not thrown in to_float" == ""
    except:
        assert 1 == 1

    t.set("elapsedtime", "kkyy66")
    t.calculate_elapsedseconds()
    assert t.values["elapsedseconds"] == 0

    t.set("elapsedtime", "1:1:2")
    t.calculate_elapsedseconds()
    assert t.values["elapsedseconds"] == 3662


def test_repr():
    t = ggps.Trackpoint()
    t.set("lang", "python")
    t.set(None, "python")
    j = repr(t)
    obj = json.loads(j)
    assert obj["type"] == "Trackpoint"
    assert obj["lang"] == "python"


def test_get():
    t = ggps.Trackpoint()
    t.set("lang", "python")
    assert t.get("lang") == "python"
    assert t.get("xxx") == ""
    assert t.get("zzz", "zero") == "zero"
