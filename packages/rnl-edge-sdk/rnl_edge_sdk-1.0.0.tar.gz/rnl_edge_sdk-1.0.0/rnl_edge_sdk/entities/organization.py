class Organization:
    def __init__(self, name, active, data_sources=None, products=None):
        self.name = name
        self.active = active
        self.data_sources = data_sources or []
        self.products = products or []