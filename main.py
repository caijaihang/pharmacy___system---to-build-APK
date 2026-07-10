"""
药房进货比较系统 - Android APK 入口
将 Flask 后端 + Android WebView 整合为独立 APP
后台运行Flask服务器，前台用原生Android WebView渲染页面
"""
import os
import sys
import threading
import socket
import time
import logging

def get_base_path():
    """获取应用根目录"""
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
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
    db_path = os.path.join(BASE_PATH, 'pharmacy.db')
    if not os.path.exists(db_path):
        import sqlite3
        db = sqlite3.connect(db_path)
        db.close()

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

def wait_for_flask(port, timeout=30):
    """等待 Flask 服务就绪"""
    import urllib.request
    for i in range(int(timeout / 0.5)):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2)
            return True
        except:
            time.sleep(0.5)
    return False

def create_android_webview(url):
    """使用 pyjnius 创建原生 Android WebView"""
    from jnius import autoclass
    from android.runnable import run_on_ui_thread

    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    WebSettings = autoclass('android.webkit.WebSettings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Color = autoclass('android.graphics.Color')

    activity = PythonActivity.mActivity

    @run_on_ui_thread
    def setup():
        # 创建 WebView
        webview = WebView(activity)

        # 配置 WebView 设置
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setDatabaseEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setLoadWithOverviewMode(True)
        settings.setUseWideViewPort(True)
        settings.setSupportZoom(False)
        settings.setBuiltInZoomControls(False)
        settings.setCacheMode(WebSettings.LOAD_DEFAULT)
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW)

        # 设置白色背景
        webview.setBackgroundColor(Color.WHITE)

        # 设置 WebViewClient（在APP内打开链接，不跳转浏览器）
        webview.setWebViewClient(WebViewClient())

        # 加载URL
        webview.loadUrl(url)

        # 设置为Activity的内容视图（替换Kivy的SDL视图）
        activity.setContentView(webview)

    setup()
    return True

def main():
    # Android 等待初始化
    is_android = 'ANDROID_ARGUMENTS' in os.environ or 'ANDROID_APP_PATH' in os.environ
    if is_android:
        time.sleep(2)

    port = find_free_port(8080)
    print(f'[APK] Flask 端口: {port}')

    # 后台启动 Flask
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # 等待 Flask 就绪
    if wait_for_flask(port):
        print(f'[APK] Flask 就绪')
    else:
        print(f'[APK] Flask 启动超时')

    url = f'http://127.0.0.1:{port}/'

    if is_android:
        # Android: 使用原生 WebView
        try:
            create_android_webview(url)
            # 保持主线程运行
            while True:
                time.sleep(1)
        except Exception as e:
            print(f'[APK] WebView 创建失败: {e}')
            # 降级：启动 Kivy 显示错误
            _start_kivy_fallback(url, str(e))
    else:
        # 桌面调试：用 Kivy 简单窗口
        _start_kivy_fallback(url, None)

def _start_kivy_fallback(url, error_msg):
    """Kivy 降级模式（桌面调试用）"""
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.core.window import Window

        Window.clearcolor = (1, 1, 1, 1)

        text = f'药房系统已启动\n\n访问地址:\n{url}'
        if error_msg:
            text += f'\n\nWebView错误: {error_msg}'

        # 桌面调试时自动打开浏览器
        import webbrowser
        webbrowser.open(url)

        class FallbackApp(App):
            def build(self):
                return Label(
                    text=text,
                    font_size='16sp',
                    color=(0.2, 0.2, 0.2, 1),
                    halign='center',
                    valign='middle'
                )

        FallbackApp().run()
    except ImportError:
        # Kivy 不可用时，直接等待
        print(f'[APK] 请访问: {url}')
        while True:
            time.sleep(1)

if __name__ == '__main__':
    main()
