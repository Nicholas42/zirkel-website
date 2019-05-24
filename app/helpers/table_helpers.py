class IdentityDict(dict):
    def get(self, key, default=None):
        return key