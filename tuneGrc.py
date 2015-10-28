'''

    Still under development!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation
from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict

from pyelectro import utils

def plot_baseline_data(targets = None):
    
    baseline = {}
    file_name = 'TestGranNet.v.basedat'

    cols = ['t', 'Gran/0/Granule_98/v', 'Gran/1/Granule_98/v', 'Gran/2/Granule_98/v']

    for c in cols:
        baseline[c] = []

    for line in open(file_name):
        values = line.split()

        for vi in range(len(values)):
           baseline[cols[vi]].append(float(values[vi])*1000)

    volts = {}
    for k in baseline.keys():
        if k!='t': 
            volts[k]=baseline[k]

    utils.simple_network_analysis(volts, 
                                  baseline['t'], 
                                  targets = targets,
                                  plot=True, 
                                  show_plot_already=False)

if __name__ == '__main__':


    sim_time =         600
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


    ref0 = 'Gran/0/Granule_98/v:'
    ref1 = 'Gran/1/Granule_98/v:'
    ref2 = 'Gran/2/Granule_98/v:'
    
    average_maximum0 = ref0+'average_maximum'
    average_minimum0 = ref0+'average_minimum'
    mean_spike_frequency0 = ref0+'mean_spike_frequency'
    first_spike_time0 = ref0+'first_spike_time'
    
    weights = {average_maximum0: 1,
               average_minimum0: 1,
               mean_spike_frequency0: 1,
               first_spike_time0: 1}

    target_data = {average_maximum0: 15.3011,
                   average_minimum0: -70.066,
                   mean_spike_frequency0: 38.339,
                   first_spike_time0: 108.34}
                   
                   
    minimum_pas1 = ref1+'minimum'
    value_110_pas1 = ref1+'value_110'
    
    minimum_pas2 = ref2+'minimum'
    value_110_pas2 = ref2+'value_110'
    value_400_pas2 = ref2+'value_400'

    target_data_pas = {minimum_pas1: -71.39,
                       value_110_pas1: -67.22,
                       minimum_pas2: -84.97147,
                       value_110_pas2: -74.36766,
                       value_400_pas2: -80.15374}


                       
    weights_pas = {minimum_pas1: 1,
                   value_110_pas1: 1,
                   minimum_pas2: 1,
                   value_110_pas2: 1,
                   value_400_pas2: 1}
    
    nogui = '-nogui' in sys.argv
    
    vars = {'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2': 0.03337471902862413,
        'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2': 0.03559929171361169,
        'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2': 7.016013314649269,
        'cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2': 55.74495636439219,
        'cell:Granule_98/specificCapacitance:all/uF_per_cm2': 1.0808061342038033}
    
    sim_vars = OrderedDict(vars)
    #sim_vars = OrderedDict([])
    
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
        sim_time =         700
        
        cont = NeuroMLController('TestGranNet', 
                                 'models/GranuleCellMulti.net.nml',
                                 'network_GranuleCell_multi',
                                 sim_time, 
                                 dt, 
                                 simulator)
        
        t, v = cont.run_individual(sim_vars, show=False)
        
        plot_baseline_data(targets = target_data_pas.keys())
        
        analysis = utils.simple_network_analysis(v, 
                                                 t, 
                                                 plot=True,
                                                 targets = target_data_pas.keys())
        
        
        
    elif '-mtune' in sys.argv:
        
        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'
        
        prefix =           'TestGranNet'
        neuroml_file =     'models/GranuleCellMulti.net.nml'
        target =           'network_GranuleCell_multi'
        sim_time =         700
        
        population_size =  5
        max_evaluations =  10
        num_selected =     3
        num_offspring =    4

        parameters = ['cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2',
                      'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2',
                      'cell:Granule_98/specificCapacitance:all/uF_per_cm2']

        #above parameters will not be modified outside these bounds:
        min_constraints_pas = [0,   0,   0,    0,   0.5]
        max_constraints_pas = [0,   0,   0.05, 0.1, 1.5]
        
        known_target_values = {'cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2':55.7227,
                               'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2':8.89691,
                               'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2': 0.03090506,
                               'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2': 0.0330033,
                               'cell:Granule_98/specificCapacitance:all/uF_per_cm2': 1}
        
        report = run_optimisation(prefix = 'Pas_'+prefix, 
                         neuroml_file =     neuroml_file,
                         target =           target,
                         parameters =       parameters,
                         max_constraints =  max_constraints_pas,
                         min_constraints =  min_constraints_pas,
                         weights =          weights_pas,
                         target_data =      target_data_pas,
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
                         show_plot_already = False,
                         seed =             seed,
                         known_target_values = known_target_values)
                         
        print report
                         
        plot_baseline_data()
        
        eps = 0.01
        
        gh = report['fittest vars']['cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2']
        gpas = report['fittest vars']['cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2']
        sc = report['fittest vars']['cell:Granule_98/specificCapacitance:all/uF_per_cm2']
        
        min_constraints = [50,   6, gh*(1-eps), gpas*(1-eps), sc*(1-eps)]
        max_constraints = [60,  15, gh*(1+eps), gpas*(1+eps), sc*(1+eps)]
        
        
        report = run_optimisation(prefix = prefix, 
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
                         show_plot_already = True,
                         seed =             seed,
                         known_target_values = known_target_values)
        
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



