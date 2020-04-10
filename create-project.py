import argparse
import sys
import os
import virtualenv
import pip
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('project_name', type=str)
parser.add_argument('--template', '-t')
args = parser.parse_args()

cwd = os.getcwd()


templates = {
    'django-postgres': ['django', 'psycopg2'],
    'django-mysql': ['django', 'mysqlclient'],
    'django': ['django'],
    'kivy': ['kivy'],
    'scientific': ['pandas', 'matplotlib'],
    'basic-ia': ['scikit-learn', 'pandas'],
}


def create_dir(dir_name):
    print(f'Creating project "{dir_name}"')
    project_dir = os.path.join(os.getcwd(), dir_name)
    os.mkdir(project_dir)
    return project_dir


def create_venv(base_dir):
    print("Creating virtualenv...")
    venv_dir = os.path.join(base_dir, 'venv')
    virtualenv.cli_run([venv_dir, '--prompt', '(venv) '])
    print("Done!")
    return venv_dir


def upgrade_pip(venv_dir):
    python_venv_path = os.path.join(venv_dir, "Scripts\\python")
    print("Upgrading pip...")
    subprocess.run([
        python_venv_path, '-m', 'pip', 'install', '--upgrade', 'pip'
    ])


def install_packages(venv_dir, packages):
    python_venv_path = os.path.join(venv_dir, "Scripts\\python")

    print("Installing packages...")
    subprocess.run([
        python_venv_path, '-m', 'pip', 'install', *packages
    ])


base_dir = create_dir(args.project_name)
venv_dir = create_venv(base_dir)
upgrade_pip(venv_dir)

if args.template:
    template = templates.get(args.template)
    if template is not None:
        install_packages(venv_dir, template)
    else:
        raise ValueError("Unknown template")

print("Done!")
