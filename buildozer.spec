[app]

# 应用信息
title = 药房进货比较系统
package.name = pharmacy
package.domain = org.pharmacy

# 源码配置
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,ico,html,js,css,db,txt,woff,woff2,ttf,eot,svg,json
source.exclude_dirs = .github,exports,__pycache__,.git,build,dist,bin
source.exclude_patterns = hook-runtime.py,setup.bat,setup.sh,*.pyc,launcher.py,update_*.py,trigger_build.py,check_status.py,get_logs.py,upload_binary.py,cancel_queued.py,create_repo.py,pharmacy.db

# 版本
version = 1.0.0

# Python 依赖
requirements = python3,kivy==2.3.0,android,pyjnius,flask==2.3.3,flask-cors==4.0.0,requests==2.31.0,beautifulsoup4==4.12.2,lxml,openpyxl==3.1.2,Werkzeug==2.3.7,python-dateutil==2.8.2

# Android 配置
orientation = portrait
fullscreen = 1

# SDK/NDK
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# 架构（使用 android.archs 复数形式）
android.archs = arm64-v8a, armeabi-v7a

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 强制构建 APK（不构建 AAB）
android.debug_artifact = apk
android.release_artifact = apk

# 构建后端（develop分支支持AAB）
p4a.branch = develop
p4a.commit = develop

# 日志
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
