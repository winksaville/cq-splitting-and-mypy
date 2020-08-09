# Experimenting with spliting solids and using mypy

I asked for help on the cq group, see: https://groups.google.com/g/cadquery/c/DFVe83-Ctb8/m/w_WI91LkCwAJ.

And did the following, it's not quite working but does something:

- Install OCP-stubs into your cq python environment:
  - pip install git+https://github.com/CadQuery/OCP-stubs.git

- Be sure mypy is installed in the conda environment you're using.
Initially I was accidentally using the version installed on my
Arch Linux system and thus the OCP-stubs weren't found.

After those two steps, mypy worked in my cadquery fork (Note: took 45secs on my system):
```
(cq-dev) wink@3900x:~/prgs/CadQuery/forks/cadquery (master)
$ time mypy cadquery
Success: no issues found in 20 source files

real	0m45.734s
user	0m45.316s
sys	0m0.360s
```

Next step is to get `mypy` to work in one of my projects. I did the following:

- Use `stubgen` to create stubs for cadquery. From your cadquery fork/checkout do (Note: took 30secs on my system):
```
(cq-dev) wink@3900x:~/prgs/CadQuery/forks/cadquery (master)
$ time stubgen cadquery -o stubs
Processed 20 modules
Generated files under stubs/cadquery/

real	0m29.091s
user	0m28.700s
sys	0m0.357s
```

- Copy [mypy.ini from cadquery repo](https://github.com/CadQuery/cadquery/blob/master/mypy.ini) to the root of your cadquery project.
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/spliting (master)
$ cp ~/prgs/CadQuery/forks/cadquery/mypy.ini .
```
- Edit mypy.ini adding mypy_path to [mypy] section which points to the `stubs` directory created above:
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/spliting (master)
$ cat -n mypy.ini 
     1	[mypy]
     2	ignore_missing_imports = False 
     3	mypy_path = ~/prgs/CadQuery/forks/cadquery/stubs
     4	
     5	[mypy-logbook.*]
     6	ignore_missing_imports = True
     7	
     8	[mypy-ezdxf.*]
     9	ignore_missing_imports = True
    10	
    11	[mypy-pyparsing.*]
    12	ignore_missing_imports = True
    13	
    14	[mypy-IPython.*]
    15	ignore_missing_imports = True
````
Execute mypy on *.py files, this first time is slow as it creates the .mypy_cache:
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/spliting (master)
$ time mypy *.py
spliting.py:4: error: Argument 1 to "Workplane" has incompatible type "str"; expected "Union[Vector, Location, Shape]"
spliting.py:6: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
spliting.py:14: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
spliting.py:22: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
Found 4 errors in 1 file (checked 1 source file)

real	0m22.792s
user	0m22.527s
sys	0m0.237s
```

So, `mypy` is detecting some errors, not sure if it's my problem or cadquery.


Written in python using the [CadQuery](https://github.com/CadQuery/cadquery) framework.
