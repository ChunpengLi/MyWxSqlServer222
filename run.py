import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    # 提供默认值，方便直接运行
    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    app.run(host=host, port=port)
