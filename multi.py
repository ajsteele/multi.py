'''multi module, for simple running of multiple processes simultaneously.'''

import os
import time
import math
import subprocess


def suffix_filename(filename, suffix):
   '''Return the file basename, plus suffix, then extension.

   Example:
      suffix_filename('file.ext', '_01') returns 'file_01.ext'
   '''
   # return the file basename, plus the suffix, plus its extension
   return os.path.splitext(filename)[0] + suffix + \
      os.path.splitext(filename)[1]


def start_process(commands, envs, shell, names, processes, i, output_file):
   '''Start a single process with subprocess.

   Arguments:
      commands, envs, shell, names -- passed from do_processes
      processes -- list, currently running processes (returned by this function)
      i         -- int, index of processes to be running
      output_file -- string, basename.ext for base output filename
   '''
   # create a 0-padded i for pretty output
   i_padded = ('{0:0' +
      str(int(math.ceil(math.log10(len(commands))))) + 'd}').format(i)
   if shell: # the command is a raw string, so just print it
      print i_padded + ': ' + commands[i]
   else: # the command is potentially a list of args, so join it with spaces
      print i_padded + ': ' + ' '.join(commands[i])

   if names is not None: # if we have task names, use them for filename suffices
      task_suffix = '_' + names[i] + '_' + i_padded
   else: # if not, just use the numbers
      task_suffix = '_' + i_padded
   output_i = suffix_filename(output_file, task_suffix)

   # in case we already have this task name, check whether a unique suffix
   # should be added
   unique_suffix_i = 1 # start from 1
   output_i_original = output_i # remember the original name in case we need it
   while os.path.isfile(output_i):
      unique_suffix = '_' + str(unique_suffix_i)
      output_i = suffix_filename(output_i_original, unique_suffix)
      unique_suffix_i += 1 # increment suffix in case this didn't work...

   subprocess_args = {
      'args': commands[i],
      'stdout': open(output_i, 'w'),
      'stderr': subprocess.STDOUT,
      'shell': shell
   }
   if envs is not None:
      subprocess_args['env'] = envs[i]
   processes.append(subprocess.Popen(**subprocess_args))
   return processes


def check_processes(
      commands, envs, shell, names, processes, max_processes, i, output_file
   ):
   '''Check running processes, and add more if there is space to do so.'''

   for j in reversed(range(len(processes))): # check processes in reverse order
      if processes[j].poll() is not None: # if process not finished return None
         del processes[j] # remove from list - this is why reverse order
   # More to do and some spare slots
   while len(processes) < max_processes and i < len(commands): 
      processes = start_process(
                     commands, envs, shell, names, processes, i, output_file
                  )
      i += 1
   return processes, i


def do_processes(
      commands, envs = None, shell = False, names = None, max_processes = 1,
      output_file = 'multipy.out', polltime = 1.0, logtime = 600
   ):
   '''Run some processes in parallel.

   Arguments:
      commands  -- list, each item a subprocess command
      envs      -- optional list, each item a subprocess environment variable
      shell     -- optional bool, subprocess's shell argument, default False
      names     -- optional list, each item a string representing this task name
      max_processes -- int, how many processes you'd like to run at a time
      output_file -- string, basename.ext for base output filename
      polltime  -- time in seconds between checks on running processes
      logtime   -- time in seconds between writing a log message to the console
   '''
   
   time_start = time.time()
   print 'Starting multiprocessing with ' + str(len(commands)) + \
   ' commands, performing ' + str(max_processes) + ' concurrently.'
   processes, i = check_processes(commands, envs, shell, names, [],
   max_processes, 0, output_file) # This will start max_processes things running
   j = 0
   while (len(processes) > 0): # if something still running
      time.sleep(polltime)
      if(time.time() - time_start - j*logtime > 0):
         print time.strftime('%Y/%m/%d %H:%M:%S') + ' ' + str(len(processes)) +\
         ' processes running...'
         j += 1
      processes, i = check_processes(
                        commands, envs, shell, names, processes, max_processes,
                        i, output_file
                     )