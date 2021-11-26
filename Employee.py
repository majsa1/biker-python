
class Employee:
    def __init__(self):
        self._id          = ""
        self._firstName   = ""
        self._lastName    = ""
        self._role        = ""
        self._loginName   = ""

    def setId(self, id):
        self._id = id

    def getId(self):
        return self._id

    id = property(getId, setId)

    def setFirstName(self, firstName):
        self._firstName = firstName

    def getFirstName(self):
        return self._firstName

    firstName = property(getFirstName, setFirstName)

    def setLastName(self, lastName):
        self._lastName = lastName
        
    def getLastName(self):
        return self._lastName
    
    lastName = property(getLastName, setLastName)

    def setRole(self, role):
        self._role = role

    def getRole(self):
        return self._role

    role = property(getRole, setRole)

    def setLoginName(self, loginName):
        self._loginName = loginName
     
    def getLoginName(self):
        return self._loginName
    
    loginName = property(getLoginName, setLoginName)


