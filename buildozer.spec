[app]

# 应用信息
title = 药房进货比较系统
package.name = pharmacy
package.domain = org.pharmacy

# 源码配置
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,ico,html,js,css,db,txt,json
source.exclude_dirs = .github,exports,__pycache__,.git,build,dist,bin
source.exclude_patterns = hook-runtime.py,setup.bat,setup.sh,*.pyc,launcher.py,update_*.py,trigger_build.py,check_status.py,get_logs.py,upload_binary.py,cancel_queued.py,create_repo.py,pharmacy.db,default.exe

# 版本
version = 1.0.0

# Python 依赖（webview bootstrap：无需Kivy/SDL2）
requirements = python3,flask,requests

# Android 配置
orientation = portrait
fullscreen = 1

# 架构
android.archs = arm64-v8a

# 权限
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# p4a配置
p4a.branch = develop

# 日志
log_level = 2
warn_on_root = 0

[buildozer]
log_level = 2
warn_on_root = 0
