class PostDocumentRequest:
    def __init__(self, files, visibilityRules=None, category=None):
        self.files = files
        self.visibilityRules = visibilityRules or []
        self.category = category

    def to_dict(self):
        return {
            "files": self.files,
            "visibilityRules": self.visibilityRules,
            "category": self.category
        }
