class DeleteMultipleDocumentsRequest:
    def __init__(self, query, category, docIds):
        self.query = query
        self.category = category or []
        self.docIds = docIds or []

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}