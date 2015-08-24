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
              'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2']

#above parameters will not be modified outside these bounds:
min_constraints = [30,   1,    1e-6,  1e-6]
max_constraints = [200,  30,   4,  0.01]


ref = 'Pop0/0/RS/v:'
average_maximum = ref+'average_maximum'
average_minimum = ref+'average_minimum'
mean_spike_frequency = ref+'mean_spike_frequency'
first_spike_time = ref+'first_spike_time'

weights = {average_maximum: 1,
           average_minimum: 1,
           mean_spike_frequency: 1,
           first_spike_time: 1}
           
target_data = {average_maximum: 44.02934,
               average_minimum: -34.528,
               mean_spike_frequency: 73.688,
               first_spike_time: 25.68}

simulator  = 'jNeuroML_NEURON'
#simulator  = 'jNeuroML'

sim_time =         300
prefix = 'SSTest'

        
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

    run_optimisation(prefix =           ref, 
                     neuroml_file =     'models/RS/SSTest.net.nml',
                     target =           'network_RS',
                     parameters =       parameters,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     sim_time =         sim_time,
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
        
        cont = NeuroMLController(prefix, 
                                 'models/RS/SSTest.net.nml',
                                 'network_RS',
                                 sim_time, 
                                 0.01, 
                                 simulator)
                                 
        sim_vars = OrderedDict([('cell:RS/channelDensity:Na_all/mS_per_cm2', 100),
                                ('cell:RS/channelDensity:Kd_all/mS_per_cm2', 20),
                                ('cell:RS/channelDensity:LeakConductance_all/mS_per_cm2', 1e-5)])
                                
                                 
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
    else:
        
        run_one_optimisation(prefix,
                            123456,
                            population_size =  30,
                            max_evaluations =  200,
                            num_selected =     16,
                            num_offspring =    12,
                            mutation_rate =    0.9,
                            num_elites =       3,
                            simulator =        simulator,
                            nogui =            nogui)
        


