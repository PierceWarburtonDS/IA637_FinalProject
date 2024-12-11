import hashlib
from baseObject import baseObject
class sequencing(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self,n=0):
        self.errors = []


        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []

        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
   