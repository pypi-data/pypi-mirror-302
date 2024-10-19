import numpy as np
import xarray as xr

from dartsflash.pyflash import PyFlash
from dartsflash.mixtures import ConcentrationUnits as cu
from dartsflash.libflash import VdWP
from dartsflash.libflash import RootFinding


class HyFlash(PyFlash):
    hydrate_eos: dict = {}

    def add_hydrate_eos(self, name: str, eos: VdWP):
        """
        Method to add hydrate EoS to map
        """
        self.hydrate_eos[name] = eos

    def calc_df(self, pressure, temperature, composition, phase: str = "sI"):
        """
        Method to calculate fugacity difference between fluid mixture and hydrate phase

        :param pressure: Pressure [bar]
        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param phase: Hydrate phase type
        """
        self.f.evaluate(pressure, temperature, composition)
        flash_results = self.f.get_flash_results()
        V = np.array(flash_results.nu)
        x = np.array(flash_results.X).reshape(len(V), self.ns)
        f0 = self.flash_params.eos_params["AQ"].eos.fugacity(pressure, temperature, x[0, :])

        fwH = self.hydrate_eos[phase].fw(pressure, temperature, f0)
        df = fwH - f0[self.H2O_idx]
        return df

    def calc_equilibrium_pressure(self, temperature: float, composition: list, p_init: float, phase: str = "sI",
                                  dp: float = 10., min_p: float = 1., max_p: float = 500., tol_f: float = 1e-15, tol_x: float = 1e-15):
        """
        Method to calculate equilibrium pressure between fluid phases and hydrate phase at given T, z

        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param p_init: Initial guess for equilibrium pressure [bar]
        :param phase: Hydrate phase type
        :param dp: Step size to find pressure bounds
        :param min_p: Minimum pressure [bar]
        :param tol_f: Tolerance for objective function
        :param tol_x: Tolerance for variable
        """
        # Find bounds for pressure
        p_min, p_max = p_init, p_init
        if self.calc_df(p_init, temperature, composition, phase) > 0:
            # Hydrate fugacity larger than fluid fugacity
            while True:
                p_max = min(max_p, p_max+dp)
                if self.calc_df(p_max, temperature, composition, phase) < 0:
                    break
                p_min = min(max_p, p_min+dp)
                if p_min == max_p:
                    print("Equilibrium pressure above p_max", temperature)
                    return None
        else:
            # Hydrate fugacity smaller than fluid fugacity
            while True:
                p_min = max(min_p, p_min-dp)
                if self.calc_df(p_min, temperature, composition, phase) > 0:
                    break
                p_max = max(min_p, p_max-dp)
                if p_max == min_p:
                    print("Equilibrium pressure below p_min", temperature)
                    return None

        pres = (p_min + p_max) / 2

        # Define objective function for Brent's method
        def obj_fun(pres):
            df = self.calc_df(pres, temperature, composition, phase)
            return -df

        rf = RootFinding()
        error = rf.brent_method(obj_fun, pres, p_min, p_max, tol_f, tol_x)

        if not error == 1:
            return rf.getx()
        else:
            print("Not converged", temperature)
            return None

    def calc_equilibrium_temperature(self, pressure: float, composition: list, t_init: float, phase: str = "sI",
                                     dT: float = 10., min_T: float = 250., tol_f: float = 1e-15, tol_x: float = 1e-15):
        """
        Method to calculate equilibrium temperature between fluid phases and hydrate phase at given P, z

        :param pressure: Pressure [bar]
        :param composition: Feed mole fractions [-]
        :param t_init: Initial guess for equilibrium temperature [K]
        :param phase: Hydrate phase type
        :param dT: Step size to find pressure bounds
        :param min_T: Minimum temperature [K]
        :param tol_f: Tolerance for objective function
        :param tol_x: Tolerance for variable
        """
        # Find bounds for temperature
        T_min, T_max = t_init, t_init
        if self.calc_df(pressure, t_init, composition, phase) < 0:
            while True:
                T_max += dT
                if self.calc_df(pressure, T_max, composition) > 0:
                    break
                T_min += dT
        else:
            while True:
                T_min = max(min_T, T_min - dT)
                if self.calc_df(pressure, T_min, composition, phase) < 0:
                    break
                T_max = max(min_T, T_max - dT)
                if T_max == min_T:
                    print("Equilibrium temperature below T_min", pressure)
                    return None

        temp = (T_min + T_max) / 2

        # Define objective function for Brent's method
        def obj_fun(temp):
            df = self.calc_df(pressure, temp, composition, phase)
            return df

        rf = RootFinding()
        error = rf.brent_method(obj_fun, temp, T_min, T_max, tol_f, tol_x)

        if not error == 1:
            return rf.getx()
        else:
            print("Not converged", pressure)
            return None

    def evaluate_equilibrium(self, state_spec: dict, compositions: dict, mole_fractions: bool,
                             concentrations: dict = None, concentration_unit: cu = cu.MOLALITY, print_state: str = None):
        """
        Method to calculate equilibrium pressure/temperature between fluid phases and hydrate phase at given P/T, z

        :param state_spec: Dictionary containing state specification. Either pressure or temperature should be None
        :param compositions: Dictionary containing variable dimensions
        :param mole_fractions: Switch for mole fractions in state
        :param concentrations: Dictionary of concentrations
        :param concentration_unit: Unit for concentration. 0/MOLALITY) molality (mol/kg H2O), 1/WEIGHT) Weight fraction (-)
        :param print_state: Switch for printing state and progress
        """
        state_spec["pressure"] = np.array([state_spec["pressure"]]) if state_spec["pressure"] is None else state_spec["pressure"]
        state_spec["temperature"] = np.array([state_spec["temperature"]]) if state_spec["temperature"] is None else state_spec["temperature"]
        assert state_spec["pressure"][0] is None or state_spec["temperature"][0] is None, \
            "Please only provide range of pressures OR temperatures, the other one will be computed"
        calc_pressure = state_spec["pressure"][0] is None
        output_arrays = {"pres": 1} if calc_pressure else {"temp": 1}

        self.prev = 1. if calc_pressure else 273.15
        def evaluate(state):
            if calc_pressure:
                result = self.calc_equilibrium_pressure(state[1], state[2:], self.prev, phase="sI")
                output_data = {"pres": lambda pressure=result: pressure}
            else:
                result = self.calc_equilibrium_temperature(state[0], state[2:], self.prev, phase="sI")
                output_data = {"temp": lambda temperature=result: temperature}
            self.prev = result if result is not None else self.prev

            return output_data

        return self.evaluate_full_space(state_spec=state_spec, compositions=compositions, mole_fractions=mole_fractions,
                                        evaluate=evaluate, output_arrays=output_arrays, concentrations=concentrations,
                                        concentration_unit=concentration_unit, print_state=print_state)

    def calc_properties(self, pressure: list, temperature: list, composition: list, guest_idx: list,
                        number_of_curves: int = 1, phase: str = "sI"):
        """
        Method to calculate hydrate phase properties at given P,T,z:
        - Hydration number nH [-]
        - Density rhoH [kg/m3]
        - Enthalpy of hydrate formation/dissociation dH [kJ/kmol]

        :param pressure: Pressure [bar]
        :param temperature: Temperature [K]
        :param composition: Feed mole fractions [-]
        :param guest_idx: Index of guest molecule(s)
        :param phase: Hydrate phase type
        :param number_of_curves: Number of equilibrium curves
        """
        from darts.physics.properties.eos_properties import EoSEnthalpy, VdWPDensity, VdWPEnthalpy
        densH = VdWPDensity(self.hydrate_eos[phase], self.mixture.comp_data.Mw)
        enthH = VdWPEnthalpy(self.hydrate_eos[phase])
        enthV = EoSEnthalpy(self.flash_params.eos_params["SRK"].eos)
        enthA = EoSEnthalpy(self.flash_params.eos_params["AQ"].eos)

        pressure = np.tile(pressure, (number_of_curves, 1)) if not isinstance(pressure[0], (list, np.ndarray)) else pressure
        temperature = np.tile(temperature, (number_of_curves, 1)) if not isinstance(temperature[0], (list, np.ndarray)) else temperature
        nH = [[] for i in range(number_of_curves)]
        rhoH = [[] for i in range(number_of_curves)]
        dH = [[] for i in range(number_of_curves)]

        for i in range(number_of_curves):
            len_data = len(pressure[i])
            assert len(temperature[i]) == len_data

            nH[i] = [None] * len_data
            rhoH[i] = [None] * len_data
            dH[i] = [None] * len_data

            for j in range(len_data):
                if not pressure[i][j] is None or not temperature[i][j] is None:
                    self.calc_df(pressure[i][j], temperature[i][j], composition[i])
                    flash_results = self.f.get_flash_results()
                    V = np.array(flash_results.nu)
                    x = np.array(flash_results.X).reshape(len(V), self.ns)
                    xH = self.hydrate_eos[phase].xH()

                    # Calculate hydration number nH
                    nH[i][j] = 1. / xH[guest_idx] - 1.

                    # Density rhoH
                    rhoH[i][j] = densH.evaluate(pressure[i][j], temperature[i][j], xH)

                    # Enthalpy of hydrate formation/dissociation
                    Hv = enthV.evaluate(pressure[i][j], temperature[i][j], x[1, :])
                    Ha = nH[i][j] * enthA.evaluate(pressure[i][j], temperature[i][j], x[0, :])
                    Hh = enthH.evaluate(pressure[i][j], temperature[i][j], xH) * (nH[i][j] + 1)
                    dH[i][j] = (Hv + Ha - Hh) * 1e-3  # H_hyd < H_fluids -> enthalpy release upon formation

        return nH, rhoH, dH
