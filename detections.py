import hashlib
from baseObject import baseObject
from taxonomy import *

class detections(baseObject):
    def __init__(self):
        self.setup()
    def verify_new(self,n=0):
        self.errors = []

        if self.data[n]['DetectionMethod'] == '':
            self.errors.append('Detection Method cannot be blank.')
        # Verify the taxonomical stuff and change to foreign keys if new species
        # Species Validation
        if not self.data[n]['SpeciesID'].isnumeric():
            s = species()
            new_data = {}
            new_data['Species'] = self.data[n]['SpeciesID']
            # Check if species is already in table
            s.getByField('Species',self.data[n]['SpeciesID'])
            if len(s.data) > 0:
                self.data[n]['SpeciesID'] = s.data[0]['speciesID']
            else:
                s.set(new_data)
                s.insert()
                self.data[n]['SpeciesID'] = s.cur.lastrowid
        # Genus Validation
        if not self.data[n]['GenusID'].isnumeric():
            g = genus()
            new_data = {}
            new_data['Genus'] = self.data[n]['GenusID']
            # Check if species is already in table
            g.getByField('Genus',self.data[n]['GenusID'])
            if len(g.data) > 0:
                self.data[n]['GenusID'] = g.data[0]['genusID']
            else:
                g.set(new_data)
                g.insert()
                self.data[n]['GenusID'] = g.cur.lastrowid
            # Phylum Validation
        if not self.data[n]['PhylumID'].isnumeric():
            p = phylum()
            new_data = {}
            new_data['Phylum'] = self.data[n]['PhylumID']
            p.set(new_data)
            # Check if species is already in table
            p.getByField('Phylum',self.data[n]['PhylumID'])
            if len(p.data) > 0:
                self.data[n]['PhylumID'] = p.data[0]['phylumsID']
            else:
                p.set(new_data)
                p.insert()
                self.data[n]['PhylumID'] = p.cur.lastrowid


        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors = []
        if self.data[n]['DetectionMethod'] == '':
            self.errors.append('Detection Method cannot be blank.')
        # Verify the taxonomical stuff and change to foreign keys if new species
        # Species Validation
        if not self.data[n]['SpeciesID'].isnumeric():
            s = species()
            new_data = {}
            new_data['Species'] = self.data[n]['SpeciesID']
            # Check if species is already in table
            s.getByField('Species',self.data[n]['SpeciesID'])
            if len(s.data) > 0:
                self.data[n]['SpeciesID'] = s.data[0]['speciesID']
            else:
                s.set(new_data)
                s.insert()
                self.data[n]['SpeciesID'] = s.cur.lastrowid
        # Genus Validation
        if not self.data[n]['GenusID'].isnumeric():
            g = genus()
            new_data = {}
            new_data['Genus'] = self.data[n]['GenusID']
            # Check if species is already in table
            g.getByField('Genus',self.data[n]['GenusID'])
            if len(g.data) > 0:
                self.data[n]['GenusID'] = g.data[0]['genusID']
            else:
                g.set(new_data)
                g.insert()
                self.data[n]['GenusID'] = g.cur.lastrowid
            # Phylum Validation
        if not self.data[n]['PhylumID'].isnumeric():
            p = phylum()
            new_data = {}
            new_data['Phylum'] = self.data[n]['PhylumID']
            p.set(new_data)
            # Check if species is already in table
            p.getByField('Phylum',self.data[n]['PhylumID'])
            if len(p.data) > 0:
                self.data[n]['PhylumID'] = p.data[0]['phylumsID']
            else:
                p.set(new_data)
                p.insert()
                self.data[n]['PhylumID'] = p.cur.lastrowid
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
   