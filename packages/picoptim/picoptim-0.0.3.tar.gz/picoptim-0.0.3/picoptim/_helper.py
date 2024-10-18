# This part is the magic which makes FunEvals.load method able to load subclass
# A protected dictionnary subclass is created to prevent careless messing up
# of the loader info (e.g. avoid overwriting an existing loading method)
class SettingOnProtected(Exception):
    """Exception when trying to reset an existing key in a ProtectedDict"""


class ProtectedDict(dict):
    """Protected Dictionnary: overwriting existing key is not allowed"""

    def __setitem__(self, key, value):
        if key in self.keys():
            raise SettingOnProtected(
                f"ProtectedDict: Key {key} already exists (value: {self.__getitem__(key)})"
            )
        super().__setitem__(key, value)
