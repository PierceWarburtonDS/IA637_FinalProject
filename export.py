import hashlib
from baseObject import baseObject
import yaml
from pathlib import Path

class export(baseObject):
    def __init__(self):
        config = yaml.safe_load(Path("config.yml").read_text())
        self.config = config
        self.table_statement = 'FROM warburpd_samples s, warburpd_sequencing seq, warburpd_species sp, \
                warburpd_phylum p, warburpd_genus g, warburpd_users u, warburpd_detections d \
                WHERE d.SampleID=s.SampleID \
                AND d.SeqID = seq.SeqID \
                AND d.SpeciesID=sp.speciesID \
                AND d.GenusID = g.genusID \
                AND d.PhylumID=p.phylumID \
                AND d.DetectionAnalyst=u.uid'
        self.establishConnection()
        self.getFields()
    def getFields(self):
        self.fields = ['SampleName', 'Technique', 'DetectionMethod', 'Phylum', 'Genus', \
                'Species', 'DateSampled', 'DateSeq','DateDetected']
    def getAll(self):
        sql = f"SELECT {",".join(x for x in self.fields)} {self.table_statement}"
        self.cur.execute(sql)
        self.data = []
        for row in self.cur:
            self.data.append(row)

    def getCol(self,col):
        sql = f"Select DISTINCT {col} {self.table_statement}" 
        #print(sql,flush=True)
        self.cur.execute(sql)
        self.colvalues = []
        for row in self.cur:
            self.colvalues.append(row[col])
        print(self.colvalues, flush=True)

    def getByField(self, col, val):
        sql = f"Select {",".join(x for x in self.fields)} {self.table_statement} AND `{col}` = %s" 
        #print(sql,flush=True)
        self.cur.execute(sql,(val))
        self.data = []
        for row in self.cur:
            self.data.append(row)

    def verify_new(self,n=0):
        self.errors = []
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
    def verify_update(self,n=0):
        self.errors=[]
        ##Include this in verify:
        if len(self.errors) > 0:
            return False
        else:
            return True
   