from os import environ
from pathlib import Path
from subprocess import call
from warnings import deprecated

from pybrary import Dico


def create_config_py(path, defaults):
    kv = [(k, f"'{v}'" if isinstance(v, str) else v) for k, v in defaults.items()]
    kv = ',\n    '.join(f'{k} = {v}' for k, v in kv)
    with open(path, 'w') as out:
        out.write(f'config = dict(\n    {kv}\n)\n')

def create_config_toml(path, defaults):
    kv = [(k, f'"{v}"' if isinstance(v, str) else v) for k, v in defaults.items()]
    kv = '\n'.join(f'{k} = {v}' for k, v in kv)
    with open(path, 'w') as out:
        out.write(f'[config]\n{kv}\n')

def create_config_yaml(path, defaults):
    kv = [(k, f"'{v}'" if isinstance(v, str) else v) for k, v in defaults.items()]
    kv = '\n    '.join(f'{k}: {v}' for k, v in kv)
    with open(path, 'w') as out:
        out.write(f'config:\n    {kv}\n')

def create_config_json(path, defaults):
    kv = [(f'"{k}"', f'"{v}"' if isinstance(v, str) else v) for k, v in defaults.items()]
    kv = ',\n    '.join(f'{k}: {v}' for k, v in kv)
    with open(path, 'w') as out:
        out.write(f'{{\n"config":\n    {{\n    {kv}\n    }}\n}}\n')

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
    def __init__(self, app, defaults=None, ext='py'):
        defaults = defaults or dict()
        config = self.find(app) or self.create(app, defaults, ext)
        if config:
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

    def create(self, app, defaults, ext):
        full = self.root / f'{app}.{ext}'
        creators[ext](full, defaults)
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
