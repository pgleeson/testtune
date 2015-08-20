'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation
from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict


if __name__ == '__main__':
    
    nogui = '-nogui' in sys.argv
    
    if '-one' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        simulator  = 'jNeuroML'
        
        cont = NeuroMLController('AllenTest', 
                                 'models/RS/AllenTest.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.01, 
                                 simulator)
                                 
        sim_vars = OrderedDict([('cell:RS/channelDensity:Na_all/mS_per_cm2', 50),
                                ('cell:RS/channelDensity:Kd_all/mS_per_cm2', 5)])
                                
                                 
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
    else:
        

        parameters = ['cell:RS/channelDensity:Na_all/mS_per_cm2',
                      'cell:RS/channelDensity:Kd_all/mS_per_cm2',
                      'cell:RS/channelDensity:IM_all/mS_per_cm2',
                      'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2']

        #above parameters will not be modified outside these bounds:
        min_constraints = [20,   1,    0,  0]
        max_constraints = [80,  30,   1,  0.5]


        ref = 'Pop0/0/RS/v:'
        average_maximum = ref+'average_maximum'
        average_minimum = ref+'average_minimum'
        mean_spike_frequency = ref+'mean_spike_frequency'
        first_spike_time = ref+'first_spike_time'

        weights = {average_maximum: 1,
                   average_minimum: 1,
                   mean_spike_frequency: 1,
                   first_spike_time: 1}

        target_data = {average_maximum: 33.320915,
                       average_minimum: -44.285,
                       mean_spike_frequency: 26.6826,
                       first_spike_time: 226}

        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'

        run_optimisation('AllenTest', 
                         'models/RS/AllenTest.net.nml',
                         'network_RS',
                         parameters,
                         max_constraints,
                         min_constraints,
                         weights,
                         target_data,
                         sim_time = 1500,
                         dt = 0.01,
                         seed = 1234,
                         population_size =  40,
                         max_evaluations =  400,
                         num_selected =     10,
                         num_offspring =    8,
                         mutation_rate =    0.9,
                         num_elites =       1,
                         simulator =        simulator,
                         nogui =            nogui)



