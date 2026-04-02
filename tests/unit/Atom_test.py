from vrel.core.constants import DUMMY
from vrel.entity.Atom import Atom, Variable
from vrel.entity.Variable import Variable


def test_atom():

    a = Atom(Variable("E1"), "likes")

    assert a.predicate == "likes"

    a = Atom(Variable("E1"), "likes", "john", "mary")

    assert a.variable.name == "E1"
    assert a.predicate == "likes"
    assert a.arguments["ARG0"] == "john"
    assert a.arguments["ARG1"] == "mary"
    assert a.positional_arguments == [Variable("E1"), "john", "mary"]
    assert a.numbered_arguments == ["john", "mary"]
    assert a.named_arguments == {}
    assert str(a) == "(E1 / likes     :ARG0 'john'    :ARG1 'mary')"
    assert repr(a) == "(E1, likes, 'john', 'mary')"

    c = Atom(Variable("E1"), "likes", "john", "mary", {"mod": "much"})

    assert c.arguments["ARG0"] == "john"
    assert c.arguments["ARG1"] == "mary"
    assert c.arguments["mod"] == "much"
    assert c.positional_arguments == [Variable("E1"), "john", "mary"]
    assert c.named_arguments == {"mod": "much"}
    assert str(c) == "(E1 / likes     :ARG0 'john'    :ARG1 'mary'    :mod 'much')"
    assert repr(c) == "(E1, likes, 'john', 'mary', mod='much')"

    d = Atom(Variable("E1"), "likes", {"time": "now"})

    assert d.arguments["time"] == "now"
    assert d.positional_arguments == [Variable("E1")]
    assert d.numbered_arguments == []
    assert d.named_arguments == {"time": "now"}

    e = Atom("likes", "john", "mary", {"time": "now"})

    assert e.variable == DUMMY
    assert e.arguments["time"] == "now"
    assert e.positional_arguments == ["john", "mary"]
    assert e.numbered_arguments == ["john", "mary"]
    assert e.named_arguments == {"time": "now"}

    f = e.add_arguments({"location": "here"})

    assert f.variable == DUMMY
    assert f.arguments["time"] == "now"
    assert f.arguments["location"] == "here"
    assert f.positional_arguments == ["john", "mary"]
    assert f.named_arguments == {"time": "now", "location": "here"}
