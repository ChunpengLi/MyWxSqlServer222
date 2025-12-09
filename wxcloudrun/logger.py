import logging
import io
import traceback
from datetime import datetime

# 创建一个内存日志缓冲区
log_buffer = io.StringIO()

# 配置日志记录器
logger = logging.getLogger('wxcloudrun')
logger.setLevel(logging.DEBUG)

# 创建日志格式化器
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 创建内存日志处理器
memory_handler = logging.StreamHandler(log_buffer)
memory_handler.setLevel(logging.DEBUG)
memory_handler.setFormatter(formatter)

# 创建控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(memory_handler)
logger.addHandler(console_handler)


def get_logs():
    """
    获取所有日志信息
    :return: 日志字符串
    """
    log_buffer.seek(0)
    return log_buffer.read()


def clear_logs():
    """
    清空日志缓冲区
    """
    log_buffer.truncate(0)
    log_buffer.seek(0)


def log_exception(exc):
    """
    记录异常信息
    :param exc: 异常对象
    """
    logger.error(f"异常: {str(exc)}")
    logger.error(f"堆栈跟踪: {traceback.format_exc()}")
