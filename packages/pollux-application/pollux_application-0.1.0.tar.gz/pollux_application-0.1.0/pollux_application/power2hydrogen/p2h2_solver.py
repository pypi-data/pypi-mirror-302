from pollux_application.application_abstract import ApplicationAbstract
from pollux_model.power_supply_demand.power_supply import PowerSupply
from pollux_model.power_supply_demand.power_demand import PowerDemand
from pollux_model.hydrogen_demand.hydrogen_demand import HydrogenDemand
from pollux_model.splitter.splitter import Splitter
from pollux_model.adder.adder import Adder
from pollux_model.electrolyser.electrolyser_physics_based import ElectrolyserDeGroot
from pollux_model.gas_storage.hydrogen_tank_model import HydrogenTankModel
from pollux_model.solver.solver import Solver
from pollux_model.solver.step_function import step_function
import numpy as np
import matplotlib.pyplot as plt


class Power2Hydrogen(ApplicationAbstract):
    def __init__(self):
        super().__init__()

        # Parameters
        self.time_horizon = 24
        self.step_size_control = 2
        self.time_vector = []
        self.time_vector_control = []
        self.splitter1_control = []

        # Input profiles
        self.power_supply_profile = []
        self.power_demand_profile = []
        self.hydrogen_demand_profile = []
        self.splitter1_control_profile = []

        # Components
        self.power_supply = None
        self.power_demand = None
        self.hydrogen_demand = None
        self.splitter1 = None
        self.electrolyser = None

    def init_parameters(self):
        # TODO: update parameters from external input

        # Check if the division of the time_horizon over the step_size_control is an integer
        if self.time_horizon % self.step_size_control != 0:
            raise ValueError(
                f"time_horizon ({self.time_horizon}) is not divisible by step_size_control ({self.step_size_control})"
            )
        self.time_vector = np.linspace(0, self.time_horizon, 97)
        # self.time_vector_control = np.linspace(0, 24, 25)  # From t=0 to t=24 with 25 steps
        self.time_vector_control = np.linspace(
            0, self.time_horizon, self.time_horizon // self.step_size_control + 1
        )

        # Initialize component objects
        # POWER SUPPLY
        self.power_supply_profile = lambda t: 10e6 * (2 + np.sin(t))  # Watt
        self.power_supply = PowerSupply(self.power_supply_profile)

        # POWER DEMAND
        self.power_demand_profile = lambda t: 10e6  # Watt
        self.power_demand = PowerDemand(self.power_demand_profile)

        # HYDROGEN DEMAND
        self.hydrogen_demand_profile = lambda t: 200 / 3600  # kg/s
        self.hydrogen_demand = HydrogenDemand(self.hydrogen_demand_profile)

        # SPLITTER 1
        # a * (0.5 + 0.5*np.sin(t)) + b  varies between b and b+a
        self.splitter1_control_profile = lambda t: 0.5 * (0.5 + 0.5 * np.sin(t)) + 0.4
        # splitter1_control_profile = lambda t: 0.8/(2 + np.sin(t))
        self.splitter1_control = lambda t: step_function(
            t,
            self.step_size_control,
            self.splitter1_control_profile(self.time_vector_control),
        )
        self.splitter1 = Splitter(self.splitter1_control)

        # ELECTROLYSER
        self.electrolyser = ElectrolyserDeGroot()

        # SPLITTER 2
        splitter2_control_profile = (
            lambda t: 0.5 * 0.1 * (1 + np.sin(t)) + 0.5
        )  # varies 0.5 and 0.5 + 0.1
        # splitter2 = Splitter(splitter2_control_profile)
        splitter2_control = lambda t: step_function(
            t,
            self.step_size_control,
            splitter2_control_profile(self.time_vector_control),
        )
        splitter2 = Splitter(splitter2_control)

        # HYDROGE STORAGE
        hydrogen_storage_profile = (
            lambda t: 100 / 3600 * (t + 1) / (t + 1)
        )  # control variable kg/s: the hydrogen mass flow produced from the storage
        # hydrogen_storage = HydrogenTankModel(mass_flow_out_profile)
        self.hydrogen_storage_control = lambda t: step_function(
            t,
            self.step_size_control,
            hydrogen_storage_profile(self.time_vector_control),
        )
        self.hydrogen_storage = HydrogenTankModel(self.hydrogen_storage_control)

        # ADDER
        self.adder = Adder()

        # SOLVER OBJECT
        self.solver = Solver(self.time_vector)

    def get_input(self, u, param):
        # TODO: retrieve input from GUI
        u = dict()
        u["T_cell"] = 273.15 + 40  # cell temperature in K
        u["p_cathode"] = 10e5  # cathode pressure in Pa
        u["p_anode"] = 10e5  # anode pressure in Pa
        u["p_0_H2O"] = 10e5  # Pa
        # u['power_input'] = 2118181.8181  # input power in Watt
        self.electrolyser.input = u

        # Update electrolyser parameters
        param = dict()
        param["eta_Faraday_array"] = 1  # just a constant, in reality is a variable
        param["Faraday_const"] = 96485.3329  # Faraday constant [(s A)/mol]
        param["delta_t"] = (
            np.diff(self.time_vector)[0] * 3600
        )  # 3600  # timestep in seconds
        param["A_cell"] = 0.436  # area in m2
        param["cell_type"] = "low_power_cell"
        param["capacity"] = 100 * 1e6  # capacity in Watt
        self.electrolyser.update_parameters(param)

        param = dict()
        param["timestep"] = (
            np.diff(self.time_vector)[0] * 3600
        )  # 3600  # 1 hour in seconds, should be taken equal to delta_t
        param["maximum_capacity"] = 3000  # kg
        self.hydrogen_storage.update_parameters(param)

        x = dict()
        x["current_mass"] = 1000.0  # kg
        self.hydrogen_storage.initialize_state(x)

        ### adder
        u = dict()
        u["input_0"] = 0
        u["input_1"] = 0
        self.adder.input = u

    def connect_components(self):
        # Connect the components
        # solver.connect(predecessor,     successor,        'predecessor_output', 'successor_input')
        self.solver.connect(self.power_supply, self.splitter1, "power_supply", "input")
        self.solver.connect(
            self.splitter1, self.power_demand, "output_0", "power_input"
        )
        self.solver.connect(
            self.splitter1, self.electrolyser, "output_1", "power_input"
        )
        self.solver.connect(self.electrolyser, self.splitter2, "massflow_H2", "input")
        self.solver.connect(self.splitter2, self.adder, "output_0", "input_0")
        self.solver.connect(
            self.splitter2, self.hydrogen_storage, "output_1", "mass_flow_in"
        )
        self.solver.connect(
            self.hydrogen_storage, self.adder, "mass_flow_out", "input_1"
        )
        self.solver.connect(
            self.adder, self.hydrogen_demand, "output", "hydrogen_input"
        )

    def calculate(self):
        self.solver.run()
        print("work in progress")

    def get_output(self):
        output_dict = dict()
        output_dict["power_supply_outputs"] = power_supply_outputs = (
            self.solver.outputs[self.power_supply]
        )
        output_dict["splitter1_outputs"] = splitter1_outputs = self.solver.outputs[
            self.splitter1
        ]
        output_dict["power_demand_outputs"] = power_demand_outputs = (
            self.solver.outputs[self.power_demand]
        )
        output_dict["hydrogen_demand_outputs"] = hydrogen_demand_outputs = (
            self.solver.outputs[self.hydrogen_demand]
        )
        output_dict["electrolyser_outputs"] = electrolyser_outputs = (
            self.solver.outputs[self.electrolyser]
        )
        output_dict["splitter2_outputs"] = splitter2_outputs = self.solver.outputs[
            self.splitter2
        ]
        output_dict["hydrogen_storage_outputs"] = hydrogen_storage_outputs = (
            self.solver.outputs[self.hydrogen_storage]
        )
        output_dict["adder_outputs"] = adder_outputs = self.solver.outputs[self.adder]

        return output_dict

    def plot(self):
        # Retrieve output
        output_dict = self.get_output()

        # Control
        fig, ax1 = plt.subplots(figsize=(10, 6))
        # ax1.plot(time_vector, splitter1_control_profile(time_vector), color='r', label='Splitter1 control')
        ax1.step(
            self.time_vector_control,
            self.splitter1_control(self.time_vector_control),
            color="r",
            where="post",
            label="Splitter1 control",
        )
        # ax1.plot(time_vector, 1-splitter1_control_profile(time_vector), color='r', label='1-Splitter1 control', linestyle='-.')
        # ax1.plot(time_vector, splitter2_control_profile(time_vector), color='r', label='Splitter2 control', linestyle='--')
        ax1.step(
            self.time_vector_control,
            self.splitter2_control(self.time_vector_control),
            color="r",
            where="post",
            label="Splitter2 control",
            linestyle="--",
        )
        ax1.set_xlabel("Time (hr)")
        ax1.set_ylabel("Splitter Control [-]", color="r")
        ax1.legend(loc="upper left")
        ax1.set_xticks(self.time_vector_control)
        plt.grid(True)
        ax2 = ax1.twinx()
        # ax2.plot(time_vector, 3600*mass_flow_out_profile(time_vector), color='b', label='Storage production rate')
        ax2.step(
            self.time_vector_control,
            3600 * self.hydrogen_storage_control(self.time_vector_control),
            color="b",
            label="Storage production rate",
        )
        ax2.legend(loc="upper right")
        ax2.set_ylabel("Storage production rate [kg/hr]", color="b")
        plt.title("Control Profiles")
        plt.grid(True)

        ### Power profiles
        output_0 = [row[0] for row in self.splitter1_outputs]
        output_1 = [row[1] for row in self.splitter1_outputs]
        power_demand = [row[0] for row in self.power_demand_outputs]
        power_difference = [row[1] for row in self.power_demand_outputs]
        fig = plt.figure(figsize=(10, 6))
        plt.step(self.time_vector, self.power_supply_outputs, label="Power Supply")
        plt.step(self.time_vector, output_0, label="Power delivered")

        # plt.plot(time_vector, output_1, label='Electrolyser input')
        plt.step(self.time_vector, output_1, label="Electrolyser input")
        sum = [x + y for x, y in zip(output_0, output_1)]
        plt.step(self.time_vector, sum, label="sum", linestyle="--")  # just for checking
        plt.step(self.time_vector, power_demand, label="Power Demand")
        plt.step(self.time_vector, power_difference, label="Demand - Delivered")
        plt.xlabel("Time (hr)")
        plt.ylabel("Power [Watt]")
        plt.xticks(self.time_vector_control)
        plt.title("Power Profiles")
        plt.legend()
        plt.grid(True)

        # Hydrogen profiles
        massflow_H2 = [row[3] for row in output_dict["electrolyser_outputs"]]
        output_0 = [row[0] for row in output_dict["splitter2_outputs"]]
        output_1 = [row[1] for row in output_dict["splitter2_outputs"]]
        mass_flow_out = [row[2] for row in output_dict["hydrogen_storage_outputs"]]
        hydrogen_demand = [row[0] for row in output_dict["hydrogen_demand_outputs"]]
        hydrogen_difference = [row[1] for row in output_dict["hydrogen_demand_outputs"]]

        fig = plt.figure(figsize=(10, 6))
        plt.plot(self.time_vector, massflow_H2, label="Electrolyser hydrogen output")
        plt.plot(self.time_vector, output_0, label="Hydrogen from Electrolyser to Demand")
        plt.plot(self.time_vector, output_1, label="Hydrogen from Electrolyser to storage")
        plt.plot(self.time_vector, mass_flow_out, label="Hydrogen from Storage to Demand")
        plt.plot(self.time_vector, hydrogen_demand, label="Hydrogen Demand")
        plt.plot(self.time_vector, output_dict["adder_outputs"], label="Hydrogen Delivered")
        plt.plot(self.time_vector, hydrogen_difference, label="Demand - Delivered")
        plt.xlabel("Time (hr)")
        plt.ylabel("Hydrogen flow [kg/s]")
        plt.title("Hydrogen Profiles")
        plt.legend()
        plt.grid(True)

        ### Storage
        current_mass = [row[0] for row in output_dict["hydrogen_storage_outputs"]]
        fill_level = [row[1] * 100 for row in output_dict["hydrogen_storage_outputs"]]
        mass_flow_out = [row[2] * 3600 for row in output_dict["hydrogen_storage_outputs"]]
        output_1 = [row[1] * 3600 for row in output_dict["splitter2_outputs"]]

        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax1.plot(self.time_vector, current_mass, color="r", label="Current Mass")
        ax1.set_xlabel("Time (hr)")
        ax1.set_ylabel("Current mass [kg]", color="r")
        ax1.legend(loc="center left")
        ax2 = ax1.twinx()
        ax2.plot(self.time_vector, fill_level, color="b", label="Fill Level %")
        ax2.plot(self.time_vector, output_1, color="b", label="Mass flow in", linestyle="-.")
        ax2.plot(
            self.time_vector, mass_flow_out, color="b", label="Mass flow out", linestyle="--"
        )
        ax2.set_ylabel("Fill Level [%] / Mass flow [kg/hr]", color="b")
        plt.title("Hydrogen Storage profiles")
        ax2.legend(loc="center right")
        plt.grid(True)

        plt.show()
