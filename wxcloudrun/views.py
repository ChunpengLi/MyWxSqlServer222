from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters, DeviceInfo
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.logger import logger, get_logs, clear_logs, log_exception


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
        logger.info(f"收到设备查询请求，device_id: {device_id}")
        
        # 检查device_id参数
        if not device_id:
            logger.warning("设备查询请求缺少device_id参数")
            return make_err_response('缺少device_id参数')
        
        # 查询设备信息
        logger.info(f"开始查询设备信息，device_id: {device_id}")
        device = DeviceInfo.query.filter(DeviceInfo.device_id == device_id).first()
        
        # 返回结果
        if device:
            production_date = device.production_date.strftime('%Y-%m-%d')
            logger.info(f"查询成功，device_id: {device_id}，production_date: {production_date}")
            return make_succ_response(production_date)
        else:
            logger.info(f"未找到设备，device_id: {device_id}")
            return make_succ_response('未找到该设备')
    except Exception as e:
        # 记录详细错误信息
        logger.error(f"查询设备失败: {str(e)}")
        log_exception(e)
        # 返回包含详细错误信息的响应
        return make_err_response(f"查询设备失败: {str(e)}")


@app.route('/api/device', methods=['POST'])
def add_device():
    """
    添加设备信息
    :return: 添加结果
    """
    try:
        # 获取请求体参数
        params = request.get_json()
        logger.info(f"收到添加设备请求，参数: {params}")
        
        # 检查device_id和production_date参数
        if 'device_id' not in params:
            logger.warning("添加设备请求缺少device_id参数")
            return make_err_response('缺少device_id参数')
        if 'production_date' not in params:
            logger.warning("添加设备请求缺少production_date参数")
            return make_err_response('缺少production_date参数')
        
        device_id = params['device_id']
        production_date = params['production_date']
        
        # 检查设备ID是否已存在
        existing_device = DeviceInfo.query.filter(DeviceInfo.device_id == device_id).first()
        if existing_device:
            logger.warning(f"设备ID已存在，device_id: {device_id}")
            return make_err_response('设备ID已存在')
        
        # 创建新设备信息
        logger.info(f"开始添加设备，device_id: {device_id}，production_date: {production_date}")
        from wxcloudrun import db
        new_device = DeviceInfo()
        new_device.device_id = device_id
        new_device.production_date = datetime.strptime(production_date, '%Y-%m-%d').date()
        new_device.create_time = datetime.now()
        
        # 保存到数据库
        db.session.add(new_device)
        db.session.commit()
        
        logger.info(f"添加设备成功，device_id: {device_id}")
        return make_succ_response('添加设备成功')
    except Exception as e:
        # 记录详细错误信息
        logger.error(f"添加设备失败: {str(e)}")
        log_exception(e)
        # 返回包含详细错误信息的响应
        return make_err_response(f"添加设备失败: {str(e)}")


@app.route('/api/test_db', methods=['GET'])
def test_db_connection():
    """
    测试数据库连接是否成功
    :return: 连接结果
    """
    try:
        logger.info("开始测试数据库连接")
        # 执行一个简单的查询来测试数据库连接
        from wxcloudrun import db
        # 使用会话执行一个简单的查询
        db.session.execute('SELECT 1')
        logger.info("数据库连接测试成功")
        return make_succ_response('数据库连接成功')
    except Exception as e:
        # 记录详细错误信息
        logger.error(f"数据库连接测试失败: {str(e)}")
        log_exception(e)
        # 返回包含详细错误信息的响应
        return make_err_response(f"数据库连接失败: {str(e)}")


@app.route('/api/logs', methods=['GET'])
def get_logs_api():
    """
    获取日志信息
    :return: 日志信息
    """
    try:
        logs = get_logs()
        return make_succ_response(logs)
    except Exception as e:
        logger.error(f"获取日志失败: {str(e)}")
        log_exception(e)
        return make_err_response(f"获取日志失败: {str(e)}")


@app.route('/api/logs', methods=['DELETE'])
def clear_logs_api():
    """
    清空日志信息
    :return: 清空结果
    """
    try:
        clear_logs()
        logger.info("日志已清空")
        return make_succ_empty_response()
    except Exception as e:
        logger.error(f"清空日志失败: {str(e)}")
        log_exception(e)
        return make_err_response(f"清空日志失败: {str(e)}")
