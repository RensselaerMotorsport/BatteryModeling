import matplotlib
import pybamm
from time import time
import numpy as np
import matplotlib.pyplot as plt


def test_model():
    start = time()
    options = {"thermal": "x-full"}
    model = pybamm.lithium_ion.DFN(options)
    solns = []

    param = model.default_parameter_values
    param['Ambient temperature [K]'] = 316.483
    param['Cell cooling surface area [m2]'] = 0.00367
    param['Cell volume [m3]'] = 1.65e-05
    param['Initial temperature [K]'] = 316.483
    param['Nominal cell capacity [A.h]'] = 2.6
    param['Open-circuit voltage at 0% SOC [V]'] = 2.5
    param['Open-circuit voltage at 100% SOC [V]'] = 4.2
    param['Current function [A]'] = 2

    sim = pybamm.Simulation(model, parameter_values=param)

    t_eval = np.linspace(0, 3600)
    sim.solve(t_eval)

    end = time()-start

    solns.append(sim._solution)



    # Now create a QuickPlot object with the adjusted solutions
    quick_plot = pybamm.QuickPlot(solns, ["X-averaged cell temperature [K]"])
    quick_plot.dynamic_plot()

    # print(solns[0]["Cell temperature [K]"].entries)
    # print(solns[0]["Voltage [V]"].entries)
    # print(solns[0].get_data_dict())

    # plt.plot(solns[0]["Voltage [V]"].entries)


    # Plot the solutions dynamically
    # new_plot = pybamm.dynamic_plot(solns, ["X-averaged cell temperature [K]"])
    print(type(quick_plot.variables[("X-averaged cell temperature [K]",)][0][0].base_variables[0]))
    '''
    <class 'pybamm.expression_tree.binary_operators.Addition'>
    
    This is the type of the data printed above, so thats where you will find the class (i.e. the binary_operators
    file in the PyBaMM folders)
    '''



    # quick_plot.plots[("Voltage [V]", )][0][0].show()

    plt.show()
    print(end)


def main():
    # cell_type = 18650  # input("Input a cell type: ")
    # max_voltage = 4.2  # float(input("Input a maximum cell voltage: "))
    # min_voltage = 2.5  # float(input("Input a minimum cell voltage: "))
    # nom_voltage = 3.6  # float(input("Input a nominal cell voltage: "))
    # max_current = 36  # float(input("Input a maximum current: "))
    # nom_internal_resistance = 20  # float(input("Input a nominal internal resistance: "))
    # ambient_temp = 40  # float(input("Input an ambient temperature: "))
    # current_draw = 12.87  # float(input("Input a current draw from load: "))

    test_model()


if __name__ == "__main__":
    main()


"""
Attempt 2: 

# this attempt was an attempt at taking in all the variables we 
# wanted to use before actually learning how to use the API
# There were several errors with trying to actually use the inputs, so I scrapped it and started fresh
import pybamm

def run_battery_model(cell_type, max_voltage, min_voltage, nom_voltage, 
                      nom_internal_resistance, max_current, ambient_temp, 
                      current_draw):
    # Create a PyBaMM parameter set for the given cell type
    chemistry = pybamm.parameter_sets.Chen2020
    parameter_values = pybamm.ParameterValues(chemistry=chemistry, values={})


    # Set user-defined parameters
    parameter_values.update(
        {
            "Maximum voltage [V]": max_voltage,
            "Minimum voltage [V]": min_voltage,
            "Nominal cell voltage [V]": nom_voltage,
            "Nominal internal resistance [Ohm]": nom_internal_resistance,
            "Maximum current [A]": max_current,
            "Ambient temperature [K]": ambient_temp,
            "Current function [A]": current_draw,
        }
    )

    # Create the battery model
    model = pybamm.lithium_ion.DFN()

    # Set parameter values
    model.parameter_values = parameter_values

    # Solve the model
    solution = pybamm.CasadiSolver().solve(model)

    # Extract desired outputs
    battery_temp = solution["X-averaged cell temperature [K]"](0)
    internal_resistance = solution["X-averaged total heating [W]"](0) / (current_draw ** 2)

    return battery_temp, internal_resistance

def main():
    cell_type = input("Input a cell type: ")
    max_voltage = float(input("Input a maximum cell voltage: "))
    min_voltage = float(input("Input a minimum cell voltage: "))
    nom_voltage = float(input("Input a nominal cell voltage: "))
    nom_internal_resistance = float(input("Input a nominal internal resistance: "))
    max_current = float(input("Input a maximum current: "))
    ambient_temp = float(input("Input an ambient temperature: "))
    current_draw = float(input("Input a current draw from load: "))

    battery_temp, internal_resistance = run_battery_model(cell_type, max_voltage, 
                                                          min_voltage, nom_voltage, 
                                                          nom_internal_resistance, 
                                                          max_current, ambient_temp, 
                                                          current_draw)

    print("Battery Temperature:", battery_temp, "K")
    print("Internal Resistance:", internal_resistance, "Ohm")

if __name__ == "__main__":
    main()





# Our eventual implementation of the package we are building
# is to incorporate it into our lap sim.  Unfortunately, the API we are using doesnt have 
# the functionality to feed us real time data over an ongoing simulation (at least that I have found yet,
# however I'm still looking).  Therefore, I was testing to see how long it would take to check the battery 
# status at each time step, to see if it was impractical to just do it that way.  My conclusion is that the 
# solution wouldn't be that elegant, but also isn't too slow, so as a last resort we can do it that way.
Attempt 3:
import pybamm

# Define the battery model
model = pybamm.lithium_ion.DFN()

# Create a simulation object
sim = pybamm.Simulation(model)

# Define simulation time and time steps
t_eval = np.linspace(0, race_time, num_time_steps)

# Iterate over time steps
for t in t_eval:
    # Set current profile based on race conditions
    current = get_current_profile(t)
    
    # Set inputs for the simulation
    sim.specs["operating mode"] = "current"
    sim.specs["current function"] = current
    
    # Solve the model for the current time step
    sim.solve(t_eval=[t, t + dt])
    
    # Collect data at each time step
    voltage = sim.solution["Terminal voltage"]
    temperature = sim.solution["Cell temperature"]
    
    # Perform analysis or visualization with the collected data

# Visualize results or perform further analysis

"""