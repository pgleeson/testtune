'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation, run_2stage_optimization

from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict

import json

import matplotlib.pyplot as plt


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
                 'izhikevich2007Cell:RS/C/pF',
                 'izhikevich2007Cell:RS/vr/mV',
                 'izhikevich2007Cell:RS/vt/mV',
                 'izhikevich2007Cell:RS/vpeak/mV',
                 'izhikevich2007Cell:RS/k/nS_per_mV']

#                     a,     b,  c,  d,   C,    vr,  vt, vpeak, k
min_constraints_iz = [0.01, -5, -65, 10,  30,  -90, -60, 0,    0.1]
max_constraints_iz = [0.2,  20, -10, 400, 300, -70,  50, 70,   1]

example_vars_iz = {'izhikevich2007Cell:RS/C/pF': 157.3674812918236,
                'izhikevich2007Cell:RS/a/per_ms': 0.09303530809766278,
                'izhikevich2007Cell:RS/b/nS': 1.0177979838287232,
                'izhikevich2007Cell:RS/c/mV': -48.063788481504965,
                'izhikevich2007Cell:RS/d/pA': 345.5017511454606,
                'izhikevich2007Cell:RS/k/nS_per_mV': 0.11978069117890949,
                'izhikevich2007Cell:RS/vpeak/mV': 36.429955149569174,
                'izhikevich2007Cell:RS/vr/mV': -76.17888228360782,
                'izhikevich2007Cell:RS/vt/mV': -35.93520240084242}
                
                        

sweep_numbers = [34,38,42,46,50,54,58]


with open("471141261_analysis.json", "r") as json_file:
    metadata = json.load(json_file)

ref0 = 'Pop0/0/RS/v:'
ref1 = 'Pop0/1/RS/v:'
ref5 = 'Pop0/5/RS/v:'
ref6 = 'Pop0/6/RS/v:'

minimum0 = ref0+'minimum'
average_last_1percent0 = ref0+'average_last_1percent'
minimum1 = ref1+'minimum'


weights_1 = {minimum0: 1,
             average_last_1percent0: 1,
             minimum1: 1}

sw0 = "%s"%sweep_numbers[0]
sw1 = "%s"%sweep_numbers[1]
sw5 = "%s"%sweep_numbers[5]
sw6 = "%s"%sweep_numbers[6]

target_data_1 = {minimum0:               metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":minimum"],
                 average_last_1percent0: metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":average_last_1percent"],
                 minimum1:               metadata['sweeps'][sw1]["pyelectro_iclamp_analysis"][sw1+":minimum"]}

average_maximum6 = ref6+'average_maximum'
average_minimum6 = ref6+'average_minimum'
mean_spike_frequency6 = ref6+'mean_spike_frequency'
mean_spike_frequency5 = ref5+'mean_spike_frequency'

weights_2 = {average_maximum6: 1,
           average_minimum6: 1,
           mean_spike_frequency6: 1,
           mean_spike_frequency5: 1}

