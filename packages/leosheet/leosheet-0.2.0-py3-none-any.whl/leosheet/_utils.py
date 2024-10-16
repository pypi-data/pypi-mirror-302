import toml
from pathlib import Path

class SecretHolder:
    def __init__(self):
        self.secrets = None
        self.load_secrets_from_file()
    
    def load_secrets_from_file(self):
        try:
            PATH =Path('./.secrets.toml')  

            # Load the TOML file
            with open(PATH, 'r') as f:
                self.secrets = toml.load(f)
        except:
            pass
    
    def set_secrets(self,toml_msg):
        self.secrets = toml.loads(toml_msg)


secret_holder = SecretHolder()