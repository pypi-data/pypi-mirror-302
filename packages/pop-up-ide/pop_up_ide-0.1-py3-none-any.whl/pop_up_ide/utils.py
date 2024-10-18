import dill
import os

class _PopUpIdeUtils:
    @staticmethod
    def save_variables_to_env(variables):
        """Save updated variables back to the virtual environment."""
        env_name='pop_up_venv'
        file_path = f"{env_name}/variables.dill"
        with open(file_path, 'wb') as f:
            dill.dump(variables, f, recurse=True)
        print(f"Variables updated in {file_path}")

    @staticmethod
    def load_variables_from_env():
        """Load variables serialized in the virtual environment using `dill`."""
        env_name='pop_up_venv'
        file_path = f"{env_name}/variables.dill"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                variables = dill.load(f)
            print(f"Loaded variables from {file_path}")
            return variables
        else:
            print(f"No variable file found at {file_path}. Starting with an empty set.")
            return {}
