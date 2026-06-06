[app]
title = My Project
package.name = myproject
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,json,sh
version = 0.1
requirements = python3,kivy,requests
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.build_tools_version = 33.0.2
android.accept_sdk_license = True

[buildozer]
log_level = 2

android.keystore = max_ai.keystore
android.keystore_passwd = maxai123
android.keyalias = max_ai
android.keyalias_passwd = maxai123
