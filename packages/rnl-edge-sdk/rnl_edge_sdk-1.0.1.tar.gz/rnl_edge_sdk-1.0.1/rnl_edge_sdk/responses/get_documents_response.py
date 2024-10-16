class GetDocumentsResponse:
    def __init__(self, record_count, files):
        self.record_count = record_count
        self.files = files

    @classmethod
    def from_dict(cls, data):
        return cls(
            record_count=data.get('recordCount', 0),
            files=data.get('files', [])
        )