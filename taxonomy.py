import hashlib
from baseObject import baseObject
class species(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['Species'] == '':
            self.errors.append('Species name cannot be blank.')
        else:
            s = species()
            s.getByField('Species',self.data[n]['Spcies'])
            if len(s.data) > 0:
                self.errors.append('Species already in database.')

        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['Species'] == '':
            self.errors.append('Species name cannot be blank.')
        else:
            s = species()
            s.getByField('Species',self.data[n]['Spcies'])
            if len(s.data) > 0:
                self.errors.append('Species already in database.')
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True

class genus(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['Genus'] == '':
            self.errors.append('Genus name cannot be blank.')
        else:
            s = genus()
            s.getByField('Genus',self.data[n]['Genus'])
            if len(s.data) > 0:
                self.errors.append('Genus already in database.')
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['Genus'] == '':
            self.errors.append('Genus name cannot be blank.')
        else:
            s = genus()
            s.getByField('Genus',self.data[n]['Genus'])
            if len(s.data) > 0:
                self.errors.append('Genus already in database.')

        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
        
class phylum(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self,n=0):
        self.errors = []
        if self.data[n]['Phylum'] == '':
            self.errors.append('Phylum name cannot be blank.')
        else:
            s = phylum()
            s.getByField('Phylum',self.data[n]['Phylum'])
            if len(s.data) > 0:
                self.errors.append('Phylum already in database.')
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['Phylum'] == '':
            self.errors.append('Phylum name cannot be blank.')
        else:
            s = phylum()
            s.getByField('Phylum',self.data[n]['Phylum'])
            if len(s.data) > 0:
                self.errors.append('Phylum already in database.')
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True