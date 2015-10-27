'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from RemoteRun import run_remotely, to_command_line_arg


if __name__ == '__main__':
    
    neuroml_file =     'models/GranuleCell.net.nml'
    target =           'network_GranuleCell'

    parameters = ['cell:Granule_98/channelDensity:Gran_NaF_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:Gran_KDr_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:Gran_H_98_all/mS_per_cm2',
                  'cell:Granule_98/channelDensity:GranPassiveCond_all/mS_per_cm2']

    #above parameters will not be modified outside these bounds:
    min_constraints = [40,1,0,0]
    max_constraints = [60,20,1,0.3]


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
                   
    sim_time =         700
    dt =               0.01
    #population_size =  40
    max_evaluations =  400
    num_selected =     20
    num_offspring =    15
    
    num_elites =       1
    
    nogui =            True
    verbose =          True

    simulator  = 'jNeuroML_NEURON'
    #simulator  = 'jNeuroML'
    
    muts = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    muts = [0.1,0.9]
    
    population_sizes = [30,50,70,100]
    
    seeds = [123,345,456,678,890]
    
    prefix =           'TestPopSize'
    
    count = 0
    for seed in seeds:
        for mut in muts:
            for population_size in population_sizes:

                prefix_ = 'p%s_m%s_s%s_%s'%(population_size,mut,seed,prefix)
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
                                                 mut,
                                                 num_elites,
                                                 seed,
                                                 simulator,
                                                 '-verbose' if verbose else '',
                                                 '-nogui' if nogui else '')

                print('-----------------------------------------')
                print(command)
                run_remotely(command, prefix_, '/home/ucgbpgl/git/testtune', runtime='03:00:00')

                count+=1
            
    print("\nSet running %i simulations\n"%count)
                     



