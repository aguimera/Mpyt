
CREATE TABLE pyFET.ACcharacts_new LIKE pyFET.ACcharacts;


INSERT INTO ACcharacts_new(idACcharacts,User_id,Trt_id,DC_id,Data,IsOK,IsCmp,UpdateDate,MeasDate,Solution,Comments,FileName)
SELECT idACcharacts,User_id,Trt_id,DC_id,Data,IsOK,IsCmp,UpdateDate,MeasDate,Solution,Comments,FileName FROM ACcharacts WHERE ACcharacts.idACcharacts <10; 

INSERT INTO ACcharacts_new SELECT * FROM ACcharacts WHERE ACcharacts.idACcharacts>0 and ACcharacts.idACcharacts<1000;

SELECT * FROM ACcharacts WHERE ACcharacts.idACcharacts>0 and ACcharacts.idACcharacts<1000; 

SHOW PROCESSLIST;

INSERT INTO ACcharacts_new(idACcharacts,User_id,Trt_id,DC_id,Data,IsOK,IsCmp,UpdateDate,MeasDate,Ph,Solution,IonStrength,FuncStep,AnalyteCon,Comments,FileName)
           SELECT idACcharacts,User_id,Trt_id,DC_id,Data,IsOK,IsCmp,UpdateDate,MeasDate,Ph,Solution,IonStrength,FuncStep,AnalyteCon,Comments,FileName FROM ACcharacts WHERE ACcharacts.idACcharacts = 1;