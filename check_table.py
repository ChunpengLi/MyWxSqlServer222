from wxcloudrun import db
from sqlalchemy import text

# 使用直接SQL查询表结构
def check_table_structure():
    try:
        with db.engine.connect() as conn:
            # 查询device_info_basic表的结构
            result = conn.execute(text("DESCRIBE device_info_basic"))
            print("device_info_basic表结构：")
            for row in result:
                print(row)
    except Exception as e:
        print(f"查询表结构失败：{e}")

if __name__ == "__main__":
    # 导入app以初始化数据库连接
    from run import app
    with app.app_context():
        check_table_structure()