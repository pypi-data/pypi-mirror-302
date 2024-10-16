from energy_tools.power import q, p
from pytest import approx


def test_q_s_pf():
    s = 1
    pf = 0.9
    assert q(s=s, pf=pf) == approx(0.43588989)


def test_q_p_pf():
    p = 0.9
    pf = 0.9
    assert q(p=p, pf=pf) == approx(0.43588989)


def test_q_s_p():
    s = 1.0
    p = 0.9
    assert q(s=s, p=p) == approx(0.43588989)


def test_q_invalid():
    try:
        q()
        assert False
    except ValueError:
        assert True


def test_q_bad_pf():
    try:
        q(pf=90)
        assert False
    except ValueError:
        assert True


def test_p_s_pf():
    s = 1
    pf = 0.9
    assert p(s=s, pf=pf) == approx(0.9)


def test_p_q_pf():
    q = 0.43588989
    pf = 0.9
    assert p(q=q, pf=pf) == approx(0.9)


def test_p_s_q():
    s = 1.0
    q = 0.43588989
    assert p(s=s, q=q) == approx(0.9)


def test_p_invalid():
    try:
        p()
        assert False
    except ValueError:
        assert True


def test_p_bad_pf():
    try:
        p(pf=90)
        assert False
    except ValueError:
        assert True
