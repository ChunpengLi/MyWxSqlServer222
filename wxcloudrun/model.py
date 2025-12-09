from datetime import datetime

from wxcloudrun import db


# 设备信息表
class DeviceInfo(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'device_info'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), unique=True, nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 计数表（保留，暂时不删除）
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
