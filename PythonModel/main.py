import matplotlib
import pybamm
from time import time
import numpy as np

def test_model():
    start = time()
    model = pybamm.lithium_ion.DFN()

    sim = pybamm.Simulation(model)

    t_eval = np.linspace(0, 7200, 10000)
    sim.solve(t_eval)

    end = time()-start

    print(end)

    param = model.default_parameter_values
    print(param)
    sim.plot()

def main():
    cell_type = 18650  # input("Input a cell type: ")
    max_voltage = 4.2  # float(input("Input a maximum cell voltage: "))
    min_voltage = 2.5  # float(input("Input a minimum cell voltage: "))
    nom_voltage = 3.6  # float(input("Input a nominal cell voltage: "))
    max_current = 36  # float(input("Input a maximum current: "))
    nom_internal_resistance = 20  # float(input("Input a nominal internal resistance: "))
    ambient_temp = 40  # float(input("Input an ambient temperature: "))
    current_draw = 12.87  # float(input("Input a current draw from load: "))

    test_model()


if __name__ == "__main__":
    main()
