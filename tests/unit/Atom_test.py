from vrel.core.constants import E1, E2, E3
from vrel.entity.Atom import Atom, Variable
from vrel.entity.Variable import Variable


def test_atom():

    a = Atom("likes")

    assert a.predicate == "likes"

    a = Atom("likes", E1, "john", "mary")

    assert a.predicate == "likes"
    assert a.arguments[0] == E1
    assert a.arguments[1] == "john"
    assert a.arguments[2] == "mary"
    assert a.arguments == [E1, "john", "mary"]

    # assert str(a) == "A(likes\n    E1\n    'john'\n    'mary')"

    c = a.mod(Atom("much", E2, E1))
    c = c.mod([Atom("location", E3, "here", E1)])

    assert a.modifiers == []
    assert c.modifiers == [Atom("much", E2, E1), Atom("location", E3, "here", E1)]

    # assert (
    #     str(c)
    #     == "A(likes\n    E1\n    'john'\n    'mary'\n    ---\n    A(much\n        E2\n        E1)\n    A(location\n        E3\n        'here'\n        E1))"
    # )
