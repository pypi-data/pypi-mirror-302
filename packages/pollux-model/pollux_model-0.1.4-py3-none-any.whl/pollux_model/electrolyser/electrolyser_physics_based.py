from pollux_model.model_abstract import Model
import numpy as np
from thermo.chemical import Chemical
from scipy.optimize import root_scalar


class ElectrolyserDeGroot(Model):
    """ Abstract base class for simulation models

        Model classes implement a discrete state space model
        The state of the model is maintained outside the model object
    """

    def __init__(self):
        """ Model initialization
        """
        super().__init__()

    def update_parameters(self, parameters):
        """ To update model parameters

        Parameters
        ----------
        parameters : dict
            parameters dict as defined by the model
        """
        for key, value in parameters.items():
            self.parameters[key] = value

        if self.parameters['cell_type'] == 'alk_ref_cell':
            self.parameters['power_single_cell'] = 6222
        elif self.parameters['cell_type'] == 'low_power_cell':
            self.parameters['power_single_cell'] = 4000
        elif self.parameters['cell_type'] == 'medium_power_cell':
            self.parameters['power_single_cell'] = 10000
        elif self.parameters['cell_type'] == 'high_power_cell':
            self.parameters['power_single_cell'] = 16000

        self.parameters['N_cells'] = np.ceil(self.parameters['capacity']
                                             / self.parameters['power_single_cell'])

    def initialize_state(self, x):
        """ generate an initial state based on user parameters """
        pass

    # def calculate_output(self, u):
    #     """calculate output based on input u"""
    #     self._calc_prod_rates(u)
    
    def calculate_output(self):
        """calculate output based on input u"""
        u = self.input
        self._calc_prod_rates(u)

    def _calc_prod_rates(self, u):
        T_cell = u['T_cell']
        p_cathode = u['p_cathode']
        p_anode = u['p_anode']
        p_0_H2O = u['p_0_H2O']
        power_input = u['power_input']

        # PVT properties of H2, O2 and water at current pressure and temperature.
        PVT_H2 = Chemical('hydrogen')
        PVT_O2 = Chemical('oxygen')
        PVT_H2O = Chemical('water')

        PVT_H2.calculate(T=T_cell, P=p_cathode)
        PVT_O2.calculate(T=T_cell, P=p_anode)
        PVT_H2O.calculate(T=T_cell, P=p_0_H2O)

        self.parameters['power_cell_real'] = power_input / self.parameters[
            'N_cells']  # * self.power_multiplier
        # todo: the power multiplier
        # can be extended to include active and non active stacks,
        # for now just give the independent stacks

        self._calc_i_cell()
        # wteta faraday assume to be constant
        # Production rates [mol/s]

        I_cell_array = self._calc_i_cell()

        self.output['prod_rate_H2'] = (self.parameters['N_cells']) * I_cell_array / (
                2 * self.parameters['Faraday_const']) * self.parameters['eta_Faraday_array']
        self.output['prod_rate_O2'] = (self.parameters['N_cells']) * I_cell_array / (
                4 * self.parameters['Faraday_const']) * self.parameters['eta_Faraday_array']
        self.output['prod_rate_H2O'] = (self.parameters['N_cells']) * I_cell_array / (
                2 * self.parameters['Faraday_const'])

        # Massflows [kg/s].
        self.output['massflow_H2'] = self.output['prod_rate_H2'] * PVT_H2.MW * 1e-3
        self.output['massflow_O2'] = self.output['prod_rate_O2'] * PVT_O2.MW * 1e-3
        self.output['massflow_H2O'] = self.output['prod_rate_H2O'] * PVT_H2O.MW * 1e-3

        # Densities [kg/m^3].
        self.output['rho_H2'] = PVT_H2.rho
        self.output['rho_O2'] = PVT_O2.rho
        self.output['rho_H2O'] = PVT_H2O.rho

        # Flowrates [m^3/s].
        self.output['flowrate_H2'] = self.output['massflow_H2'] / self.output['rho_H2']
        self.output['flowrate_O2'] = self.output['massflow_O2'] / self.output['rho_O2']
        self.output['flowrate_H2O'] = (self.output['massflow_H2O'] /
                                       self.output['rho_H2O'])

        # Integrate massflows to obtain masses of H2, O2 and H20 in this period [kg].
        # Note: it assumes constant operating conditions in the time-step
        self.output['mass_H2'] = self.output['massflow_H2'] * self.parameters['delta_t']
        self.output['mass_O2'] = self.output['massflow_O2'] * self.parameters['delta_t']
        self.output['mass_H2O'] = self.output['massflow_H2O'] * self.parameters['delta_t']

    def _calc_i_cell(self):
        I_current_sol = root_scalar(
            self._root_I_cell, bracket=[1.0, 30000],
            method='brentq',
            args=(
                self.parameters['power_cell_real'],
            )
        )
        return I_current_sol.root

    def _root_I_cell(self, I_cell, power_cell):
        self.state['E_total_cell'] = \
            self._compute_potentials(
                I_cell, self.parameters['A_cell'])
        root_expr = power_cell / (self.state['E_total_cell']) - I_cell
        return root_expr

    def _compute_potentials(self, I_cell, A_cell):
        # A_cell = 0.436
        I_cell_in = I_cell / 1e4 / A_cell
        # Voltage efficiency WITH COEFFICIENTS
        E_total_cel = (-0.160249069 * I_cell_in ** 4 + 0.734073995 * I_cell_in ** 3 -
                       1.168543948 * I_cell_in ** 2 + 1.048496283 * I_cell_in + 1.46667069)
        return E_total_cel
