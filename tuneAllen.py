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
              'cell:RS/erev_id:LeakConductance_all/mV']

#above parameters will not be modified outside these bounds:
min_constraints = [20,   1,    0,  1e-5, -100]
max_constraints = [80,  30,   1,  0.5, -80]


ref = 'Pop0/0/RS/v:'
average_maximum = ref+'average_maximum'
average_minimum = ref+'average_minimum'
mean_spike_frequency = ref+'mean_spike_frequency'
first_spike_time = ref+'first_spike_time'
average_last_1percent = ref+'average_last_1percent'

weights = {average_maximum: 1,
           average_minimum: 1,
           mean_spike_frequency: 1,
           first_spike_time: 1,
           average_last_1percent: 1}

target_data = {average_maximum: 33.320915,
               average_minimum: -44.285,
               mean_spike_frequency: 26.6826,
               first_spike_time: 226,
               average_last_1percent: -80}

simulator  = 'jNeuroML_NEURON'
#simulator  = 'jNeuroML'
        
def run_one_optimisation(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites,
                     simulator,
                     nogui):
                         
    ref = '%s__s%s_p%s_m%s_s%s_o%s_m%s_e%s'%(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites)           

    run_optimisation(prefix =           ref, 
                     neuroml_file =     'models/RS/AllenTest.net.nml',
                     target =           'network_RS',
                     parameters =       parameters,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     sim_time =         1500,
                     dt =               0.025,
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
                            population_size =  40,
                            max_evaluations =  200,
                            num_selected =     15,
                            num_offspring =    10,
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui)
        


