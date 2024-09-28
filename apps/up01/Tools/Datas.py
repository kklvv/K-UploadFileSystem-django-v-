
class Mine:



    def __init__(self, myData):
        self._baseName = myData.get('baseName')
        self._rootName = myData.get('rootName')
        self._password = myData.get('password')

    @property
    def baseName(self):
        return self._baseName

    @property
    def rootName(self):
        return self._rootName

    @property
    def password(self):
        return self._password

    def __str__(self):
        return f" {self.baseName} {self.rootName} {self.password} "


