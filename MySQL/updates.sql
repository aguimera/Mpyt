
UPDATE DCcharacts SET DCcharacts.AnalyteCon=20e-9, DCcharacts.FuncStep = 'Tromb'
	WHERE DCcharacts.FuncStep = '20nM Tromb';


SELECT DCcharacts.AnalyteCon,DCcharacts.FuncStep FROM DCcharacts WHERE DCcharacts.FuncStep like '%Tromb';



UPDATE  ACcharacts,Trts, Devices set ACcharacts.FuncStep = ACcharacts.Comments
    WHERE Trts.idTrts = ACcharacts.Trt_id AND Devices.idDevices = Trts.Device_id AND Devices.Name='B10803W17-Xip2N';
    
    
SELECT ACcharacts.FuncStep,ACcharacts.Comments FROM ACcharacts,Trts, Devices
    WHERE Trts.idTrts = ACcharacts.Trt_id AND Devices.idDevices = Trts.Device_id AND Devices.Name='B10803W17-Xip2N';
    
    

SELECT Trts.Name, Trts.Type_id, TrtTypes.Name 
	FROM Trts, TrtTypes 
    WHERE Trts.Type_id=TrtTypes.idTrtTypes and (Trts.Name like 'B002%T4' or Trts.Name like 'B002%T6');
    
UPDATE Trts, TrtTypes SET Trts.Type_id = 126
	WHERE Trts.Type_id=TrtTypes.idTrtTypes and (Trts.Name like 'B002%T4' or Trts.Name like 'B002%T6');
    
UPDATE Trts, TrtTypes SET Trts.Type_id = 127
	WHERE Trts.Type_id=TrtTypes.idTrtTypes and (Trts.Name like 'B002%T1' or Trts.Name like 'B002%T7');    
    
UPDATE Trts, TrtTypes SET Trts.Type_id = 128
	WHERE Trts.Type_id=TrtTypes.idTrtTypes and (Trts.Name like 'B002%T3' or Trts.Name like 'B002%T5');    

UPDATE Trts, TrtTypes SET Trts.Type_id = 129
	WHERE Trts.Type_id=TrtTypes.idTrtTypes and (Trts.Name like 'B002%T2' or Trts.Name like 'B002%T8');    

UPDATE Devices SET Devices.Wafer_id = 70
	WHERE Devices.Wafer_id=152;

SELECT * FROM Devices WHERE Devices.Wafer_id=70;

SELECT * FROM Devices WHERE Devices.Wafer_id=70 and Devices.Name like '%W3%';

UPDATE Devices SET Devices.Name = REPLACE(Devices.Name,'W03','W3') WHERE Devices.Wafer_id=70;

UPDATE Devices, Trts, Wafers SET Trts.Name = REPLACE(Trts.Name,'W03','W3') 
	WHERE Wafers.idWafers = Devices.Wafer_id and Devices.idDevices = Trts.Device_id AND Wafers.Name='B10631W3';

SELECT Trts.Name FROM Devices, Trts, Wafers WHERE Wafers.idWafers = Devices.Wafer_id and Devices.idDevices = Trts.Device_id AND Wafers.Name='B10631W3';




UPDATE ACcharacts SET ACcharacts.Trt_id = 6848 WHERE ACcharacts.Trt_id = 4512;
UPDATE DCcharacts SET DCcharacts.Trt_id = 6848 WHERE DCcharacts.Trt_id = 4512;

UPDATE ACcharacts SET ACcharacts.Trt_id = 6847 WHERE ACcharacts.Trt_id = 4513;
UPDATE DCcharacts SET DCcharacts.Trt_id = 6847 WHERE DCcharacts.Trt_id = 4513;

UPDATE ACcharacts SET ACcharacts.Trt_id = 6846 WHERE ACcharacts.Trt_id = 4514;
UPDATE DCcharacts SET DCcharacts.Trt_id = 6846 WHERE DCcharacts.Trt_id = 4514;

SELECT Trts.Name, Trts.idTrts FROM Devices, Trts WHERE Devices.idDevices = Trts.Device_id AND Devices.Name='B10179W11-T7';



