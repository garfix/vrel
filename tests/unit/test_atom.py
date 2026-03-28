from vrel.entity.Atom import Atom, Variable
from vrel.entity.Variable import Variable


def test_atom():

    a = Atom('likes', Variable('E1'))

    assert a.name == 'likes'

