'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from RemoteRun import run_remotely

def to_command_line_arg(arg):
    
    if isinstance(arg, list):
        ret = '['
        for a in arg:
            ret+='%s,'%a
        return ret[:-1]+']'
    elif isinstance(arg, dict):
        ret = '['
        for k in arg.keys():
            ret+='%s:%s,'%(k,arg[k])
        return ret[:-1]+']'
    else:
        return '???'

if __name__ == '__main__':
    
    prefix =           'TestGran'
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
    population_size =  20
    max_evaluations =  40
    num_selected =     10
    num_offspring =    8
    mutation_rate =    0.5
    num_elites =       1
    seed =             1234
    
    nogui =            False
    verbose =          True

    simulator  = 'jNeuroML_NEURON'
    #simulator  = 'jNeuroML'
    
    command = 'pynml-tune  %s  %s  %s  %s  %s  %s  %s  %s -simTime %s -dt %s -populationSize %s -maxEvaluations %s -numSelected %s -numOffspring %s -mutationRate %s -numElites %s -seed %s -simulator %s %s %s'%(prefix,
                                     neuroml_file,
                                     target,
                                     to_command_line_arg(parameters),
                                     to_command_line_arg(max_constraints),
                                     to_command_line_arg(min_constraints),
                                     to_command_line_arg(weights),
                                     to_command_line_arg(target_data),
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
                                     '-nogui' if nogui else '')
    
    print(command)
    
    run_remotely(command, 'testGrc', '/home/ucgbpgl/git/testtune')
                     



