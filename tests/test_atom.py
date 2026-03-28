from vrel.entity import Atom, Variable


def test_atom():

    a = Atom('likes', Variable('E1'))

    assert a.name == 'likes'

