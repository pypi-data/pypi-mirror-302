import json

import ggps

from tests.helpers.unit_test_helper import UnitTestHelper

# pytest -v tests/test_counter.py


def test_counter():
    c = ggps.Counter()
    c.increment(150)
    c.increment(155)
    c.increment(155)
    c.increment(160)
    c.increment(160)
    c.decrement(160)

    assert c.get_value(150) == 1
    assert c.get_value(155) == 2
    assert c.get_value(160) == 1
    assert c.most_frequent() == 155
    assert c.get_data() == {"150": 1, "155": 2, "160": 1}

    c.decrement("x")
    assert c.get_value("x") == -1

    assert c.get_value("not_present") == 0