target_data_2 = {average_maximum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_maximum"],
                 average_minimum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_minimum"],
                 mean_spike_frequency6: metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":mean_spike_frequency"],
                 mean_spike_frequency5: metadata['sweeps'][sw5]["pyelectro_iclamp_analysis"][sw5+":mean_spike_frequency"]} 

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
                     dt =               0.025):
                         
    ref = '%s__s%s_p%s_m%s_s%s_o%s_m%s_e%s'%(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites)           

    return run_optimisation(prefix =           ref, 
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
                     
def scale(scale, number, min=1):
    return max(min, int(scale*number))

def reload_standard_dat_file(file_name):
    
    dat_file = open(file_name)
    data = {}
    indeces = []
    for line in dat_file:
        words = line.split()
        
        if not data.has_key('t'):
            data['t'] = []
            for i in range(len(words)-1):
                data[i] = []
                indeces.append(i)
        data['t'].append(float(words[0]))
        for i in range(len(words)-1):
            data[i].append(float(words[i+1]))
            
    print("Loaded data from %s, %s"%(file_name, indeces))
    
    return data, indeces
    
def compare(sim_data_file):
    dat_file_name = '../AllenInstituteNeuroML/CellTypesDatabase/data/471141261.dat'
    
    data, indeces = reload_standard_dat_file(dat_file_name)
    
    for ii in indeces:
        plt.plot(data['t'],data[ii], color='grey')
        
    data, indeces = reload_standard_dat_file(sim_data_file)
    
    for ii in indeces:
        plt.plot(data['t'],data[ii])
        
    plt.show()
            

if __name__ == '__main__':
    
    nogui = '-nogui' in sys.argv
    
    if '-compare' in sys.argv:
        
        compare('NT_AllenIzh__s12345_p200_m600_s80_o60_m0.1_e2_Mon_Nov_30_12.30.28_2015/AllenIzh__s12345_p200_m600_s80_o60_m0.1_e2.Pop0.v.dat')
        
    elif '-one' in sys.argv:
        
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
        
    elif '-mone' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        
        cont = NeuroMLController('AllenTest', 
                                 'models/RS/AllenTestMulti.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.01, 
                                 simulator)
                                 
        example_vars = {'cell:RS/channelDensity:IM_all/mS_per_cm2': 0.298616048828908,
                        'cell:RS/channelDensity:Kd_all/mS_per_cm2': 10.01185622839693,
                        'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2': 0.09709819705345717,
                        'cell:RS/channelDensity:Na_all/mS_per_cm2': 89.52537116523236,
                        'cell:RS/erev_id:IM_all/mV': -79.75855615087383,
                        'cell:RS/erev_id:Kd_all/mV': -72.09249355952414,
                        'cell:RS/erev_id:LeakConductance_all/mV': -77.72370827350683,
                        'cell:RS/erev_id:Na_all/mV': 51.57661143347139,
                        'cell:RS/specificCapacitance:all/uF_per_cm2': 0.5217289166700633}

        sim_vars = OrderedDict(example_vars)
                                
                                 
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
    elif '-izhone' in sys.argv:
        
        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'
        
        cont = NeuroMLController('AllenIzhTest', 
                                 'models/RS/AllenIzh.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.05, 
                                 simulator)
                                 

        sim_vars = OrderedDict(example_vars_iz)
                                
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
    elif '-izhmone' in sys.argv:
        
        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'
        
        cont = NeuroMLController('AllenIzhMulti', 
                                 'models/RS/AllenIzhMulti.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.05, 
                                 simulator)

        sim_vars = OrderedDict(example_vars_iz)
                                
        t, v = cont.run_individual(sim_vars, show=(not nogui))
        
        
        
    elif '-izhquick' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        
        scale1 = 0.1
        
        report = run_one_optimisation('AllenIzh',
                            12345,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'models/RS/AllenIzh.net.nml',
                            target =           'network_RS',
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz)
        
        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']))
        
        
    elif '-izhquick' in sys.argv:
        
        simulator  = 'jNeuroML_NEURON'
        
        scale1 = 0.1
        
        report = run_one_optimisation('AllenIzh',
                            12345,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'models/RS/AllenIzh.net.nml',
                            target =           'network_RS',
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz)
        
        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']))
        
        
        
        
    
        
    elif '-quick' in sys.argv:

        run_one_optimisation('AllenTestQ',
                            1234,
                            population_size =  4,
                            max_evaluations =  8,
                            num_selected =     2,
                            num_offspring =    2,
                            mutation_rate =    0.9,
                            num_elites =       1,
                            simulator =        simulator,
                            nogui =            nogui)
                            
    elif '-2stage' in sys.argv:
        
        print("Running 2 stage optimisation")
        
        parameters = ['cell:RS/channelDensity:LeakConductance_all/mS_per_cm2',
                      'cell:RS/erev_id:LeakConductance_all/mV',
                      'cell:RS/specificCapacitance:all/uF_per_cm2',
                      'cell:RS/channelDensity:Na_all/mS_per_cm2',
                      'cell:RS/channelDensity:Kd_all/mS_per_cm2',
                      'cell:RS/channelDensity:IM_all/mS_per_cm2',
                      'cell:RS/erev_id:Na_all/mV',
                      'cell:RS/erev_id:Kd_all/mV',
                      'cell:RS/erev_id:IM_all/mV']


        max_constraints_1 = [0.1,   -70,  2,   0, 0, 0, 55, -80, -80]
        min_constraints_1 = [0.001, -100, 0.2, 0, 0, 0, 55, -80, -80]
        
        # For a quick test...
        # max_constraints_1 = [0.1,   -77.9, 0.51,   0, 0, 0, 55, -80, -80]
        # min_constraints_1 = [0.09,  -77.8, 0.52,   0, 0, 0, 55, -80, -80]
        
        max_constraints_2 = ['x',   'x',   'x',    100,  25,   4,    60, -70,  -70]
        min_constraints_2 = ['x',   'x',   'x',    20,   1,    1e-6, 50, -100, -100]
        

        
        scale1 = 0.1
        scale2 = 0.05
        
        run_2stage_optimization('Allen2stage',
                                neuroml_file =     'models/RS/AllenTestMulti.net.nml',
                                target =           'network_RS',
                                parameters = parameters,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.01,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.025,
                                population_size_1 = scale(scale1,50,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,200,20),
                                max_evaluations_2 = scale(scale2,500,10),
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,20,5),
                                num_offspring_2 = scale(scale2,20,5),
                                mutation_rate = 0.1,
                                num_elites = 2,
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = True,
                                seed = 1234,
                                known_target_values = {},
                                dry_run = False)

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
        


