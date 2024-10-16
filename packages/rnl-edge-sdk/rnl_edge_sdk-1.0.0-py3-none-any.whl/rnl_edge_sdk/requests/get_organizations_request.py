class GetOrganizationsRequest:
    def __init__(self, data_source_type=None, active=None, name=None):
        self.data_source_type = data_source_type
        self.active = active
        self.name = name

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
