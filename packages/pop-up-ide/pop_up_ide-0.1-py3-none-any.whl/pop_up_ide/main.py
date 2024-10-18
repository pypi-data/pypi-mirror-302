import re
import os
import sys
import dill
import venv
import shutil
import inspect
import builtins
import subprocess
import urllib.request
import importlib.metadata
from types import ModuleType as module, FunctionType

# Adjust sys.path to ensure the directory is included
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Now use an absolute import
from utils import _PopUpIdeUtils

# Rest of the imports for the terminal functionality
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import PythonLexer
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from prompt_toolkit.key_binding import KeyBindings


class _PopUpScope:
    def __init__(self):
        self.scope_func = globals  

    @classmethod
    def scope(cls):
        # Get the local variables from the calling frame
        caller_frame = inspect.currentframe().f_back
        local_vars = caller_frame.f_locals

        # Filter the local variables for functions, data types, and user-defined objects
        cls.variable_scope = {
            k: v for k, v in local_vars.items() 
            if not k.startswith('__')  # Exclude system variables
            and (callable(v) or isinstance(v, (int, float, str, list, dict, set, tuple)))  # Capture functions and data types
            and k not in dir(__builtins__)  # Exclude built-in functions and variables
        }

        # Capture only the modules that were explicitly imported by the user, not system modules
        cls.imported_modules = {}
        for name, module in sys.modules.items():
            if module and hasattr(module, '__file__'):  # Modules with a file path (not built-ins)
                cls.imported_modules[name] = module

        # Capture local module aliases like `import numpy as np`
        cls.aliases = {}
        for k, v in local_vars.items():
            if isinstance(v, type(sys)):  # If the value is a module
                if v.__name__ in cls.imported_modules:  # Ensure it's an imported module
                    cls.aliases[k] = v.__name__

        print(f"Captured scope: {cls.variable_scope}")
        print(f"Captured imported modules: {list(cls.imported_modules.keys())}")
        print(f"Captured module aliases: {cls.aliases}")

        return cls  # Return the class itself

    @classmethod
    def get_scope(cls):
        # Dynamically return the latest scope stored
        return cls.variable_scope
    
    @classmethod
    def get_imported_modules(cls):
        # Return only the names of the imported modules
        return cls.imported_modules
    
    @classmethod
    def get_aliases(cls):
        # Return the module aliases, like np for numpy
        return cls.aliases

