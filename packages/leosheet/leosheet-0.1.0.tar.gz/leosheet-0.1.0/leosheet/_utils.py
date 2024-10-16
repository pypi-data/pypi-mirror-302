import toml
from pathlib import Path


PATH =Path('./.secrets.toml')  

# Load the TOML file
with open(PATH, 'r') as f:
    secrets = toml.load(f)