import urllib.request
import urllib.parse
import json

# 测试INSERT语句
url = 'http://localhost:8080/api/execute_sql'
sql = "INSERT INTO device_info_basic (device_id, device_type, rated_power, main_version, sub_version, bms_mode, cabinet_version, cooling_method, production_plant, production_date, serial_number) VALUES ('M4C30NALCHC250900083', '组串式PCS', '430kW', 'Vinco200版', '第3版', '不内置', '不适用', '液冷Liquid-Cooled', '汇川HC', '2025-09-30', '00083');"

# 构建请求数据
data = {'sql': sql}
json_data = json.dumps(data).encode('utf-8')

# 设置请求头
headers = {
    'Content-Type': 'application/json',
    'Content-Length': len(json_data)
}

# 发送POST请求
try:
    req = urllib.request.Request(url, data=json_data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        response_text = response.read().decode('utf-8')
        print(f"状态码: {status_code}")
        print(f"响应内容: {response_text}")
        
        # 只有当状态码为200时才继续查询
        if status_code == 200:
            # 尝试查询刚才插入的数据
            select_sql = "SELECT * FROM device_info_basic WHERE device_id = 'M4C30NALCHC250900082';"
            select_data = {'sql': select_sql}
            select_json_data = json.dumps(select_data).encode('utf-8')
            select_req = urllib.request.Request(url, data=select_json_data, headers=headers, method='POST')
            with urllib.request.urlopen(select_req) as select_response:
                select_status_code = select_response.getcode()
                select_response_text = select_response.read().decode('utf-8')
                print(f"\n查询状态码: {select_status_code}")
                print(f"查询响应内容: {select_response_text}")
            
            # 解析查询结果
            result = json.loads(select_response_text)
            if isinstance(result, list) and len(result) > 0:
                print(f"\n成功插入数据，查询到{len(result)}条记录")
                for record in result:
                    print(f"设备ID: {record.get('device_id')}, 设备类型: {record.get('device_type')}")
            else:
                print("\n插入失败，未查询到数据")

except urllib.error.HTTPError as e:
    print(f"HTTP错误: {e.code} - {e.reason}")
    # 读取并打印错误响应内容
    if hasattr(e, 'read'):
        error_content = e.read().decode('utf-8')
        print(f"错误响应内容: {error_content}")
except Exception as e:
    print(f"请求失败: {e}")