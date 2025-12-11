import os

# 是否开启debug模式
DEBUG = True

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'Lcp5655734')
if(1):  # 1: 上传正式（腾讯云内网访问更直接）  # 0： 本地调试（外网访问腾讯云）
    db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')
else:
    db_address = os.environ.get("MYSQL_ADDRESS", 'sh-cynosdbmysql-grp-cq366x3k.sql.tencentcdb.com:21004')
