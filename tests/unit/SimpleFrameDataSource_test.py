import unittest

from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.core.constants import DUMMY
from simple_frame_data_source.SimpleModule import SimpleModule


class TestSimpleFrameDataSource(unittest.TestCase):

    def test_simple_frame_datasource(self):

        model = Model([SimpleModule(SimpleFrameDataSource())])

        solver = Solver(model)
        solver.write_atom(Atom("goal", 1))

        self.assertEqual(solver.solve_single(Atom("goal", Variable("E1")), {"B": 5}), [{"B": 5, "E1": 1}])
        self.assertEqual(solver.solve_single(Atom("goal", 1), {"B": 5}), [{"B": 5}])
        self.assertEqual(solver.solve_single(Atom("goal", 2), {}), [])

        solver.write_atom(Atom("goal", [Atom("win", "john", "cup")]))
        solver.write_atom(Atom("goal", [Atom("win", "mary", "championship")]))

        self.assertEqual(
            solver.solve_single(Atom("goal", [Atom("win", Variable("E1"), Variable("E2"))]), {"X": 27}),
            [{"X": 27, "E1": "john", "E2": "cup"}, {"X": 27, "E1": "mary", "E2": "championship"}],
        )
        self.assertEqual(solver.solve_single(Atom("goal", [Atom("win", Variable("E1"), Variable("E1"))]), {}), [])
