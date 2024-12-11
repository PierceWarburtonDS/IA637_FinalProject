-- Create the Tables

CREATE TABLE `warburpd_users` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
   PRIMARY KEY (uid)
);
CREATE TABLE `warburpd_samples` (
  `SampleID` int NOT NULL AUTO_INCREMENT,
  `SampleName` varchar(50)NOT NULL,
  `DateSampled` varchar(50) DEFAULT NULL,
  `Location` varchar(50) DEFAULT NULL,
  `Collector_uid` int NOT NULL,
   PRIMARY KEY (SampleID),
   FOREIGN KEY (Collector_uid) REFERENCES warburpd_users(uid)
);
CREATE TABLE `warburpd_sequencing` (
  `SeqID` int NOT NULL AUTO_INCREMENT,
  `Technique` varchar(50) NOT NULL,
  `DateSeq` varchar(50) NOT NULL,
  `LabTech` int NOT NULL,
   PRIMARY KEY (SeqID),
   FOREIGN KEY (LabTech) REFERENCES warburpd_users(uid)
);
CREATE TABLE `warburpd_species` (
  `speciesID` int NOT NULL AUTO_INCREMENT,
  `Species` varchar(100) NOT NULL,
   PRIMARY KEY (speciesID)
);
CREATE TABLE `warburpd_genus` (
  `genusID` int NOT NULL AUTO_INCREMENT,
  `Genus` varchar(100) NOT NULL,
   PRIMARY KEY (genusID)
);
CREATE TABLE `warburpd_phylum` (
  `phylumID` int NOT NULL AUTO_INCREMENT,
  `Phylum` varchar(100) NOT NULL,
   PRIMARY KEY (phylumID)
);
CREATE TABLE `warburpd_detections` (
  `DetectionID` int NOT NULL AUTO_INCREMENT,
  `SampleID` int NOT NULL,
  `SeqID` int NOT NULL,
  `SpeciesID` int NOT NULL,
  `GenusID` int NOT NULL,
  `PhylumID` int NOT NULL,
  `DateDetected` DATE DEFAULT NULL,
  `DetectionMethod` varchar(100) NOT NULL,
  `DetectionAnalyst` int NOT NULL,
   PRIMARY KEY (DetectionID),
   FOREIGN KEY (SampleID) REFERENCES warburpd_samples(SampleID),
   FOREIGN KEY (SeqID) REFERENCES warburpd_sequencing(SeqID),
   FOREIGN KEY (SpeciesID) REFERENCES warburpd_species(speciesID),
   FOREIGN KEY (GenusID) REFERENCES warburpd_genus(genusID),
   FOREIGN KEY (PhylumID) REFERENCES warburpd_phylum(phylumID),
   FOREIGN KEY (DetectionAnalyst) REFERENCES warburpd_users(uid)
);

-- Insert the data
INSERT INTO `warburpd_users` (`user_name`, `password`, `role`) VALUES
('warburpd', '123', 'admin'),
('LabTech1', '12345', 'LabTech'),
('LabTech2', '12345', 'LabTech'),
('Analyst1', '12345', 'Analyst'),
('Analyst2', '12345', 'Analyst');
INSERT INTO `warburpd_samples` (`SampleName`, `DateSampled`, `Location`, `Collector_uid`) VALUES
('BlackLake_EastBank', '2024', 'BL', 2),
('BlackLake_WestBank', '2024', 'BL', 2),
('GovernersIsland', '2022', 'StLaw', 1),
('UpperRiver', '2023', 'StLaw', 3),
('LowerRiver', '2023', 'StLaw', 3),
('Bay', '2022', 'StLaw', 3);
INSERT INTO `warburpd_sequencing` (`Technique`, `DateSeq`, `labTech`) VALUES
('16S', '2022', '2'),
('metagenomic', '2022', '2'),
('16S', '2023', '3'),
('metagenomic', '2023', '3'),
('16S', '2024', '2'),
('metagenomic', '2024', '3');
INSERT INTO `warburpd_species` (`Species`) VALUES
('arctic cyanobacterium 65RS1'),
('heterocystous cyanobacterium C1C5'),
('Cyanobacteria bacterium UBA947 '),
('Petrachlorosaceae '),
('Thalassoporaceae'),
('Lusitaniellaceae');
INSERT INTO `warburpd_genus` (`Genus`) VALUES
('Chroococcidiopsidales'),
('Desertifilales'),
('Gomontiellales ');
INSERT INTO `warburpd_phylum` (`Phylum`) VALUES
('Cyanophyceae'),
('Armatimonadota ');
INSERT INTO `warburpd_detections` (`SampleID`,`SeqID`,`SpeciesID`,`GenusID`,`PhylumID`,`DateDetected`,`DetectionMethod`,`DetectionAnalyst`) VALUES
('5','3','1','1','1','12/11/24','Dorado','5'),
('5','3','2','1','1','12/11/24','Dorado','5'),
('5','3','3','2','2','12/11/24','Dorado','5'),
('5','4','1','2','1','12/10/24','metagenomic','4'),
('5','4','4','3','1','12/10/24','metagenomic','4'),
('1','5','5','3','1','12/11/24','Dorado','5'),
('1','5','1','1','1','12/11/24','Dorado','5'),
('2','6','2','2','1','12/11/24','metagenomic','5'),
('2','6','1','1','1','12/11/24','metagenomic','4'),
('3','1','2','2','2','12/11/24','Dorado','5'),
('3','1','5','3','2','12/11/24','Dorado','4'),
('3','1','4','1','2','12/11/24','Dorado','5'),
('4','3','1','1','2','12/9/24','Dorado','4'),
('4','4','2','3','1','12/9/24','metagenomic','5'),
('4','4','3','3','1','12/9/24','metagenomic','4'),
('4','4','4','2','1','12/9/24','metagenomic','4'),
('4','4','5','1','1','12/9/24','metagenomic','4'),
('6','1','2','1','2','12/1/24','Dorado','5'),
('6','1','3','3','2','12/1/24','Dorado','5'),
('6','1','1','3','1','12/1/24','Dorado','4');