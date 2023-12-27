import os
from pathlib import Path
from sys import platform

# Check OS platform and assign the pyButler directory accordingly
def app():
    if platform == 'linux': # Linux
        app_dir = Path.home() / '.config' / 'pyButler'

    elif platform == 'darwin': # macOS
        app_dir = Path.home() / 'Library' / 'Application Support' / 'pyButler'

    elif platform == 'win32': # Windows
        app_dir = Path(os.getenv('APPDATA')) / 'pyButler'

    if os.path.exists(app_dir):
        return app_dir
    else:
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir


# return the path of config.json
def config_file():
    app_dir = app()
    config_path = app_dir / 'config.json'
    return config_path

# return the path of .env file (used for api key)
def auth_file():
    app_dir = app()
    auth_path = app_dir / '.env'
    return auth_path


# ! Not yet implimented...create user set directories automatically, trigged by toggle.
def setup_dirs(configs):
    dir_names = ['source', 'movie', 'show', 'audiobook']
    
    for dir_name in dir_names:
        dir_path = configs[dir_name]
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            exist_msg = f"Directory exists! {dir_path}"
            print(f"{exist_msg}")
        else:
            print(f"Directory created → {dir_path}")