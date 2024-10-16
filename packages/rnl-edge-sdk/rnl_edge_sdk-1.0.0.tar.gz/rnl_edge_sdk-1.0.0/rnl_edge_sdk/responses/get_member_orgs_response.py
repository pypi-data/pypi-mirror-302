class GetMemberOrgsResponse:
    def __init__(self, email, memberOrgs):
        self.email = email
        self.memberOrgs = memberOrgs

    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data.get('email', ''),
            memberOrgs=data.get('memberOrgs', [])
        )