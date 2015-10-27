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


    sim_time =         700
    dt =               0.01

    prefix =           'TestGran'
    neuroml_file =     'models/GranuleCell.net.nml'
    target =           'network_GranuleCell'

    simulator  = 'jNeuroML_NEURON'
    #simulator  = 'jNeuroML'

    quick = True
    #quick = False
    
    if quick:
        population_size =  5
        max_evaluations =  20
        num_selected =     10
        num_offspring =    8
    else:
        population_size =  50
        max_evaluations =  300
        num_selected =     50
        num_offspring =    30
    
    mutation_rate =    0.5
    num_elites =       1

    seed = 1234
    verbose = False
    

    parameters = ['cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2',
                  'cell:Granule_98/specificCapacitance:all/uF_per_cm2']

    #above parameters will not be modified outside these bounds:
    min_constraints = [50,   6,   0,    0,   0.5]
    max_constraints = [60,  15,   0.05, 0.1, 1.5]


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
    
    nogui = '-nogui' in sys.argv
    
    vars = {'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2': 0.03337471902862413,
        'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2': 0.03559929171361169,
        'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2': 7.016013314649269,
        'cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2': 55.74495636439219,
        'cell:Granule_98/specificCapacitance:all/uF_per_cm2': 1.0808061342038033}
    
    sim_vars = OrderedDict(vars)
    sim_vars = OrderedDict([])
    
    if '-one' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        
        cont = NeuroMLController('TestGran', 
                                 'models/GranuleCell.net.nml',
                                 'network_GranuleCell',
                                 sim_time, 
                                 dt, 
                                 simulator)
        
        t, v = cont.run_individual(sim_vars, show=False)
        
        analysis = utils.simple_iclamp_analysis(v['Gran/0/Granule_98/v'], t, plot=True)
        
    elif '-mone' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        
        cont = NeuroMLController('TestGranNet', 
                                 'models/GranuleCellMulti.net.nml',
                                 'network_GranuleCell_multi',
                                 sim_time, 
                                 dt, 
                                 simulator)
        
        t, v = cont.run_individual(sim_vars, show=False)
        
        analysis = utils.simple_network_analysis(v, t, plot=True)
        
    elif '-mtune' in sys.argv:
        
        prefix =           'TestGranNet'
        neuroml_file =     'models/GranuleCellMulti.net.nml'
        target =           'network_GranuleCell_multi'
        
        run_optimisation(prefix =           prefix, 
                         neuroml_file =     neuroml_file,
                         target =           target,
                         parameters =       parameters,
                         max_constraints =  max_constraints,
                         min_constraints =  min_constraints,
                         weights =          weights,
                         target_data =      target_data,
                         sim_time =         sim_time,
                         dt =               dt,
                         population_size =  population_size,
                         max_evaluations =  max_evaluations,
                         num_selected =     num_selected,
                         num_offspring =    num_offspring,
                         mutation_rate =    mutation_rate,
                         num_elites =       num_elites,
                         simulator =        simulator,
                         nogui =            nogui,
                         seed =             seed)
        
    else:
        
        
        if not '-remote' in sys.argv:

            run_optimisation(prefix =           prefix, 
                             neuroml_file =     neuroml_file,
                             target =           target,
                             parameters =       parameters,
                             max_constraints =  max_constraints,
                             min_constraints =  min_constraints,
                             weights =          weights,
                             target_data =      target_data,
                             sim_time =         sim_time,
                             dt =               dt,
                             population_size =  population_size,
                             max_evaluations =  max_evaluations,
                             num_selected =     num_selected,
                             num_offspring =    num_offspring,
                             mutation_rate =    mutation_rate,
                             num_elites =       num_elites,
                             simulator =        simulator,
                             nogui =            nogui,
                             seed =             seed)
        else:
            
            from RemoteRun import run_remotely, to_command_line_arg

            prefix_ = 'Grc_%s_e%s_m%s_s%s_%s'%(population_size,max_evaluations,mutation_rate,seed,prefix)
                
            command = 'pynml-tune  %s  %s  %s  %s  %s  %s  %s  %s -simTime %s -dt %s -populationSize %s -maxEvaluations %s -numSelected %s -numOffspring %s -mutationRate %s -numElites %s -seed %s -simulator %s %s %s'%(prefix_,
                                                 neuroml_file,
                                                 target,
                                                 to_command_line_arg(parameters),
                                                 to_command_line_arg(max_constraints),
                                                 to_command_line_arg(min_constraints),
                                                 to_command_line_arg(target_data),
                                                 to_command_line_arg(weights),
                                                 sim_time,
                                                 dt,
                                                 population_size,
                                                 max_evaluations,
                                                 num_selected,
                                                 num_offspring,
                                                 mutation_rate,
                                                 num_elites,
                                                 seed,
                                                 simulator,
                                                 '-verbose' if verbose else '',
                                                 '-nogui')

            print('-----------------------------------------')
            print(command)
            run_remotely(command, prefix_, '/home/ucgbpgl/git/testtune', runtime='03:00:00')



