
CREATE TABLE `Wafers` (
  `idWafers` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  `Masks` varchar(64) DEFAULT NULL,	  
  `Comments` varchar(128),
  PRIMARY KEY (`idWafers`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  UNIQUE KEY `idWafers_UNIQUE` (`idWafers`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Devices` (
  `idDevices` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  `Wafer_id` int(11),
  `Comments` varchar(128),
  PRIMARY KEY (`idDevices`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  UNIQUE KEY `idDevices_UNIQUE` (`idDevices`),
  KEY `fk_Devices_1_idx` (`Wafer_id`),
  CONSTRAINT `fk_Devices_1` FOREIGN KEY (`Wafer_id`) REFERENCES `Wafers` (`idWafers`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `TrtTypes` (
  `idTrtTypes` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL, 	
  `Length` double DEFAULT NULL,
  `Width` double DEFAULT NULL,
  `Pass` double DEFAULT NULL,
  `Contact` varchar(64) DEFAULT NULL,
  `Shape` varchar(64) DEFAULT NULL,
  `Comments` varchar(128),
  PRIMARY KEY (`idTrtTypes`),
  UNIQUE KEY `idTrtTypes_UNIQUE` (`idTrtTypes`),
  UNIQUE KEY `Name_UNIQUE` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Trts` (
  `idTrts` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  `Type_id` int(11) DEFAULT NULL,
  `Device_id` int(11) DEFAULT NULL,
  `DCMeas` int(11) DEFAULT NULL,
  `ACMeas` int(11) DEFAULT NULL,
  `Comments` varchar(128),
  PRIMARY KEY (`idTrts`),
  UNIQUE KEY `idTrts_UNIQUE` (`idTrts`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  KEY `fk_Trts_1_idx` (`Type_id`),
  KEY `fk_Trts_2_idx` (`Device_id`),
  CONSTRAINT `fk_Trts_1` FOREIGN KEY (`Type_id`) REFERENCES `TrtTypes` (`idTrtTypes`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_Trts_2` FOREIGN KEY (`Device_id`) REFERENCES `Devices` (`idDevices`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Users` (
  `idUsers` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  UNIQUE KEY `idUsers_UNIQUE` (`idUsers`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `Gcharacts` (
  `idGcharacts` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(64) NOT NULL,
  `User_id` int(11) DEFAULT NULL,
  `Data` mediumblob NOT NULL,
  `UpdateDate` datetime DEFAULT NULL,
  `MeasDate` datetime DEFAULT NULL,
  `FileName` varchar(64) DEFAULT NULL,
  `Comments` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idGcharacts`),
  UNIQUE KEY `idDCcharacts_UNIQUE` (`idGcharacts`),  
  KEY `fk_Gcharacts_1_idx` (`User_id`),
  CONSTRAINT `fk_Gcharacts_1` FOREIGN KEY (`User_id`) REFERENCES `Users` (`idUsers`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `DCcharacts` (
  `idDCcharacts` int(11) NOT NULL AUTO_INCREMENT,
  `User_id` int(11) DEFAULT NULL,
  `Trt_id` int(11) DEFAULT NULL,  
  `Data` mediumblob NOT NULL,
  `Gate_id` int(11) DEFAULT NULL,  
  `IsOK` int(2) DEFAULT NULL,
  `UpdateDate` datetime DEFAULT NULL,
  `MeasDate` datetime DEFAULT NULL,
  `Solution` varchar(32) DEFAULT NULL,
  `Ph` long DEFAULT NULL,
  `FileName` varchar(64) DEFAULT NULL,
  `Comments` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idDCcharacts`),
  UNIQUE KEY `idDCcharacts_UNIQUE` (`idDCcharacts`),
  KEY `fk_DCcharact_1_idx` (`Trt_id`),
  KEY `fk_DCcharact_2_idx` (`User_id`),
  KEY `fk_DCcharact_3_idx` (`Gate_id`),
  CONSTRAINT `fk_DCcharact_1` FOREIGN KEY (`Trt_id`) REFERENCES `Trts` (`idTrts`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_DCcharact_2` FOREIGN KEY (`User_id`) REFERENCES `Users` (`idUsers`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_DCcharact_3` FOREIGN KEY (`Gate_id`) REFERENCES `Gcharacts` (`idGcharacts`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `ACcharacts_new` (
  `idACcharacts` int(11) NOT NULL AUTO_INCREMENT,
  `User_id` int(11) DEFAULT NULL,
  `Trt_id` int(11) DEFAULT NULL,
  `DC_id` int(11) DEFAULT NULL,
  `Data` longblob NOT NULL,
  `IsOK` int(2) DEFAULT NULL,
  `IsCmp` int(2) DEFAULT NULL,
  `UpdateDate` datetime DEFAULT NULL,
  `MeasDate` datetime DEFAULT NULL,
  `Ph` double DEFAULT NULL,
  `Solution` varchar(32) DEFAULT NULL,
  `IonStrength` double DEFAULT NULL,
  `FuncStep` varchar(45) DEFAULT NULL,
  `AnalyteCon` double DEFAULT NULL,
  `Comments` varchar(32) DEFAULT NULL,
  `FileName` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`idACcharacts`),
  UNIQUE KEY `idACcharacts_UNIQUE` (`idACcharacts`),
  KEY `fk_ACcharact_1_idx` (`Trt_id`),
  KEY `fk_ACcharact_2_idx` (`User_id`),
  KEY `fk_ACcharact_3_idx` (`DC_id`),
  CONSTRAINT `fk_ACcharact_1` FOREIGN KEY (`Trt_id`) REFERENCES `Trts` (`idTrts`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ACcharact_2` FOREIGN KEY (`User_id`) REFERENCES `Users` (`idUsers`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ACcharact_3` FOREIGN KEY (`DC_id`) REFERENCES `DCcharacts` (`idDCcharacts`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4;


CREATE TABLE `ACcharacts` (
  `idACcharacts` int(11) NOT NULL AUTO_INCREMENT,
  `User_id` int(11) DEFAULT NULL,
  `Trt_id` int(11) DEFAULT NULL,
  `DC_id` int(11) DEFAULT NULL,
  `Data` longblob NOT NULL,
  `IsOK` int(2) DEFAULT NULL,
  `UpdateDate` datetime DEFAULT NULL,
  `MeasDate` datetime DEFAULT NULL,
  `Solution` varchar(32) DEFAULT NULL,
  `Ph` long DEFAULT NULL,
  `FileName` varchar(64) DEFAULT NULL,
  `Comments` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`idACcharacts`),
  UNIQUE KEY `idACcharacts_UNIQUE` (`idACcharacts`),
  KEY `fk_ACcharact_1_idx` (`Trt_id`),
  KEY `fk_ACcharact_2_idx` (`User_id`),
  KEY `fk_ACcharact_3_idx` (`DC_id`),
  CONSTRAINT `fk_ACcharact_1` FOREIGN KEY (`Trt_id`) REFERENCES `Trts` (`idTrts`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ACcharact_2` FOREIGN KEY (`User_id`) REFERENCES `Users` (`idUsers`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_ACcharact_3` FOREIGN KEY (`DC_id`) REFERENCES `DCcharacts` (`idDCcharacts`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `MeasCond` (
  `idMeasCond` int(11) NOT NULL AUTO_INCREMENT,
  `Blocker_id` int(11) DEFAULT NULL,
  `Linker_id` int(11) DEFAULT NULL,
  `Comments` varchar(45) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idMeasCond`),
  UNIQUE KEY `idMeasCond_UNIQUE` (`idMeasCond`),
  CONSTRAINT `fk_MeasCond_1` FOREIGN KEY (`Blocker_id`) REFERENCES `BlockerType` (`idBlockerType`)  ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_MeasCond_2` FOREIGN KEY (`linker_id`) REFERENCES `LinkerType` (`idLinkerType`)  ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


