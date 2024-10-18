
![logo]()
# pop-up-ide

*Interactive Python-editor that allows nondestructive examination of host code*

## Table of Contents

- [What does pop-up-ide do?](#what-does-pop-up-ide-do)
- [Limitations](#limitations)
- [Quick-start](#quick-start)
  - [Installation](#installation)
  - [Getting started](#getting-started)

## What does pop-up-ide do?

When placed in code, pop-up-ide creates a new virtual environment with a copy of host namespace.
Inside the virtual environment host variables and functions can be used in an interactive code execution environment without afftecting state of the original namespace.

## Limitations

Currently pop-up-ide lacks capability to copy variables that use C under the hood (such as numpy arrays or pandas dataframes) unless they are wrapped inside Python functions.

```
def zeros():
    return np.zeros([50,50])
```
*Wrapping variables utilizing C with functions allows them to be used inside pop-up-ide.*

Operating system: pop-up-ide can currently used only in linux environments.

## Quick-start

### Installation

1. Run ```pip install pop-up-ide```

### Getting started

1. Include ```from pop_up_ide import ide, scope``` in your python files imports.

2. Place ```ide(scope())``` in your code.

Placement is not trivial. Only variables and functions declared before the ```ide(scope())``` -function call will be included in the interactive code execution environment.

```
variable_1 = 1

def function_1(a):
    return a

ide(scope())

variable_2 = 2

def function_2(a):
    return a
```
*Only variable_1 and function_1 can be found in the pop-up-ide code execution environment in this case.*

By inheriting the namespace in a precise code execution state, pop-up-ide can be used like a debugging tool.

3. Run your code. When Python interpreter comes to line with: ```ide(scope())```, it will launch pop-up-ide.

*Note!*
*When pop-up-ide is launched the first time, installation of necessary dependencies takes some time.*
*Launching pop-up-ide to the same environment later is faster.*

4. pop-up-ide creates virtual environment 'pop_up_env' to your directory.

5. pop-up-ide opens to your local terminal or xterm if you have xterm installed.

6. Inside pop-up-ide, most of Python functionalities can be used. pop-up-ide's code execution environment is interactive and it attempts to execute once two empty lines have been entered.

![xterm_example]()
*Using standard Python in pop-up-ide.*

*Note!*
*Any changes made inside pop-up-ide to variables or functions loaded from host environment will not take place in the host namespace.*
*Any variables or functions created inside pop-up-ide will not be available in the host environment, when pop-up-ide has been closed.*

*Tip!*
*pop-up-ide launches with PySide2 installed allowing for images and graphs to open in a separate window for easy saving.*

7. Exit pop-up-ide by typing 'exit' or 'exit & delete environment' inside pop-up-ide. After this your host Python interpreter will continue executing the rest of your code.