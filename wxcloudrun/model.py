from datetime import datetime

from wxcloudrun import db


# 设备信息表
class DeviceInfo(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'device_info_basic'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), unique=True, nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    container_code = db.Column(db.String(63))
    ip_addr = db.Column(db.String(8))
    issue_record = db.Column(db.String(256))
    remark = db.Column(db.String(256))
    create_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 维修信息表
class RepairInfo(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'repair_info'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    repair_date = db.Column(db.Date, nullable=False)
    repair_note = db.Column(db.String(256))
    engineer_name = db.Column(db.String(32))
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
