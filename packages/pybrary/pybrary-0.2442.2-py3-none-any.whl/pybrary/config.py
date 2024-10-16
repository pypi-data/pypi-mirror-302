from os import environ
from pathlib import Path
from subprocess import call
from warnings import deprecated

from pybrary import Dico


def create_config_py(path):
    with open(path, 'w') as out:
        out.write('config = dict(\n)\n')

def create_config_toml(path):
    with open(path, 'w') as out:
        out.write('[config]\n')

def create_config_yaml(path):
    with open(path, 'w') as out:
        out.write('config: {}\n')

def create_config_json(path):
    with open(path, 'w') as out:
        out.write('{"config": {}}\n')

creators = dict(
    py = create_config_py,
    toml = create_config_toml,
    yaml = create_config_yaml,
    json = create_config_json,
)


def load_config_py(path):
    from pybrary.modules import load
    return load('config', path).config

def load_config_toml(path):
    from tomllib import loads
    return loads(path.read_text())['config']

def load_config_yaml(path):
    from yaml import load, SafeLoader
    return load(open(path), Loader=SafeLoader)['config']

def load_config_json(path):
    from json import load
    return load(open(path))['config']

loaders = dict(
    py = load_config_py,
    toml = load_config_toml,
    yaml = load_config_yaml,
    json = load_config_json,
)


class Config(Dico):
    def __init__(self, app, default='py'):
        config = self.find(app) or self.create(app, default)
        for key, val in config.items():
            setattr(self, key, val)

    @property
    def root(self):
        return Path('~/.config').expanduser()

    def find(self, app):
        for ext, loader in loaders.items():
            full = self.root / f'{app}.{ext}'
            if full.is_file():
                config = loader(full)
                self.path = full
                return config

    def create(self, app, ext):
        full = self.root / f'{app}.{ext}'
        creators[ext](full)
        loader = loaders[ext]
        config = loader(full)
        self.path = full
        return config

    def edit(self):
        editor = environ.get('EDITOR', 'vim')
        call([editor, self.path])


@deprecated('Use pybrary.Config instaed')
def get_app_config(app):
    path = Path(f'~/.config/{app}').expanduser()
    try:
        from pybrary.modules import load
        full = path / 'config.py'
        config = load('config', full)
        return full, config.config
    except: pass
    try:
        from tomllib import loads
        full = path / 'config.toml'
        config = loads(full.read_text())
        return full, config
    except: pass
    try:
        from yaml import load, SafeLoader
        full = path / 'config.yaml'
        config = load(full, loader=SafeLoader)
        return full, config
    except: pass
    try:
        from json import load
        full = path / 'config.json'
        config = load(full)
        return full, config
    except: pass
    return None, None
