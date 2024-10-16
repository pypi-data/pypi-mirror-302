class GetOrganizationsResponse:
    def __init__(self, record_count, results):
        self.record_count = record_count
        self.results = results

    @classmethod
    def from_dict(cls, data):
        return cls(data['recordCount'], data['results'])
