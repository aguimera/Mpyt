SELECT * FROM Devices WHERE Devices.Wafer_id IS NULL;
DELETE FROM Devices WHERE Devices.Wafer_id IS NULL;

SELECT * FROM Trts WHERE Trts.Device_id IS NULL;
DELETE FROM Trts WHERE Trts.Device_id IS NULL;

SELECT * FROM DCcharacts WHERE DCcharacts.Trt_id IS NULL;
DELETE FROM DCcharacts WHERE DCcharacts.Trt_id IS NULL;

SELECT * FROM ACcharacts WHERE ACcharacts.DC_id IS NULL;
DELETE FROM ACcharacts WHERE ACcharacts.DC_id IS NULL;

