import os.path
import os
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

import matplotlib.pyplot as pylab


def plot_it(x, y, xlabel, ylabel, trace, title=None):

    if not title:
        title = '%s vs %s'%(xlabel, ylabel)
        
    fig = pylab.figure()
    fig.canvas.set_window_title(title)

    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    pylab.grid('on')
    
    pylab.plot(x,y,trace)

refs = []

for f in os.listdir('.'):
    if os.path.isdir(f) and f.startswith("NT_"):
        refs.append(f)
    
print(refs)

info = {}
for ref in refs:
    report = ref+'/report.json'
    print('Reading info from %s'%report)
    if os.path.isfile(report):
        rep_str = open(report).read().replace('\'','"')
        data = json.loads(rep_str)
        print('    %s'%data['comment'])
        info[ref] = data
    else:
        
        print('***** Missing report: %s'%report)
    
#pp.pprint(info)

muts = []
fitnesses = []
pop_sizes = []
max_evals = []

for ref in info.keys():
    data = info[ref]
    fitnesses.append(float(data['fitness']))
    muts.append(float(data['mutation_rate']))
    pop_sizes.append(int(data['population_size']))
    max_evals.append(int(data['max_evaluations']))
    
plot_it(muts, fitnesses, 'Mutation rate', 'Fitness', 'ko')
plot_it(pop_sizes, fitnesses, 'Population size', 'Fitness', 'ko')
plot_it(max_evals, fitnesses, 'Max evaluations', 'Fitness', 'ko')
    
pylab.show()