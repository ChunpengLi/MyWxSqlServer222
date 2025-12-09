from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters, DeviceInfo
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 4
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/device', methods=['GET'])
def get_device():
    """
    根据device_id查询设备的production_date
    :return: 设备的生产日期
    """
    try:
        # 获取请求参数
        device_id = request.args.get('device_id')
        
        # 检查device_id参数
        if not device_id:
            return make_err_response('缺少device_id参数')
        
        # 查询设备信息
        device = DeviceInfo.query.filter(DeviceInfo.device_id == device_id).first()
        
        # 返回结果
        if device:
            return make_succ_response(device.production_date.strftime('%Y-%m-%d'))
        else:
            return make_succ_response('未找到该设备')
    except Exception as e:
        # 记录详细错误信息
        import traceback
        error_msg = f"查询设备失败: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        # 返回包含详细错误信息的响应
        return make_err_response(error_msg)


@app.route('/api/test_db', methods=['GET'])
def test_db_connection():
    """
    测试数据库连接是否成功
    :return: 连接结果
    """
    try:
        # 执行一个简单的查询来测试数据库连接
        from wxcloudrun import db
        # 使用会话执行一个简单的查询
        db.session.execute('SELECT 1')
        return make_succ_response('数据库连接成功')
    except Exception as e:
        # 记录详细错误信息
        import traceback
        error_msg = f"数据库连接失败: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        # 返回包含详细错误信息的响应
        return make_err_response(error_msg)
