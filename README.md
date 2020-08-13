# Experimenting with splitting solids and using mypy

Update 2020-08-13:

As I started the day I was having one last problem running mypy. This is after incorporating
the changes from Adam as well as my [PR #435](https://github.com/CadQuery/cadquery/pull/435) which
add `py.typed`:
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/splitting (master)
$ mypy workplane.py 
Traceback (most recent call last):
  File "/opt/miniconda3/envs/cq-dev/bin/mypy", line 8, in <module>
    sys.exit(console_entry())
  File "/opt/miniconda3/envs/cq-dev/lib/python3.7/site-packages/mypy/__main__.py", line 8, in console_entry
    main(None, sys.stdout, sys.stderr)
  File "mypy/main.py", line 89, in main
  File "mypy/build.py", line 180, in build
  File "mypy/build.py", line 252, in _build
  File "mypy/build.py", line 2626, in dispatch
  File "mypy/build.py", line 2942, in process_graph
  File "mypy/build.py", line 3020, in process_fresh_modules
  File "mypy/build.py", line 1955, in fix_cross_refs
  File "mypy/fixup.py", line 25, in fixup_module
  File "mypy/fixup.py", line 91, in visit_symbol_table
  File "mypy/nodes.py", line 515, in accept
  File "mypy/fixup.py", line 105, in visit_overloaded_func_def
  File "mypy/types.py", line 1296, in accept
  File "mypy/fixup.py", line 196, in visit_overloaded
  File "mypy/types.py", line 1098, in accept
  File "mypy/fixup.py", line 182, in visit_callable_type
  File "mypy/types.py", line 1724, in accept
  File "mypy/fixup.py", line 251, in visit_union_type
  File "mypy/types.py", line 794, in accept
  File "mypy/fixup.py", line 153, in visit_instance
  File "mypy/fixup.py", line 262, in lookup_qualified_typeinfo
  File "mypy/fixup.py", line 290, in lookup_qualified
  File "mypy/fixup.py", line 299, in lookup_qualified_stnode
  File "mypy/lookup.py", line 47, in lookup_fully_qualified
AssertionError: Cannot find component 'Message' for 'OCP.Message.Message_ProgressIndicator'
```
To make a long story short, see the comments in PR #435, if I use the master branch of mypy
all is well!!!!
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/splitting (master)
$ mypy workplane.py 
mypy.main:+ WINK
Success: no issues found in 1 source file
```

---

Update: Adam has merged [PR #430](https://github.com/CadQuery/cadquery/pull/430) and
now there is only one error when I use stubgen to generate `*.pyi` files. Additonally,
he educated me on how [@overload](https://docs.python.org/3/library/typing.html#typing.overload) works.



---

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
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/splitting (master)
$ cp ~/prgs/CadQuery/forks/cadquery/mypy.ini .
```
- Edit mypy.ini adding mypy_path to [mypy] section which points to the `stubs` directory created above:
```
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/splitting (master)
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
(cq-dev) wink@3900x:~/prgs/CadQuery/projects/splitting (master)
$ time mypy *.py
splitting.py:4: error: Argument 1 to "Workplane" has incompatible type "str"; expected "Union[Vector, Location, Shape]"
splitting.py:6: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
splitting.py:14: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
splitting.py:22: error: Argument 1 to "faces" of "Workplane" has incompatible type "str"; expected "Optional[Selector]"
Found 4 errors in 1 file (checked 1 source file)

real	0m22.792s
user	0m22.527s
sys	0m0.237s
```

So, `mypy` is detecting some errors, not sure if it's my problem or cadquery.


Written in python using the [CadQuery](https://github.com/CadQuery/cadquery) framework.
