[app]
title = 药房进货比较系统
package.name = pharmacy
package.domain = org.pharmacy
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,ico,html,js,css,db,spec,txt,woff,woff2,ttf,eot,svg
source.exclude_dirs = .github,exports,__pycache__,.git
source.exclude_patterns = hook-runtime.py,setup.bat,setup.sh,*.pyc

version = 1.0.0
requirements = python3==3.11.6,kivy==2.3.0,android,pillow,flask==2.3.3,flask-cors==4.0.0,requests==2.31.0,beautifulsoup4==4.12.2,lxml==4.9.3,openpyxl==3.1.2,xlrd==2.0.1,pandas==2.0.3,fake-useragent==1.4.0,python-dateutil==2.8.2,Werkzeug==2.3.7
p4a.branch = master
orientation = portrait

fullscreen = 1
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.sdk = 33

android.meta_data = app_name=药房进货比较系统

[buildozer]

log_level = 2
warn_on_root = 1
