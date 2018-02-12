DELETE FROM Trts WHERE Trts.Type_id IS NULL;
DELETE FROM ACcharacts WHERE ACcharacts.Trt_id IS NULL;
DELETE FROM DCcharacts WHERE DCcharacts.Trt_id IS NULL;

SELECT Devices.Name, Trts.Name, Trts.DCMeas 
	FROM Trts INNER JOIN Devices ON Devices.idDevices=Trts.Device_id 
    WHERE Devices.Name='OBL3-T18';

SELECT Devices.idDevices, Devices.Name
	FROM Devices 
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    WHERE Wafers.Masks='Cortical16';

SELECT TrtsDCcharacts.Name, Trts.idTrts, TrtTypes.Name, TrtTypes.idTrtTypes
	FROM Trts 
    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    INNER JOIN DCcharacts ON Trts.idTrts = DCcharacts.Trt_id
    INNER JOIN ACcharacts ON Trts.idTrts = ACcharacts.Trt_id
    WHERE TrtTypes.Length = 5e-6
    ORDER BY DCcharacts.MeasDate;


SELECT VTrts.DCMeas, Trts.Name, Trts.idTrts, TrtTypes.Name, TrtTypes.idTrtTypes, TrtTypes.Contact, TrtTypes.Width, TrtTypes.Length
	FROM VTrts, Trts
    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    WHERE VTrts.idTrts = Trts.idTrts and Trts.idTrts > 0;

SELECT Trts.Name, Trts.idTrts, TrtTypes.Name, TrtTypes.idTrtTypes, TrtTypes.Contact, TrtTypes.Width, TrtTypes.Length
	FROM Trts 
    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    WHERE Devices.Name = 'B9355W16-T13' and (Trts.Name != 'B9355W16-T13-Ch07' or Trts.Name != 'B9355W16-T13-Ch04');


SELECT Trts.Name, Wafers.Name, Devices.Name, TrtTypes.Name
	FROM Devices 
    INNER JOIN Trts ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    WHERE (Wafers.Name = 'B9355O25' OR Wafers.Name = 'B9355O26') AND (TrtTypes.Name='RW40L40P1p5CC5' OR TrtTypes.Name='RW40L20P1p5CC5');


SELECT * FROM ACcharacts WHERE ACcharacts.DC_id IS NULL;
DELETE FROM ACcharacts WHERE ACcharacts.DC_id IS NULL;

SELECT * FROM DCcharacts WHERE DCcharacts.Trt_id IS NULL;
DELETE FROM DCcharacts WHERE DCcharacts.Trt_id IS NULL;


UPDATE ACcharacts SET ACcharacts.IsCmp=0 WHERE ACcharacts.idACcharacts>0;

SELECT * FROM ACcharacts WHERE ACcharacts.Trt_id = 1189;

SELECT * FROM DCcharacts WHERE DCcharacts.UpdateDate >'2017-05-18 14:00:00';


SELECT * FROM Devices WHERE Devices.Wafer_id IS NULL;
DELETE FROM Devices WHERE Devices.Wafer_id IS NULL;

SELECT * FROM Trts WHERE Trts.Device_id IS NULL;
DELETE FROM Trts WHERE Trts.Device_id IS NULL;


UPDATE Devices SET Devices.Name = REPLACE(Devices.Name, 'B9872O24', 'B9872W24') WHERE Devices.Name like 'B9872O24%';
SELECT * FROM Devices WHERE Devices.Name like 'Dummy01%';

UPDATE Trts SET Trts.Name = REPLACE(Trts.Name, 'C:\Users\user\Documents\Python\Data20Ch\B10179W13-B2', 'B10179W13-B2') WHERE Trts.Name like 'C:\Users\user\Documents\Python\Data20Ch\%';
SELECT * FROM Trts WHERE Trts.Name like 'Dummy01%';


SELECT * FROM Trts WHERE Trts.Name like 'B10179W13-T%';
UPDATE Trts SET Trts.Type_id = 45 WHERE Trts.Name like 'B9872O24-T%';

