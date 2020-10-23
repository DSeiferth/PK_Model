import unittest
import pkmodel as pk
import matplotlib
import numpy as np


class PipelineTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    Init calls solver and so the output of solver is also tested.
    """

    def test_build_iv(self):
        """
        Tests the whole pipeline can be built;
        - make model
        - make protocol
        - make solution
        for an intravenous dosing protocol.
        """

        model = pk.Model(Vc=2., Vps=[1, 2], Qps=[3, 4], CL=3.)

        dosing = pk.Protocol(dose_amount=10, subcutaneous=False,
                             k_a=0.3, continuous=True,
                             continuous_period=[0.2, 0.6],
                             instantaneous=True, dose_times=[0, .1, .2, .3])

        solution = pk.Solution(model=model, protocol=dosing)
        self.assertEqual(solution.sol.y.shape[0], solution.model.size)
        self.assertEqual(solution.sol.y.shape[1], solution.t_eval.shape[0])
        self.assertIsInstance(solution.t_eval, np.ndarray)
        self.assertIsInstance(solution.y0, np.ndarray)

    def test_build_sc(self):
        """
        Tests the whole pipeline can be built;
        - make model
        - make protocol
        - make solution
        for an subcataneous dosing protocol.
        """

        model = pk.Model(Vc=2., Vps=[1, 2], Qps=[3, 4], CL=3.)

        dosing = pk.Protocol(dose_amount=10, subcutaneous=True,
                             k_a=0.3, continuous=True,
                             continuous_period=[0.2, 0.6],
                             instantaneous=True, dose_times=[0, .1, .2, .3])

        solution = pk.Solution(model=model, protocol=dosing)
        self.assertEqual(solution.sol.y.shape[0], solution.model.size + 1)
        self.assertEqual(solution.sol.y.shape[1], solution.t_eval.shape[0])
        self.assertIsInstance(solution.t_eval, np.ndarray)
        self.assertIsInstance(solution.y0, np.ndarray)

    def test_all_zeros(self):
        """
        Tests the whole pipeline;
        - make model
        - make protocol
        - make solution
        for an intravenous dosing protocol.
        """

        model = pk.Model(Vc=2., Vps=[], Qps=[], CL=3.)

        dosing = pk.Protocol(dose_amount=0, subcutaneous=True,
                             k_a=0.3, continuous=False,
                             continuous_period=[],
                             instantaneous=True, dose_times=[])

        solution = pk.Solution(model=model, protocol=dosing)
        sol = solution.sol

        assert(not((sol.y != 0).any()))

    def test_plot_pipeline(self):
        """
        Tests the whole pipeline;
        - make model
        - make protocol
        - make solution
        - plot solution
        for an intravenous dosing protocol.
        """

        model = pk.Model(Vc=2., Vps=[], Qps=[], CL=3.)

        dosing = pk.Protocol(dose_amount=10, subcutaneous=True,
                             k_a=0.3, continuous=True,
                             continuous_period=[0.2, 0.6],
                             instantaneous=True,
                             dose_times=[0, .1, .2, .3])

        solution = pk.Solution(model=model, protocol=dosing)
        sol_fig = solution.generate_plot()
        self.assertIsInstance(sol_fig, matplotlib.figure.Figure)
