import matplotlib
import pybamm
from time import time
import numpy as np
import matplotlib.pyplot as plt


# Function to get user input with default values
def get_input(prompt, default):
    while True:
        user_input = input(prompt)
        if user_input == '':
            return default
        try:
            return eval(user_input)
        except SyntaxError:
            print("Invalid input, please try again.")


def single_cell_model(amb, surf, cell_vol, init_temp, cap, min_volt, max_volt, curr, time_to_run):
    """
    Runs a battery model on a single cell based on the following given inputs and plots them

    :param curr: current in amps
    :param amb: Ambient Temp in C
    :param surf: Cell cooling surface area in meters sqrd
    :param cell_vol: Cell volume in meters cubed
    :param init_temp: Initial Temp in C
    :param cap: Nominal Cell capacity in amp hours
    :param min_volt: minimum voltage in volts
    :param max_volt: maximum voltage in volts
    :param time_to_run: Time over which to run the model in minutes
    :return: none
    """
    # sets up model
    options = {"thermal": "x-full"}
    model = pybamm.lithium_ion.DFN(options)

    # sets up parameters
    param = model.default_parameter_values
    param.update(
        {
            'Ambient temperature [K]': amb + 273.15,
            'Cell cooling surface area [m2]': surf,
            'Cell volume [m3]': cell_vol,
            'Initial temperature [K]': init_temp + 273.15,
            'Nominal cell capacity [A.h]': cap,
            'Open-circuit voltage at 0% SOC [V]': min_volt,
            'Open-circuit voltage at 100% SOC [V]': max_volt,
            "Current function [A]": curr,
        }
    )

    # builds sim
    sim = pybamm.Simulation(model, parameter_values=param)

    # creates an array of time steps to run over
    t_eval = np.linspace(0, time_to_run * 60)
    sim.solve(t_eval)

    # print(sim.solution["X-averaged cell temperature [K]"].entries)
    # print(sim.solution["Time [s]"].entries)

    # # get the SOC values
    # soc = sim.solution['State of Charge']
    #
    # # calculate the time at which SOC reaches 0%
    # discharge_time = sim.solution['Time [s]'].entries[soc.entries.argmin()]
    #
    # print("Discharge Time:", discharge_time / 60, "minutes")

    # solve and plot
    print(f"\n\n\nFinal voltage: {sim.solution['Voltage [V]'].entries[-1]:.4f} V\n"
          f"Final Temperature: {sim.solution['X-averaged cell temperature [K]'].entries[-1] - 273.15:.4f} C")

    quick_plot = pybamm.QuickPlot(sim, ["X-averaged cell temperature [K]", "Voltage [V]",
                                        "Total heating [W.m-3]", "Current [A]", 'Discharge capacity [A.h]',
                                        "X-averaged negative particle surface concentration", ])
    quick_plot.dynamic_plot()


# def pack_model(amb, surf, cell_vol, init_temp, cap, min_volt, max_volt, curr, time_to_run):
#     """
#     Runs a battery model on a single cell based on the following given inputs and plots them
#
#     :param curr: current in amps
#     :param amb: Ambient Temp in C
#     :param surf: Cell cooling surface area in meters sqrd
#     :param cell_vol: Cell volume in meters cubed
#     :param init_temp: Initial Temp in C
#     :param cap: Nominal Cell capacity in amp hours
#     :param min_volt: minimum voltage in volts
#     :param max_volt: maximum voltage in volts
#     :param time_to_run: Time over which to run the model in minutes
#     :return: none
#     """
#     # sets up model
#     options = {"thermal": "x-full"}
#     model = pybamm.lithium_ion.DFN(options)
#
#     # sets up parameters
#     param = model.default_parameter_values
#     param.update(
#         {
#             'Ambient temperature [K]': amb + 273.15,
#             'Cell cooling surface area [m2]': surf,
#             'Cell volume [m3]': cell_vol,
#             'Initial temperature [K]': init_temp + 273.15,
#             'Nominal cell capacity [A.h]': cap,
#             'Open-circuit voltage at 0% SOC [V]': min_volt,
#             'Open-circuit voltage at 100% SOC [V]': max_volt,
#             "Current function [A]": curr,
#         }
#     )
#
#     # Build the single-cell model
#     single_cell = pybamm.lithium_ion.SPM(options)
#
#     # Assemble the full pack model
#     geometry = pybamm.battery_geometry()
#     _pack_model = (pybamm.lithium_ion.MPM(geometry, single_cell, options))
#
#     # Connect cells in series to form the pack
#     pack = pybamm.SeriesModel(570 * [_pack_model])
#
#     # Set up simulation
#     sim = pybamm.Simulation(pack, parameter_values=param)
#
#     # Create an array of time steps to run over
#     t_eval = np.linspace(0, time_to_run * 60)
#     sim.solve(t_eval)
#
#     # Print final voltage and temperature
#     print(f"\n\n\nFinal voltage: {sim.solution['Terminal voltage [V]'].entries[-1]:.4f} V\n"
#           f"Final temperature: {sim.solution['X-averaged cell temperature [K]'].entries[-1] - 273.15:.4f} C")
#
#     # Plot results
#     quick_plot = pybamm.QuickPlot(sim, ["X-averaged cell temperature [K]", "Terminal voltage [V]",
#                                         "Total heating [W.m-3]", "Current [A]", 'Discharge capacity [A.h]',
#                                         "X-averaged negative particle surface concentration"])
#     quick_plot.dynamic_plot()


def main():
    amb_temp = get_input("Ambient temperature [C] (default is 43.333): ", 43.333)
    surf_area = get_input("Cell cooling surface area [m2] (default is 0.00367): ", 0.00367)
    cell_vol = get_input("Cell volume [m3] (default is 1.65e-05): ", 1.65e-05)
    init_temp = get_input("Initial temperature [C] (default is 43.333): ", 43.333)
    nom_cap = get_input("Nominal cell capacity [A.h] (default is 2.6): ", 2.6)
    min_volt = get_input("Open-circuit voltage at 0% SOC [V] (default is 2.5): ", 2.5)
    max_volt = get_input("Open-circuit voltage at 100% SOC [V] (default is 4.2): ", 4.2)
    curr = get_input("Current function [A] (default is 0.68): ", 0.68)
    t = get_input("Enter a number of minutes to run for (default is 60 mins): ", 60)

    single_cell_model(amb_temp, surf_area, cell_vol, init_temp, nom_cap, min_volt, max_volt, curr, t)


if __name__ == "__main__":
    main()