SELECT * FROM Trts WHERE Trts.Name like 'B10179W13-B%';
UPDATE Trts SET Trts.Type_id = 50 WHERE Trts.Name like 'B10082W22-B%';

SELECT Trts.Type_id, Trts.Name, Trts.Device_id
	FROM Trts 
	INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    WHERE Wafers.Masks='Biosensv1';

UPDATE Trts SET Trts.Type_id = 109 WHERE Trts.Device_id = 278;

UPDATE Trts  
	INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    SET Trts.Type_id = 109
    WHERE Wafers.Masks='Biosensv1';


SELECT Trts.idTrts, Trts.Name,
	(SELECT count(*) from DCcharacts where Trts.idTrts=DCcharacts.Trt_id) 
    from Trts,DCcharacts where Trts.idTrts=DCcharacts.Trt_id;

SELECT Wafers.idWafers,Wafers.Comments,Devices.Comments,VTrts.DCMeas,VTrts.ACMeas,TrtTypes.Width,Trts.Name,TrtTypes.Area,TrtTypes.Contact,Trts.idTrts,Devices.idDevices,TrtTypes.Length,Trts.Comments,TrtTypes.Name,TrtTypes.Pass,Devices.Name,TrtTypes.Name,Wafers.Name,Wafers.Substrate,Wafers.Masks
                    FROM VTrts, Trts
                    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
                    INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id
                    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
                    WHERE VTrts.idTrts = Trts.idTrts and  (Trts.idTrts> 0); 


UPDATE DCcharacts SET DCcharacts.AnalyteCon=200e-9
	WHERE DCcharacts.FuncStep = '200nM Tromb';

SELECT DCcharacts.AnalyteCon,DCcharacts.FuncStep FROM DCcharacts WHERE DCcharacts.FuncStep = '200nM Tromb';


UPDATE DCcharacts SET DCcharacts.FuncStep=DCcharacts.Comments 
	FROM Trts
    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    INNER JOIN DCcharacts ON Trts.idTrts = DCcharacts.Trt_id
	WHERE Devices.Name='B10803W17-Xip2N';

UPDATE DCcharacts SET DCcharacts.FuncStep = DCcharacts.Comments;

SELECT DCcharacts.FuncStep,  DCcharacts.Comments 
	FROM Trts 
    INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id		  	
    INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
    INNER JOIN DCcharacts ON Trts.idTrts = DCcharacts.Trt_id 
	WHERE Devices.Name='B10803W17-Xip2N';
    
UPDATE DCcharacts SET DCcharacts.FuncStep = DCcharacts.Comments WHERE DCcharacts.FuncStep is null;

UPDATE ACcharacts SET ACcharacts.IsCmp=0 WHERE ACcharacts.idACcharacts>0;


SELECT DCcharacts.idDCcharacts, DCcharacts.FuncStep, DCcharacts.AnalyteCon, Trts.Name, DCcharacts.IsCmp
	FROM DCcharacts
	INNER JOIN Trts ON Trts.idTrts = DCcharacts.Trt_id
	INNER JOIN TrtTypes ON TrtTypes.idTrtTypes = Trts.Type_id
	INNER JOIN Devices ON Devices.idDevices = Trts.Device_id
	INNER JOIN Wafers ON Wafers.idWafers = Devices.Wafer_id
	INNER JOIN VTrts ON VTrts.idTrts = Trts.idTrts
	WHERE DCcharacts.FuncStep='Tromb' 
		and Devices.Name='B10803W17-Xip2N' 
        and DCcharacts.IsCmp>0 
        and (DCcharacts.AnalyteCon like 2e-7 or DCcharacts.AnalyteCon like 2e-8);

SELECT * FROM DCcharacts where DCcharacts.Trt_id=5518; 


SELECT * FROM DCcharacts where DCcharacts.Comments like 'IonCal%'; 

