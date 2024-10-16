import ggps


def test_author():
    assert ggps.AUTHOR == "Chris Joakim <christopher.joakim@gmail.com>"


def test_version():
    assert ggps.VERSION == "0.5.0"


def test_default_run_walk_separator_cadence():
    assert ggps.DEFAULT_RUN_WALK_SEPARATOR_CADENCE == 150
