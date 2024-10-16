class Product:
    def __init__(self, name, description, host_names=None):
        self.name = name
        self.description = description
        self.host_names = host_names or {}