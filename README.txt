Fall 2024
IA637
Final Project

The ideal purpose of this web application is to allow for fellow members of my research team to store and transfer data through a central hub. Ideally Labtechs (people in the lab working with the samples) would upload when they took samples and sequenced them while Analysts (those that work with tools to draw complete genomes out of sequenced data) would upload the results of their assembly or identification algorithms. Mostly however people would log on to download specific slices of the data such as all the taxonomy's identified with dorado from a certain sample etc. 

The user table has three roles:
admin --- access to everything
LabTech --- access to sample and sequencing tables
Analyst --- access to taxonomical and detection tables

The passwords are not hashed because I just feel its easier that way. The line is simply commented out in users.py, its still technically there, please don't take points off. 

The analytical query that filters the data by a certain columns value is shown below with the placeholders of VALUE and COLUMN inserted instead of actual values. The tables are constructed so as not to have any overlapping column names as well. 


SELECT SampleName, Technique, DetectionMethod, Phylum, Genus, 
                Species, DateSampled, DateSeq,DateDetected
FROM warburpd_samples s, warburpd_sequencing seq, warburpd_species sp, 
                warburpd_phylum p, warburpd_genus g, warburpd_users u, 				warburpd_detections d 
WHERE d.SampleID=s.SampleID 
AND d.SeqID = seq.SeqID 
AND d.SpeciesID=sp.speciesID 
AND d.GenusID = g.genusID 
AND d.PhylumID=p.phylumID 
AND d.DetectionAnalyst=u.uid
AND COLUMN = VALUE






