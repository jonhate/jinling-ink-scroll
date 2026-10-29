"""serve.py -- 本地起一个静态服务预览数字长卷

用法：
    python serve.py           # 默认 8080 端口
    python serve.py 9000

浏览器打开 http://127.0.0.1:8080/

（DZI 瓦片必须通过 http 加载，直接双击 index.html 会被浏览器的
  file:// 同源策略挡住。）
"""
import http.server
import os
import socketserver
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    # 必须用多线程版本：DZI 查看器会并发请求几十块瓦片，
    # 单线程的 TCPServer 会把它们排成队，本地预览会异常地慢。
    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with Server(('127.0.0.1', PORT), Handler) as httpd:
        print('水墨金陵梦 · 数字长卷')
        print('  目录：%s' % ROOT)
        print('  地址：http://127.0.0.1:%d/' % PORT)
        print('  Ctrl+C 结束')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n已停止')
