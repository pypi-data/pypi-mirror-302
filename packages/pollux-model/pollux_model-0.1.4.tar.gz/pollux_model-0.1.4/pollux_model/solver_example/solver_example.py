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

time_horizon = 24  # hours (integer)
step_size_control = 2 # time_horizon/step_size_control (integer)
if time_horizon % step_size_control != 0:
    raise ValueError(f"time_horizon ({time_horizon}) is not"
                     f" divisible by step_size_control ({step_size_control})")

# times of the supply and demand profiles
time_vector = np.linspace(0, time_horizon, 97)
# time_vector_control = np.linspace(0, 24, 25)  # From t=0 to t=24 with 25 steps
time_vector_control = np.linspace(0, time_horizon, time_horizon//step_size_control + 1)

# ## power supply
power_supply_profile = lambda t: 10E6 * (2 + np.sin(t))     # Watt
power_supply = PowerSupply(power_supply_profile)

# ## power demand
power_demand_profile = lambda t: 10E6   # Watt
power_demand = PowerDemand(power_demand_profile)

# ## hydrogen demand
hydrogen_demand_profile = lambda t: 200/3600    # kg/s
hydrogen_demand = HydrogenDemand(hydrogen_demand_profile)

# ## splitter1
# a * (0.5 + 0.5*np.sin(t)) + b  varies between b and b+a
splitter1_control_profile = lambda t: 0.5 * (0.5 + 0.5*np.sin(t)) + 0.4 
# splitter1_control_profile = lambda t: 0.8/(2 + np.sin(t)) 
splitter1_control = lambda t: step_function(t, step_size_control, splitter1_control_profile(time_vector_control))
splitter1 = Splitter(splitter1_control)

# ## electrolyser
electrolyser = ElectrolyserDeGroot()

u = dict()
u['T_cell'] = 273.15 + 40   # cell temperature in K
u['p_cathode'] = 10e5   # cathode pressure in Pa
u['p_anode'] = 10e5     # anode pressure in Pa
u['p_0_H2O'] = 10e5     # Pa
# u['power_input'] = 2118181.8181  # input power in Watt
electrolyser.input = u

param = dict()
param['eta_Faraday_array'] = 1  # just a constant, in reality is a variable
param['Faraday_const'] = 96485.3329  # Faraday constant [(s A)/mol]
param['delta_t'] = np.diff(time_vector)[0]*3600     # 3600  # timestep in seconds
param['A_cell'] = 0.436  # area in m2
param['cell_type'] = 'low_power_cell'
param['capacity'] = 100 * 1e6  # capacity in Watt
electrolyser.update_parameters(param)

# ## splitter2
splitter2_control_profile = lambda t: 0.5 * 0.1 *(1 + np.sin(t)) + 0.5  # varies 0.5 and 0.5 + 0.1
# splitter2 = Splitter(splitter2_control_profile)
splitter2_control = lambda t: step_function(t,
                                            step_size_control,
                                            splitter2_control_profile(time_vector_control))
splitter2 = Splitter(splitter2_control)

# ## storage
# control variable kg/s: the hydrogen mass flow produced from the storage
hydrogen_storage_profile = lambda t: 100/3600 * (t+1)/(t+1)

# hydrogen_storage = HydrogenTankModel(mass_flow_out_profile)
hydrogen_storage_control = lambda t: step_function(t,
                                                   step_size_control,
                                                   hydrogen_storage_profile(time_vector_control))
hydrogen_storage = HydrogenTankModel(hydrogen_storage_control)

param = dict()

# 3600  # 1 hour in seconds, should be taken equal to delta_t
param['timestep'] = np.diff(time_vector)[0]*3600
param['maximum_capacity'] = 3000    # kg
hydrogen_storage.update_parameters(param)

x = dict()
x['current_mass'] = 1000.0  # kg
hydrogen_storage.initialize_state(x)

# ## adder
adder = Adder()
u = dict()
u['input_0'] = 0
u['input_1'] = 0
adder.input = u

# ## solver object
solver = Solver(time_vector)

# ## connect the components
# solver.connect(predecessor,     successor,        'predecessor_output', 'successor_input')
solver.connect(power_supply,     splitter1,        'power_supply',  'input')
solver.connect(splitter1,        power_demand,     'output_0',      'power_input')
solver.connect(splitter1,        electrolyser,     'output_1',      'power_input')
solver.connect(electrolyser,     splitter2,        'massflow_H2',   'input')
solver.connect(splitter2,        adder,            'output_0',      'input_0')
solver.connect(splitter2,        hydrogen_storage, 'output_1',      'mass_flow_in')
solver.connect(hydrogen_storage, adder,            'mass_flow_out', 'input_1')
solver.connect(adder,            hydrogen_demand,  'output',        'hydrogen_input')

# ## run the solver, loop over time
solver.run()

# print(f"Power supply: {power_supply.input}") # boundary condition
print(f"Power supply output: {power_supply.output}")

print(f"Splitter1 input: {splitter1.input}")
print(f"Splitter1 output: {splitter1.output}")

print(f"Power demand: {power_demand.input}")    # boundary condition
# print(f"Power demand input: {power_demand.input}")
print(f"Power demand difference: {power_demand.output}")

print(f"Splitter2 input: {splitter2.input}")
print(f"Splitter2 output: {splitter2.output}")

print(f"Electrolyser input: {electrolyser.input}")
print(f"Electrolyser output: {electrolyser.output}")

print(f"Hydrogen storage input: {hydrogen_storage.input}")
print(f"Hydrogen storage output: {hydrogen_storage.output}")

print(f"Adder input: {adder.input}")
print(f"Adder output: {adder.output}")

print(f"Hydrogen demand: {hydrogen_demand.input}")  # boundary condition
# print(f"Hydrogen demand input: {hydrogen_demand.input}")
print(f"Hydrogen demand difference: {hydrogen_demand.output}")

power_supply_outputs = solver.outputs[power_supply]
splitter1_outputs = solver.outputs[splitter1]
power_demand_outputs = solver.outputs[power_demand]
hydrogen_demand_outputs = solver.outputs[hydrogen_demand]
electrolyser_outputs = solver.outputs[electrolyser]
splitter2_outputs = solver.outputs[splitter2]
hydrogen_storage_outputs = solver.outputs[hydrogen_storage]
adder_outputs = solver.outputs[adder]

# ## control
fig, ax1 = plt.subplots(figsize=(10, 6))
# ax1.plot(time_vector,
#          splitter1_control_profile(time_vector),
#          color='r',
#          label='Splitter1 control')
ax1.step(time_vector_control,
         splitter1_control(time_vector_control),
         color='r',
         where='post',
         label='Splitter1 control')
# ax1.plot(time_vector,
#          1-splitter1_control_profile(time_vector),
#          color='r',
#          label='1-Splitter1 control',
#          linestyle='-.')
# ax1.plot(time_vector,
#          splitter2_control_profile(time_vector),
#          color='r',
#          label='Splitter2 control',
#          linestyle='--')
ax1.step(time_vector_control, splitter2_control(time_vector_control),
         color='r',
         where='post',
         label='Splitter2 control',
         linestyle='--')
ax1.set_xlabel('Time (hr)')
ax1.set_ylabel('Splitter Control [-]', color='r')
ax1.legend(loc='upper left')
ax1.set_xticks(time_vector_control)
plt.grid(True)
ax2 = ax1.twinx()

# ax2.plot(time_vector, 3600*mass_flow_out_profile(time_vector), color='b', label='Storage production rate')
ax2.step(time_vector_control,
         3600*hydrogen_storage_control(time_vector_control),
         color='b',
         label='Storage production rate')
ax2.legend(loc='upper right')
ax2.set_ylabel('Storage production rate [kg/hr]', color='b')
plt.title('Control Profiles')
plt.grid(True)

# ## Power profiles
output_0 = [row[0] for row in splitter1_outputs]
output_1 = [row[1] for row in splitter1_outputs]
power_demand = [row[0] for row in power_demand_outputs]
power_difference = [row[1] for row in power_demand_outputs]
fig = plt.figure(figsize=(10, 6))
plt.step(time_vector, power_supply_outputs, label='Power Supply')
plt.step(time_vector, output_0, label='Power delivered')

# plt.plot(time_vector, output_1, label='Electrolyser input')
plt.step(time_vector, output_1, label='Electrolyser input')
sum = [x + y for x, y in zip(output_0, output_1)]
plt.step(time_vector, sum, label='sum', linestyle='--')     # just for checking
plt.step(time_vector, power_demand, label='Power Demand')
plt.step(time_vector, power_difference, label='Demand - Delivered')
plt.xlabel('Time (hr)')
plt.ylabel('Power [Watt]')
plt.xticks(time_vector_control)
plt.title('Power Profiles')
plt.legend()
plt.grid(True)


# ## Hydrogen profiles
massflow_H2 = [row[3] for row in electrolyser_outputs]
output_0 = [row[0] for row in splitter2_outputs]
output_1 = [row[1] for row in splitter2_outputs]
mass_flow_out = [row[2] for row in hydrogen_storage_outputs]
hydrogen_demand = [row[0] for row in hydrogen_demand_outputs]
hydrogen_difference = [row[1] for row in hydrogen_demand_outputs]

fig = plt.figure(figsize=(10, 6))
plt.plot(time_vector, massflow_H2, label='Electrolyser hydrogen output')
plt.plot(time_vector, output_0, label='Hydrogen from Electrolyser to Demand')
plt.plot(time_vector, output_1, label='Hydrogen from Electrolyser to storage')
plt.plot(time_vector, mass_flow_out, label='Hydrogen from Storage to Demand')
plt.plot(time_vector, hydrogen_demand, label='Hydrogen Demand')
plt.plot(time_vector, adder_outputs, label='Hydrogen Delivered')
plt.plot(time_vector, hydrogen_difference, label='Demand - Delivered')
plt.xlabel('Time (hr)')
plt.ylabel('Hydrogen flow [kg/s]')
plt.title('Hydrogen Profiles')
plt.legend()
plt.grid(True)

# ## Storage
current_mass = [row[0] for row in hydrogen_storage_outputs]
fill_level = [row[1]*100 for row in hydrogen_storage_outputs]
mass_flow_out = [row[2]*3600 for row in hydrogen_storage_outputs]
output_1 = [row[1]*3600 for row in splitter2_outputs]

fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(time_vector, current_mass, color='r', label='Current Mass')
ax1.set_xlabel('Time (hr)')
ax1.set_ylabel('Current mass [kg]', color='r')
ax1.legend(loc='center left')
ax2 = ax1.twinx()
ax2.plot(time_vector, fill_level, color='b', label='Fill Level %')
ax2.plot(time_vector, output_1, color='b', label='Mass flow in', linestyle='-.')
ax2.plot(time_vector, mass_flow_out, color='b', label='Mass flow out', linestyle='--')
ax2.set_ylabel('Fill Level [%] / Mass flow [kg/hr]', color='b')
plt.title('Hydrogen Storage profiles')
ax2.legend(loc='center right')
plt.grid(True)

plt.show()
