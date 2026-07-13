"""
药房进货比较系统 - Android APK 入口 (webview bootstrap)
Flask 后端 + Android WebView
"""
import os
import sys
import threading
import socket
import time

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

def find_free_port(start_port=8080, max_tries=20):
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    return start_port + max_tries

def start_flask(port):
    os.chdir(BASE_PATH)
    db_path = os.path.join(BASE_PATH, 'pharmacy.db')
    if not os.path.exists(db_path):
        import sqlite3
        db = sqlite3.connect(db_path)
        db.close()

    import logging
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    from app import app as flask_app
    flask_app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True
    )

def wait_for_flask(port, timeout=30):
    import urllib.request
    for i in range(int(timeout / 0.5)):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/health', timeout=2)
            return True
        except:
            time.sleep(0.5)
    return False

def main():
    is_android = 'ANDROID_ARGUMENTS' in os.environ or 'ANDROID_APP_PATH' in os.environ
    if is_android:
        time.sleep(2)

    port = find_free_port(8080)
    print(f'[APK] Flask port: {port}')

    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    if wait_for_flask(port):
        print(f'[APK] Flask ready')
    else:
        print(f'[APK] Flask startup timeout')

    # webview bootstrap会自动加载页面，这里只需保持主线程运行
    if not is_android:
        import webbrowser
        webbrowser.open(f'http://127.0.0.1:{port}/')
        print(f'Open browser: http://127.0.0.1:{port}/')

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
