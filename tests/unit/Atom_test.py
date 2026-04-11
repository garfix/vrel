from vrel.entity.Atom import Atom, Variable
from vrel.entity.Variable import Variable


def test_atom():

    a = Atom("likes")

    assert a.predicate == "likes"

    a = Atom("likes", Variable("E1"), "john", "mary")

    assert a.predicate == "likes"
    assert a.arguments[0] == Variable("E1")
    assert a.arguments[1] == "john"
    assert a.arguments[2] == "mary"
    assert a.numbered_arguments == [Variable("E1"), "john", "mary"]
    assert a.named_arguments == {}
    assert str(a) == "A(likes\n    :0 E1\n    :1 'john'\n    :2 'mary')"
    assert repr(a) == "A(likes, E1, 'john', 'mary')"

    c = Atom("likes", Variable("E1"), "john", "mary", {"mod": "much"})

    assert c.arguments[0] == Variable("E1")
    assert c.arguments[1] == "john"
    assert c.arguments[2] == "mary"
    assert c.numbered_arguments == [Variable("E1"), "john", "mary"]
    assert c.named_arguments == {"mod": "much"}
    assert str(c) == "A(likes\n    :0 E1\n    :1 'john'\n    :2 'mary'\n    :mod 'much')"
    assert repr(c) == "A(likes, E1, 'john', 'mary', mod='much')"

    f = c.add_arguments({"location": "here"})

    assert f.arguments["mod"] == "much"
    assert f.arguments["location"] == "here"
    assert f.named_arguments == {"mod": "much", "location": "here"}
