[app]
title = TigerBot
package.name = tigerbot
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
# Оставили только базу, чтобы ускорить процесс
requirements = python3,kivy

orientation = portrait
fullscreen = 1

# iOS специфичные настройки
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/ios-control/ios-deploy
ios.ios_deploy_branch = master

# ЭТО ВАЖНО: отключаем подпись кода для GitHub
ios.codesign.allowed = False

[buildozer]
log_level = 2
warn_on_root = 1
