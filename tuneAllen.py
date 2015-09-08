'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation
from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict


parameters = ['cell:RS/channelDensity:Na_all/mS_per_cm2',
              'cell:RS/channelDensity:Kd_all/mS_per_cm2',
              'cell:RS/channelDensity:IM_all/mS_per_cm2',
              'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2',
              'cell:RS/erev_id:LeakConductance_all/mV',
              'cell:RS/erev_id:Na_all/mV',
              'cell:RS/erev_id:Kd_all/mV',
              'cell:RS/erev_id:IM_all/mV']

#above parameters will not be modified outside these bounds:
min_constraints = [20,   1,    1e-6,  0.001, -100, 50, -100, -100]
max_constraints = [100,  25,   4,     0.1,     -70,  60, -70,  -70]


ref = 'Pop0/0/RS/v:'
average_maximum = ref+'average_maximum'
average_minimum = ref+'average_minimum'
mean_spike_frequency = ref+'mean_spike_frequency'
#first_spike_time = ref+'first_spike_time'
average_last_1percent = ref+'average_last_1percent'

weights = {average_maximum: 1,
           average_minimum: 1,
           mean_spike_frequency: 5,
           average_last_1percent: 1}

target_data = {average_maximum: 33.320915,
               average_minimum: -44.285,
               mean_spike_frequency: 26.6826,
               average_last_1percent: -80}

simulator  = 'jNeuroML_NEURON'
#simulator  = 'jNeuroML'

parameters_iz = ['izhikevich2007Cell:RS/a/per_ms',
                 'izhikevich2007Cell:RS/b/nS',
                 'izhikevich2007Cell:RS/c/mV',
                 'izhikevich2007Cell:RS/d/pA',
                 'izhikevich2007Cell:RS/vr/mV',
                 'izhikevich2007Cell:RS/vt/mV',
                 'izhikevich2007Cell:RS/vpeak/mV',]
                 
min_constraints_iz = [0.01, -5, -65, 10,  -100, -70, 0]
max_constraints_iz = [0.2,  20, -50, 400, -40,  0,   60]
        
def run_one_optimisation(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites,
                     simulator,
                     nogui,
                     neuroml_file =     'models/RS/AllenTest.net.nml',
                     target =           'network_RS',
                     parameters =       parameters,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     dt =               0.025,):
                         
    ref = '%s__s%s_p%s_m%s_s%s_o%s_m%s_e%s'%(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites)           

    run_optimisation(prefix =           ref, 
                     neuroml_file =     neuroml_file,
                     target =           target,
                     parameters =       parameters,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     sim_time =         1500,
                     dt =               dt,
                     seed =             seed,
                     population_size =  population_size,
                     max_evaluations =  max_evaluations,
                     num_selected =     num_selected,
                     num_offspring =    num_offspring,
                     mutation_rate =    mutation_rate,
                     num_elites =       num_elites,
                     simulator =        simulator,
                     nogui =            nogui)

if __name__ == '__main__':
    
    nogui = '-nogui' in sys.argv
    
    if '-one' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        
        cont = NeuroMLController('AllenTest', 
                                 'models/RS/AllenTest.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.01, 
                                 simulator)
                                 
        example_vars = {'cell:RS/channelDensity:IM_all/mS_per_cm2': 0.7724432400416816,
                            'cell:RS/channelDensity:Kd_all/mS_per_cm2': 4.643108211145454,
                            'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2': 0.007883588106567089,
                            'cell:RS/channelDensity:Na_all/mS_per_cm2': 44.05565568387002,
                            'cell:RS/erev_id:LeakConductance_all/mV': -95.25485559729064}

        sim_vars = OrderedDict(example_vars)
                                
                                 
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
    elif '-izhone' in sys.argv:
        
        simulator  = 'jNeuroML'
        
        cont = NeuroMLController('AllenIzhTest', 
                                 'models/RS/AllenIzh.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.01, 
                                 simulator)
                                 
        example_vars = {'izhikevich2007Cell:RS/a/per_ms': 0.01}

        sim_vars = OrderedDict(example_vars)
                                
                                 
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
        
    elif '-izhquick' in sys.argv:
        
        simulator  = 'jNeuroML'
        
        run_one_optimisation('AllenIzh',
                            1234,
                            population_size =  40,
                            max_evaluations =  300,
                            num_selected =     20,
                            num_offspring =    15,
                            mutation_rate =    0.2,
                            num_elites =       3,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'models/RS/AllenIzh.net.nml',
                            target =           'network_RS',
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz)
        
        
        
    elif '-quick' in sys.argv:

        run_one_optimisation('AllenTestQ',
                            1234,
                            population_size =  10,
                            max_evaluations =  20,
                            num_selected =     5,
                            num_offspring =    8,
                            mutation_rate =    0.9,
                            num_elites =       1,
                            simulator =        simulator,
                            nogui =            nogui)

    else:
        
        run_one_optimisation('AllenTest',
                            1234,
                            population_size =  20,
                            max_evaluations =  100,
                            num_selected =     15,
                            num_offspring =    15,
                            mutation_rate =    0.1,
                            num_elites =       1,
                            simulator =        simulator,
                            nogui =            nogui)
        