# Define the classes for environment management, utils, and terminal operations here...
class _PopUpIdeEnvManager:

    @staticmethod
    def extract_imported_modules_with_aliases(scope):
        """Extract imported modules and aliases from the provided scope."""
        imported_modules = {}
        for key, value in scope.items():
            if isinstance(value, type(sys)):  # Check if it's a module
                module_name = value.__name__.split('.')[0]
                imported_modules[key] = module_name
        return imported_modules


    @staticmethod
    def create_requirements_file(imported_modules=None):
        env_name='pop_up_venv'
        requirements_file='requirements.txt'
        """Create requirements.txt and include any dynamically found imported modules."""
        # Get the already installed packages
        installed_packages = importlib.metadata.distributions()
        requirements = [f"{pkg.metadata['Name']}=={pkg.version}" for pkg in installed_packages]

        # Ensure prompt_toolkit, pygments, dill, etc. are included if used in the code
        required_packages = {"dill", "prompt_toolkit", "pygments"}
        
        # Add dynamically found modules (if any)
        if imported_modules:
            required_packages.update(imported_modules.values())

        # Only add packages that aren't already installed
        existing_packages = {pkg.split("==")[0].lower() for pkg in requirements}
        for package in required_packages:
            if package not in existing_packages:
                requirements.append(package)

        # Write the packages to the requirements.txt file in the virtual environment directory
        requirements_path = os.path.join(env_name, requirements_file)
        with open(requirements_path, 'w') as f:
            f.write("\n".join(requirements))

        print(f"Requirements saved to {requirements_path}")
        return requirements_path


    @staticmethod
    def install_packages(requirements_file):
        env_name = 'pop_up_venv'
        pip_path = os.path.join(env_name, 'bin', 'pip')
        install_flag_file = os.path.join(env_name, 'installed_packages.flag')

        def is_installed(package_name):
            """Check if a package is installed in the virtual environment."""
            try:
                importlib.metadata.version(package_name)
                return True
            except importlib.metadata.PackageNotFoundError:
                return False

        # First-time installation: if no flag file exists
        if not os.path.exists(install_flag_file):
            print("Installing all packages for the first time...")
            # Install all packages in the requirements file
            with open(requirements_file, 'r') as f:
                packages = [line.strip() for line in f if line.strip()]

            for package in packages:
                package_name = package.split('==')[0]
                print(f"Installing {package_name}...")
                subprocess.run([pip_path, 'install', package])

            # Ensure specific packages are installed
            for pkg in ['dill', 'prompt_toolkit', 'pygments']:
                print(f"Ensuring {pkg} is installed...")
                subprocess.run([pip_path, 'install', pkg])

            # Create a flag file to indicate that packages have been installed
            with open(install_flag_file, 'w') as flag_file:
                flag_file.write("Packages installed")

            print("All packages installed. Flag created.")
        
        else:
            # Subsequent runs: only check if required packages are installed
            print("Checking if additional packages are needed...")

            # Read the requirements file to get a list of packages
            with open(requirements_file, 'r') as f:
                packages = [line.strip() for line in f if line.strip()]

            for package in packages:
                package_name = package.split('==')[0]
                if not is_installed(package_name):
                    print(f"Installing {package_name}...")
                    subprocess.run([pip_path, 'install', package])
                else:
                    print(f"{package_name} is already installed. Skipping...")

            # Ensure required packages (dill, prompt_toolkit, pygments) are installed
            for pkg in ['dill', 'prompt_toolkit', 'pygments']:
                if not is_installed(pkg):
                    print(f"Ensuring {pkg} is installed...")
                    subprocess.run([pip_path, 'install', pkg])
                else:
                    print(f"{pkg} is already installed. Skipping...")

        print("Package installation check complete.")


    @staticmethod
    def create_virtualenv():
        env_name='pop_up_venv'
        try:
            venv.create(env_name, with_pip=True)
            # print(f"Virtual environment '{env_name}' created.")
        except subprocess.CalledProcessError as e:
            print(f"Error during virtual environment creation: {e}")
            # print("Attempting to install pip manually.")
            try:
                print("Downloading get-pip.py...")
                url = "https://bootstrap.pypa.io/get-pip.py"
                get_pip_path = os.path.join(env_name, "get-pip.py")
                urllib.request.urlretrieve(url, get_pip_path)
                subprocess.run([os.path.join(env_name, 'bin', 'python'), get_pip_path])
                # print("Pip installed using get-pip.py.")
            except Exception as manual_pip_error:
                print(f"Failed to manually install pip: {manual_pip_error}")
        except Exception as general_error:
            print(f"Unexpected error during virtual environment creation: {general_error}")


    @staticmethod
    def launch_in_new_terminal(variable_scope):
        env_name='pop_up_venv'
        """Launch a new terminal running `main.py` in the specified virtual environment."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        env_python_path = os.path.join(current_dir, env_name)
        main_script_path = os.path.join(env_name, 'main.py')
        
        def filter_user_scope(full_scope):
            filtered_scope = {}
            
            for k, v in full_scope.items():
                if not k.startswith('__') and k not in dir(__builtins__):
                    if callable(v):
                        try:
                            # Try getting the function source
                            func_source = inspect.getsource(v)
                            filtered_scope[k] = func_source  # Save the source code
                        except TypeError:
                            # Skip built-in or unsupported functions
                            continue
                    else:
                        filtered_scope[k] = v  # Keep non-callables as they are
            # print(f"Filtered scope (variables and functions as code): {filtered_scope}")
            return filtered_scope
        
        filtered_scope = filter_user_scope(variable_scope)
        # print(f"Filtered scope: {filtered_scope}")
        
        # Serialize the variables and store them in a file
        serialized_variables_path = os.path.join(env_name, 'variables.dill')
        with open(serialized_variables_path, 'wb') as f:
                dill.dump(filtered_scope, f, recurse=True)

        # print(f"Variables serialized and saved to {serialized_variables_path}")

        try:
            # Try to open program in a new xterm window
            subprocess.run([
                'xterm', '-hold', '-bg', 'linen', '-fa', 'Monospace', '-fs', '12',
                '-T', 'pop-up-ide', '-geometry', '60x24',
                '-e', f"PYTHONPATH={os.path.abspath(current_dir)}:{env_python_path} {env_name}/bin/python {main_script_path}"
            ])
        except FileNotFoundError:
            # If xterm is not found, fallback to running in the current terminal
            print("xterm is not installed. Running in the current terminal instead.")
            subprocess.run([
                f"{env_name}/bin/python", f"{main_script_path}"
            ])


    @staticmethod
    def copy_utils_to_env():
        """Copy pop_up_utils.py to the virtual environment."""
        env_name='pop_up_venv'
        utils_script_path = os.path.join(env_name, 'utils.py')
        with open(utils_script_path, 'w') as f:
            f.write("""
