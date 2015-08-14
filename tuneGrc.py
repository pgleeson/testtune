'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation
from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict

from pyelectro import utils


if __name__ == '__main__':
    
    nogui = '-nogui' in sys.argv
    
    if '-one' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        
        cont = NeuroMLController('TestGran', 
                                 'models/GranuleCell.net.nml',
                                 'network_GranuleCell',
                                 700, 
                                 0.01, 
                                 simulator)
                                 
        sim_vars = OrderedDict([('cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2', 55.7227),
                                ('cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2', 8.89691)])
                                
        
        t, v = cont.run_individual(sim_vars, show=False)
        
        analysis = utils.simple_iclamp_analysis(v['Gran/0/Granule_98/v'], t, plot=True)
        
    else:
        

        parameters = ['cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2']

        #above parameters will not be modified outside these bounds:
        min_constraints = [40,   1,   0, 0]
        max_constraints = [60,  20,   1, 0.3]


        ref = 'Gran/0/Granule_98/v:'
        average_maximum = ref+'average_maximum'
        average_minimum = ref+'average_minimum'
        mean_spike_frequency = ref+'mean_spike_frequency'
        first_spike_time = ref+'first_spike_time'

        weights = {average_maximum: 1,
                   average_minimum: 1,
                   mean_spike_frequency: 1,
                   first_spike_time: 1}

        target_data = {average_maximum: 15.3011,
                       average_minimum: -70.066,
                       mean_spike_frequency: 38.339,
                       first_spike_time: 108.34}

        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'

        run_optimisation('TestGran', 
                         'models/GranuleCell.net.nml',
                         'network_GranuleCell',
                         parameters,
                         max_constraints,
                         min_constraints,
                         weights,
                         target_data,
                         sim_time = 700,
                         dt = 0.01,
                         population_size =  20,
                         max_evaluations =  100,
                         num_selected =     10,
                         num_offspring =    8,
                         mutation_rate =    0.5,
                         num_elites =       1,
                         simulator =        simulator,
                         nogui =            nogui)



