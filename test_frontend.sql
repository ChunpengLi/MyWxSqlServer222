-- 测试INSERT语句
INSERT INTO device_info_basic (device_id, device_type, rated_power, main_version, sub_version, bms_mode, cabinet_version, cooling_method, production_plant, production_date, serial_number) VALUES ('Test_Frontend_Insert', '组串式PCS', '430kW', 'Vinco200版', '第3版', '不内置', '不适用', '液冷Liquid-Cooled', '汇川HC', '2025-09-30', '00084');

-- 验证数据是否插入成功
SELECT * FROM device_info_basic WHERE device_id = 'Test_Frontend_Insert';