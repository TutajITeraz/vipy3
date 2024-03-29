# vipy3
Visual Python programming tool that supports pytorch, based on node editor provided by dear pygui

## Requirements
```
    python -m pip install -r requirements.txt
```

## Using 
```
    python -m vipy3.kickstart
```

### Example: Simple addition and code generation:

![Addition example](README_img/sneak_peak_simple_add.gif?raw=true "Example 1")


### Example: Training and evaluating network using pytorch:

![PyTorch example](README_img/vipy_ai.webp?raw=true "Example 2")


TODO
====
Work In Progress:
-----------------
* FOR pass args to exe function, get iter, get last element
* reimplement pytorch nodes
* more input types
* FOR2 gen code
* FOR2 get all args

High (engine) priority:
-----------------------
* Fix imports in code gen

Medium priority:
----------------
* Last saved path and Main meta node in window titlebar
* Closing meta_node and main meta_nodes
* Removing nodes should del objects
* Executing meta-node without dpg gui
* Removing meta node in/outs should remove node attributes too
* Meta-node input disconnect
* For last result output and recurency
* replace lambda a,b,c with proper solution
* Specify function types and return types
* add nodes to workspace by themselves
* Documentation and private methods
* InConnX serialize/deserialize could use parents methods

Low priority:
-------------
* dialog box on error
* copy-paste nodes
* MetaNode from selection
* Node creator / node code editor
* Node outputs - align to right
* Prettier node colors
* Smaller nodes style
* Attrs colors based on type

Blocked:
--------
* Create right click menu in node editor
* re-wiring nodes

Author: Łukasz Bolda