from vrel.entity.Atom import Atom, Variable
from vrel.entity.Variable import Variable


def test_atom():

    a = Atom(Variable("E1"), "likes")

    assert a.name == "likes"

    a = Atom(Variable("E1"), "likes", "john", "mary")

    assert a.name == "likes"
    assert a.arguments["ARG0"] == "john"
    assert a.arguments["ARG1"] == "mary"

    c = Atom(Variable("E1"), "likes", "john", "mary", {"mod": "much"})

    assert c.arguments["ARG0"] == "john"
    assert c.arguments["ARG1"] == "mary"
    assert c.arguments["mod"] == "much"

    d = Atom(Variable("E1"), "likes", {"time": "now"})

    assert d.arguments["time"] == "now"
