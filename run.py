import sys

from wxcloudrun import app

# 启动Flask Web服务
if __name__ == '__main__':
    a=1
    app.run(host=sys.argv[1], port=sys.argv[2])
