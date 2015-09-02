"""

   Helper script for running on UCL's supercomputing cluster. 
   No guarantee that this is useful/usable anywhere else...
   
"""

from jinja2 import Template
import time
import os

from pyneuroml.pynml import execute_command_in_dir

class SubmitHelper():
    
    template = """#!/bin/bash
#$ -V               # preserve environment variables
#$ -S /bin/bash     # specify which shell to use
#$ -cwd             # cd to current folder before executing the script

#$ -o {{ remote_dir }}/log_{{ task }}    # redirect standard output
#$ -e {{ remote_dir }}/log_{{ task }}    # redirect standard error
#$ -j y

#$ -l tmem=8G             # max memory limit
#$ -l h_vmem=8G           # max memory limit
#$ -l h_rt={{ runtime }}  # max runtime
#$ -l h_stack=1G          # hard limit on max stack size (SGE sets this to 'unlimited' by default and this can cause some applications to crash)

#$ -N  {{ task }}

##======END OF SGE OPTIONS===========

echo "Starting {{ task }}..."

{{ command }}

echo "Done {{ task }}!"

    """
    
    def __init__(self, username, host):
        self.username = username
        self.host = host
    
uclClusterSubmit = SubmitHelper('ucgbpgl', 'pryor.cs.ucl.ac.uk')

def run_remotely(command, task, remote_dir, runtime='01:00:00', submit_helper=uclClusterSubmit):

    variables = {}
    
    task_full = '%s_%s'%(task, time.ctime().replace(' ','_' ).replace(':','.' ))
    
    variables['command'] = command
    variables['task'] = task_full
    variables['remote_dir'] = remote_dir
    variables['runtime'] = runtime

    t = Template(submit_helper.template)

    contents = t.render(variables)
    
    tmp_script_name = 'submit_%s'%(task_full)
    tmp_script = open(tmp_script_name,'w')
    tmp_script.write(contents)
    tmp_script.close()
    
    '''
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(contents)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")'''
    
    
    scp_cmd = 'scp "%s" "%s@%s:%s"' % (tmp_script_name, submit_helper.username, submit_helper.host, remote_dir)
    print execute_command_in_dir(scp_cmd, '.', True)
    
    ssh_cmd = "ssh %s@%s \"cd %s;/bin/bash -ci  'qsub %s'\"" % (submit_helper.username, submit_helper.host, remote_dir, tmp_script_name)

    print execute_command_in_dir(ssh_cmd, '.', True)
    
    return tmp_script_name
      
        
        
        
if __name__ == '__main__':
    
    tmp_script_name = run_remotely('pwd\nls -alt', 'TestTask', '/home/ucgbpgl/git/testtune')