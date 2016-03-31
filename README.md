# multi.py

multi Python module, for simple running of multiple processes simultaneously using subprocess.

Simply download multi.py, place it in the same folder as a script you’re running, and then ``import multi`` to use!

Here is a very simple example:

```python
import multi

# commands to run
cmds  = [
            # subprocess commands are issued as lists unless shell=True
            ['echo', 'hello', 'world'],
            ['echo', 'hello', 'world', '2'],
            ['sleep', '5'],
            ['sleep', '2']
        ]
# list of names for commands
names = ['echo', 'echo', 'sleep', 'sleep']
# number of processes to run concurrently
max_processes = 2

# do it!
multi.do_processes(cmds, names = names, max_processes = max_processes, logtime=3)
```