import dill
import os

class _PopUpIdeUtils:
    @staticmethod               
    def save_variables_to_env(variables):
        \"\"\"Save updated variables back to the virtual environment.\"\"\"
        env_name='pop_up_venv'
        file_path = f"{env_name}/variables.dill"
        with open(file_path, 'wb') as f:
            dill.dump(variables, f, recurse=True)
        #print(f"Variables updated in {file_path}")
                
    @staticmethod
    def load_variables_from_env():
        \"\"\"Load variables serialized in the virtual environment using `dill`.\"\"\"
        env_name='pop_up_venv'
        file_path = f"{env_name}/variables.dill"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                variables = dill.load(f)
            #print(f"Loaded variables from {file_path}")
            return variables
        else:
            print(f"No variable file found at {file_path}. Starting with an empty set.")
            return {}
    """)
        # print(f"Copied utils.py to {utils_script_path}")


def ide(env_specs):
    """Set up the virtual environment, save initial variables, and launch `main.py` in a new terminal."""
    env_name='pop_up_venv'
    # Get the absolute path of this script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script_path = os.path.join(current_dir, 'main.py')

    # Get the latest scope, imported modules, and aliases
    variable_scope = env_specs.get_scope()
    imported_modules = env_specs.get_imported_modules()
    aliases = env_specs.get_aliases()

    # Use the imported_modules and aliases as needed
    print(f"Imported modules: {imported_modules}")
    print(f"Aliases: {aliases}")

    # Extract imported modules and aliases
    imported_modules = _PopUpIdeEnvManager.extract_imported_modules_with_aliases(variable_scope)
    # Create and set up the virtual environment first
    _PopUpIdeEnvManager.create_virtualenv()

    # Ensure that the environment directory exists before copying
    env_main_script_path = os.path.join(env_name, 'main.py')
    if not os.path.exists(env_name):
        os.makedirs(env_name)

    # Copy `pop_up_main.py` to the virtual environment directory only if the paths differ
    if os.path.abspath(main_script_path) != os.path.abspath(env_main_script_path):
        shutil.copy(main_script_path, env_main_script_path)
        # print(f"Copied main logic to {env_main_script_path}")
    else:
        print(f"Source and destination paths are identical: {main_script_path}. Skipping copy.")

    # Continue with the setup: create requirements, install packages, etc.
    requirements_file = _PopUpIdeEnvManager.create_requirements_file(imported_modules=imported_modules)
    _PopUpIdeEnvManager.install_packages(requirements_file)
    _PopUpIdeEnvManager.copy_utils_to_env()

    # Save host variables to the environment
    _PopUpIdeUtils.save_variables_to_env(variable_scope)
    # print("All host variables have been copied to the virtual environment.")

    # Write to `pop_up_main.py` within the environment
    with open(env_main_script_path, 'w') as f:
        f.write("import re\n")
        f.write("import os\n")
        f.write("import dill\n")
        f.write("import sys\n")
        f.write("import builtins\n")

        # Dynamically write imports for the captured modules and aliases
        for alias, module in aliases.items():
            f.write(f"import {module} as {alias}\n")

        f.write("from utils import _PopUpIdeUtils\n")
        f.write("from prompt_toolkit import PromptSession\n")
        f.write("from prompt_toolkit.patch_stdout import patch_stdout\n")
        f.write("from prompt_toolkit.lexers import PygmentsLexer\n")
        f.write("from pygments.lexers import PythonLexer\n")
        f.write("from prompt_toolkit.completion import Completer, Completion\n")
        f.write("from pygments.styles import get_style_by_name\n")
        f.write("from prompt_toolkit.styles.pygments import style_from_pygments_cls\n")
        f.write("from prompt_toolkit.key_binding import KeyBindings\n")
        f.write("from utils import _PopUpIdeUtils\n")

        # Copy the `main` function definition and related classes from `pop_up_main.py`
        with open(main_script_path, 'r') as source:
            f.write(source.read())

        # Add condition to run the interactive environment if the --interactive flag is set
        f.write("\n\nif __name__ == '__main__':\n")
        f.write("    ide_main()\n")
        # print(f"Updated main logic in {env_main_script_path}")

    # Create a flag file to indicate the first run
    flag_file = os.path.join(env_name, 'first_run.flag')
    print("Launching pop-up-ide...")

    # Launch the environment in a new terminal only if the flag file doesn't exist
    if not os.path.exists(flag_file):
        with open(flag_file, 'w') as f:
            f.write('This file indicates that the terminal has already been launched.\n')
        _PopUpIdeEnvManager.launch_in_new_terminal(variable_scope)
    else:
        print("\n********************************************************************************************************\n    'first_run.flag' indicates that terminal has already been launched. \n    If this is not the case, delete 'first_run.flag' from pop_up_venv-directory and try again.\n********************************************************************************************************\n")


class _PopUpIdeBindings:
    # Custom key binding function to handle auto-closing
    @staticmethod
    def handle_autoclose_brackets(event):

        # Define auto-closing characters mapping
        BRACKETS = {
            '(': ')',
            '[': ']',
            '{': '}',
            '"': '"',
            "'": "'"
        }

        buffer = event.app.current_buffer
        char = event.data
        if char in BRACKETS:
            buffer.insert_text(char)
            buffer.insert_text(BRACKETS[char])
            buffer.cursor_left()

    bindings = KeyBindings()

    @bindings.add('(')
    @bindings.add('[')
    @bindings.add('{')
    @bindings.add('"')
    @bindings.add("'")
    
    @staticmethod
    def insert_autoclose_brackets(event):
        _PopUpIdeBindings.handle_autoclose_brackets(event)

class _PopUpIdeSystemFunctions:
    @staticmethod
    def is_function_call(user_input):
        match = re.match(r'(\w+)\((.*)\)', user_input)
        if match:
            function_name = match.group(1)
            arguments = match.group(2)
            # Check if it's a built-in function, and skip it
            if function_name in dir(builtins):
                return None, None
            return function_name, arguments
        return None, None

class _PopUpIdeTerminalOperations:
    @staticmethod
    def exit_virtualenv():
        """Gracefully exit the environment by removing the 'first_run.flag' and stopping the main loop."""
        env_name='pop_up_venv'
        # Remove the flag file to allow relaunching
        flag_file = os.path.join(env_name, 'first_run.flag')
        if os.path.exists(flag_file):
            os.remove(flag_file)
            print(f"Removed '{flag_file}', allowing the environment to be relaunched.")
        else:
            print(f"'{flag_file}' not found. Nothing to remove.")

        # Set an exit flag or call sys.exit() to break out of the loop in pop_up_main()
        global running
        running = False
        print("Exiting the interactive session. Goodbye!")
        # Try to close the terminal window using sys.exit() and subprocess
        try:
            # Exit the Python script
            sys.exit(0)
        except SystemExit:
            # If the terminal is still open, try sending a command to close it
            try:
                # Use `pkill` to close xterm if the terminal is still open
                subprocess.run(['pkill', 'xterm'])
            except Exception as e:
                print(f"Failed to close the terminal window: {e}")

    @staticmethod
    def exit_and_delete_virtualenv():
        """Gracefully delete the virtual environment by removing files and folders."""
        env_name='pop_up_venv'
        # Remove the flag file to allow relaunching
        flag_file = os.path.join(env_name, 'first_run.flag')
        if os.path.exists(flag_file):
            os.remove(flag_file)
            print(f"Removed '{flag_file}', allowing the environment to be relaunched.")
        else:
            print(f"'{flag_file}' not found. Nothing to remove.")

        # Exit the interactive session
        global running
        running = False
        print(f"Exiting the interactive session and preparing to delete the virtual environment '{env_name}'.")

        # Construct the command to delete the virtual environment folder
        delete_command = f"rm -rf {env_name}"

        # Run the deletion command after exiting the script
        try:
            # Exit the Python script
            sys.exit(0)
        except SystemExit:
            # Use `subprocess` to run the delete command
            try:
                print(f"Deleting the virtual environment '{env_name}'...")
                subprocess.run(delete_command, shell=True)
                print(f"Virtual environment '{env_name}' deleted successfully.")
                # Use `pkill` to close xterm if the terminal is still open
                subprocess.run(['pkill', 'xterm'])
            except Exception as e:
                print(f"Failed to delete the virtual environment: {e}")

class _PythonCompleter(Completer):
    def get_completions(self, document, complete_event):
        # Get current input text before the cursor
        text_before_cursor = document.text_before_cursor
        python_keywords = ['def', 'class', 'import', 'from', 'print', 'for', 'while', 'if', 'else', 'elif', 'return']
        all_globals = list(globals().keys())
        do_not_suggest_these = ['os', 're', 'ast', 'sys', 'importlib', 'builtins', 'dill', 'shutil', 'inspect', 'module',
                                'venv', 'subprocess', 'urllib', 'prompt', 'PromptSession', 'FunctionType', 'current_dir', 
                                'patch_stdout', 'PygmentsLexer', 'PythonLexer', 'get_style_by_name',  
                                'style_from_pygments_cls', 'Completer', 'Completion', 'ide', '_PopUpScope',
                                '_PopUpIdeUtils', '_PopUpIdeEnvManager', 'ide_main', '_PopUpIdeBindings', '_PopUpIdeSystemFunctions',
                                '_PopUpIdeTerminalOperations', '_PythonCompleter', 
                                'KeyBindings', '__package__', '__spec__', '__warningregistry__',
                                '__loader__', '__name__', '__annotations__',
                                '__doc__', '__builtins__', '__file__', '__cached__',
                                'self', 'document', 'variables', 'scope',
                                'complete_event', 'text_before_cursor', 'python_keywords',
                                'all_globals', 'globals_without_do_not_suggest_these', 'do_not_suggest_these',
                                ]
        
        globals_without_do_not_suggest_these = [i for i in all_globals if i not in do_not_suggest_these]

        all_locals = list(locals().keys())
        locals_without_do_not_suggest_these = [i for i in all_locals if i not in do_not_suggest_these]

        include_these = ['clear', 'exit', 'exit & delete environment']

        # Combine suggestions, prioritizing local variables first, followed by global variables, and then keywords and built-in functions
        words_ordered = locals_without_do_not_suggest_these + include_these + globals_without_do_not_suggest_these + python_keywords + dir(builtins)

        # Ensure unique suggestions by converting the list to a set and back to list
        words = list(dict.fromkeys(words_ordered))

        # Suggest completions inside parentheses as well
        # Extract the current word being typed, even if it's within parentheses
        current_word = self._get_current_word(text_before_cursor)

        # Generate completions based on the current word being typed
        for word in words:
            if word.startswith(current_word):
                yield Completion(word, start_position=-len(current_word))

    def _get_current_word(self, text):
        """
        Extracts the word currently being typed. Handles cases where the user is typing inside parentheses.
        """
        # Find the last word being typed
        import re
        match = re.search(r'\w+$', text)
        return match.group(0) if match else ''

def ide_main():

    def load_variables_to_scope(variable_scope):
        """Load variables, including reconstructing functions from their source code."""
        for k, v in variable_scope.items():
            if isinstance(v, str) and "def " in v:  # Check if it's a function source code
                try:
                    exec(v, globals())  # Recreate the function in the global scope
                    print(f"Reconstructed function: {k}")
                except Exception as e:
                    print(f"Failed to reconstruct function {k}: {e}")
            else:
                globals()[k] = v  # Restore regular variables

        print(f"Loaded variables into the global scope: {globals()}")

    # Check if variables need to be loaded from a file
    # if '--load-variables' in sys.argv:
    serialized_variables_path = 'pop_up_venv/variables.dill'  # Adjust this path as needed
    if os.path.exists(serialized_variables_path):
        with open(serialized_variables_path, 'rb') as f:
            variable_scope = dill.load(f)
        load_variables_to_scope(variable_scope) 
        # globals().update(variable_scope)
        # print(f"Loaded variables into global scope: {list(variable_scope.keys())}")
    else:
        print(f"Serialized variables file not found: {serialized_variables_path}")

    # Re-import modules if necessary
    for module_name, module_obj in variable_scope.get('imported_modules', {}).items():
        globals()[module_name] = module_obj
        print(f"Re-imported module: {module_name}")

    ide_code_lines = []
    ide_empty_line_count = 0
    ide_prompt_session = PromptSession()

    with patch_stdout():
        # clear()
        os.system('clear')
        while True:
            try:
                # Prompt user input
                line = ide_prompt_session.prompt('› ', key_bindings=_PopUpIdeBindings.bindings, completer=_PythonCompleter(), lexer=PygmentsLexer(PythonLexer), style=style_from_pygments_cls(get_style_by_name('autumn')) )

                # Check for an exit command
                if line.strip() == "exit":
                    _PopUpIdeTerminalOperations.exit_virtualenv()
                    break

                # Check for an exit and delete command
                if line.strip() == "exit & delete environment":
                    _PopUpIdeTerminalOperations.exit_and_delete_virtualenv()
                    break
                
                # Check for an terminal clear command
                if line.strip() == "clear":
                    os.system('clear')

                # Track empty lines
                if line.strip() == "":
                    ide_empty_line_count += 1
                else:
                    ide_empty_line_count = 0  # Reset empty line count if it's not empty
                    ide_code_lines.append(line)  # Add line to code_lines

                # Execute code after two consecutive empty lines
                if ide_empty_line_count == 2:
                    code = "\n".join(ide_code_lines).strip()  # Join all lines into a single block

                    # Check if the entire code block is a function call
                    function_name, arguments = _PopUpIdeSystemFunctions.is_function_call(code)  # Check the entire block

                    if function_name:
                        # Verify if the function exists in globals
                        if function_name in globals() and callable(globals()[function_name]):
                            try:
                                # Prepare and evaluate arguments
                                args = [eval(arg.strip()) for arg in arguments.split(',')] if arguments else []
                                # Call the function dynamically
                                # print("»»")
                                print('prints:')
                                result = globals()[function_name](*args)
                                print(f'\nreturns:\n{result}')
                                print("\n")
                            except Exception as e:
                                print(f"Error calling function: {e}")
                    else:
                        try:
                            # Execute the code block if it's not a function call or system call
                            print("»»")
                            # print('prints:')
                            exec(code, globals())
                            print("\n")

                        except Exception as e:
                            print(f"Error executing code: {e}")

                    # Reset code lines and empty line count after execution
                    ide_code_lines = []
                    ide_empty_line_count = 0
                    
            except Exception as e:
                print(f"Error: {e}")
                ide_code_lines = []  # Reset in case of error
                ide_empty_line_count = 0  # Reset empty line count in case of error



