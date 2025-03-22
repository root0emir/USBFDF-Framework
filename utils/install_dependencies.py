import subprocess
import sys
import platform
import importlib.util

def is_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_requirements():
    dependencies = {
        'tsk': 'tsk',  
        'magic': 'python-magic',  
        'hashlib': None,  
        'unittest': None,  
        'requests': 'requests',  
        'pillow': 'Pillow',  
        'argparse': None,  
        'shutil': None,  
        'datetime': None,  
        'csv': None,  
    }

    try:
        for module_name, package_name in dependencies.items():
            if package_name and not is_installed(module_name):
                if platform.system() == 'Linux':
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--break-system-packages', package_name])
                else:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
                print(f"'{package_name}' installed successfully.")
            elif not package_name:
                print(f"'{module_name}' is a standard library module or already installed.")
            else:
                print(f"'{module_name}' is already installed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependency: {package_name}")
        print(e)

if __name__ == "__main__":
    install_requirements()