"""
药房进货比较系统 - Android APK 入口
将 Flask 后端 + Kivy WebView 整合为独立 Android APP
"""
import os
import sys
import threading
import socket
import time

def get_base_path():
    """获取应用根目录（兼容开发环境和打包环境）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

def find_free_port(start_port=8080, max_tries=20):
    """查找可用端口"""
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return start_port + max_tries

def start_flask(port):
    """后台启动 Flask 服务器"""
    os.chdir(BASE_PATH)
    # 确保数据库目录存在
    db_path = os.path.join(BASE_PATH, 'pharmacy.db')
    if not os.path.exists(db_path):
        # 创建空数据库
        import sqlite3
        db = sqlite3.connect(db_path)
        db.close()

    # 禁止 Flask 日志刷屏
    import logging
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    from app import app as flask_app
    flask_app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True
    )

def main():
    # 等待几秒让 Android 完成初始化
    if 'ANDROID_ARGUMENTS' in os.environ or 'ANDROID_APP_PATH' in os.environ:
        time.sleep(2)

    port = find_free_port(8080)
    print(f'[APK] 启动 Flask 服务，端口: {port}')

    # 后台启动 Flask
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # 等待 Flask 启动
    import urllib.request
    import urllib.error
    for i in range(30):
        try:
            url = f'http://127.0.0.1:{port}/health'
            req = urllib.request.Request(url, method='GET')
            urllib.request.urlopen(req, timeout=2)
            print(f'[APK] Flask 就绪 (耗时 {(i+1)*0.5:.1f}s)')
            break
        except:
            time.sleep(0.5)

    # 使用 Kivy WebView
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.core.window import Window
    from kivy.logger import Logger

    Logger.setLevel('WARNING')

    class PharmacyApp(App):
        def build(self):
            Window.bind(on_keyboard=self.on_key)

            # 使用 Kivy 内置 WebView（通过 webview 组件）
            try:
                from kivy.uix.boxlayout import BoxLayout
                from kivy.core.window import Window as W
                W.clearcolor = (1, 1, 1, 1)  # 白色背景

                from android.webview import WebView  # type: ignore
                wv = WebView()
                wv.load_url(f'http://127.0.0.1:{port}/')
                return wv
            except ImportError:
                # 桌面调试模式：用浏览器打开
                import webbrowser
                webbrowser.open(f'http://127.0.0.1:{port}/')
                # 显示提示
                from kivy.uix.label import Label
                return Label(
                    text=f'药房系统已启动\n端口: {port}\n请在浏览器中访问\nhttp://127.0.0.1:{port}',
                    font_size='20sp',
                    halign='center',
                    valign='middle'
                )

        def on_key(self, window, key, scancode, codepoint, modifier):
            """返回键退出"""
            if key == 27:  # ESC / 返回键
                return True  # 拦截返回键
            return False

    app = PharmacyApp()
    app.run()

if __name__ == '__main__':
    main()
