class PostDocumentResponse:
    def __init__(self, documentCount, category, files, errors, duplicates):
        self.documentCount = documentCount
        self.category = category
        self.files = files
        self.errors = errors
        self.duplicates = duplicates

    @classmethod
    def from_dict(cls, data):
        return cls(data['documentCount'], data['category'], data['files'], data['errors'], data['duplicates'])