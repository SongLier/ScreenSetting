import os
import sys
import subprocess
import threading
from PIL import Image
from pystray import Icon, MenuItem
import keyboard
import winreg
from functools import partial
import tkinter as tk


class ResolutionChanger:
    def resource_path_ico(self, relative_path):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def resource_path_config(self, relative_path):
        if getattr(sys, 'frozen', False):
            if os.path.exists(os.path.join("D:\\Tools", relative_path)):
                base_path = "D:\\Tools"
                self.pathmod = "Tools"
            else:
                base_path = os.path.dirname(sys.executable)
        else:
            if os.path.exists(os.path.join("D:\\Tools", relative_path)):
                base_path = "D:\\Tools"
                self.pathmod = "Tools"
            else:
                base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def get_theme(self):
        try:
            if sys.platform == "win32":
                reg_key = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                reg_value = "SystemUsesLightTheme"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_key) as key:
                    theme_value, _ = winreg.QueryValueEx(key, reg_value)
                    return theme_value
        except Exception as e:
            print(f"Error detecting theme: {e}")
            return 1

    def __init__(self):
        self.presets = []
        self.resolutions = []
        self.dpi_list = []
        self.refresh_rates = []
        self.ifkey = 0
        self.pathmod = ""
        self.button_add=False

        self.load_config()
        self.menu, self.button = self.build_menu()

        theme = self.get_theme()
        icon_path = self.resource_path_ico(
            "icon_white.png" if theme == 0 else "icon_black.png"
        )

        self.icon_image = Image.open(icon_path)
        self.icon = Icon("屏幕设置", self.icon_image, "屏幕设置", self.menu)

        self.icon.run()

    def load_config(self):
        config_path = self.resource_path_config("Screen.config")
        if not os.path.exists(config_path):
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("""预设:
ctrl+alt+shift+[ 1K 1920x1080 60 100
ctrl+alt+shift+] 2K 2560x1440 60 125
None 2k+ 2560x1440 60 100
                   
分辨率:
2560x1440
1920x1080
1366x768

刷新率:
60
48

DPI:
100
125                   
""")
        with open(config_path, "r", encoding="utf-8") as f:
            x = 0
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == "预设:":
                    x = 1
                    continue
                elif line == "分辨率:":
                    x = 2
                    continue
                elif line == "刷新率:":
                    x = 3
                    continue
                elif line == "DPI:":
                    x = 4
                    continue
                if x == 1:
                    parts = line.replace('x', ' ').split()
                    self.presets.append([parts[0], parts[1], int(
                        parts[2]), int(parts[3]), int(parts[4]), int(parts[5])])
                elif x == 2:
                    parts = line.split('x')
                    self.resolutions.append([int(parts[0]), int(parts[1])])
                elif x == 3:
                    self.refresh_rates.append(int(line))
                elif x == 4:
                    self.dpi_list.append(int(line))
        f.close()

    def build_menu(self):
        menu_items = []
        button_items = []
        if self.pathmod == "Tools":
            menu_items.append(
                MenuItem("============< Tools >============", self.show_window, default=True))
        else:
            menu_items.append(
                MenuItem("============< Native >===========", self.show_window, default=True))
        if self.presets:
            for preset in self.presets:
                if preset[0] == "None":
                    menu_items.append(MenuItem("📦   "+str(preset[2])+"x"+str(preset[3])+'  '+str(preset[4])+"Hz  "+str(
                        preset[5])+'%  '+' ' * 13+preset[1], partial(self.set_custom_settings, preset)))
                    button_items.append(("📦   "+str(preset[2])+"x"+str(preset[3])+'  '+str(preset[4])+"Hz  "+str(
                        preset[5])+'%  '+' ' * 13+preset[1], lambda a=1, b=2, preset=preset: self.set_custom_settings(preset, a, b)))
                else:
                    self.ifkey = 1
                    menu_items.append(MenuItem("📦   "+str(preset[2])+"x"+str(preset[3])+'  '+str(preset[4])+"Hz  "+str(
                        preset[5])+'%  '+' '*8+preset[0][-1]+' '*4+preset[1], partial(self.set_custom_settings, preset)))
                    button_items.append(("📦   "+str(preset[2])+"x"+str(preset[3])+'  '+str(preset[4])+"Hz  "+str(
                        preset[5])+'%  '+' '*8+preset[0][-1]+' '*4+preset[1], lambda a=1, b=2, preset=preset: self.set_custom_settings(preset, a, b)))
                    keyboard.add_hotkey(
                        preset[0], lambda a=1, b=2, preset=preset: self.set_custom_settings(preset, a, b))

        if self.resolutions:
            for res in self.resolutions:
                menu_items.append(
                    MenuItem(f"🏁   {res[0]}x{res[1]}", partial(self.set_resolution, res)))
                button_items.append(
                    (f"🏁   {res[0]}x{res[1]}", lambda a=1, b=2, res=res: self.set_resolution(res, a, b)))

        if self.refresh_rates:
            for rate in self.refresh_rates:
                menu_items.append(
                    MenuItem(f"⚡   {rate}Hz", partial(self.set_rate, rate)))
                button_items.append(
                    (f"⚡   {rate}Hz", lambda a=1, b=2, rate=rate: self.set_rate(rate, a, b)))

        if self.dpi_list:
            for dpi in self.dpi_list:
                menu_items.append(
                    MenuItem(f"🔍   {dpi}%", partial(self.set_dpi, dpi)))
                button_items.append(
                    (f"🔍   {dpi}%", lambda a=1, b=2, dpi=dpi: self.set_dpi(dpi, a, b)))
        menu_items.append(MenuItem("💤   退出", lambda: self.quit()))
        return tuple(menu_items), button_items

    def show_window(self, icon=None, item=None):

        def tk_window():

            root = tk.Tk()
            root.title("控制台")
            
            if self.button_add==False:
                self.button.append(("✔   确定", root.quit))
                self.button.append(("💤   退出", lambda: self.quit()))
                self.button_add=True

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            lengths = [len(self.presets), len(self.resolutions), len(
                self.refresh_rates), len(self.dpi_list)]
            lengths_sum = [sum(lengths[:i+1]) for i in range(len(lengths))]

            subject_num = len([x for x in lengths if x != 0])

            window_width = 0
            window_height = 0

            column_count = 0
            # 将按钮放入 grid 中，动态设置每行每列的位置
            for i, (text, cmd) in enumerate(self.button):
                button = tk.Button(root, text=text, command=cmd, anchor='w')
                if i < lengths_sum[0]:
                    if lengths[0] != 0 and i == 0:
                        column_count += 1
                    button.grid(column=column_count, row=i, padx=10,
                                pady=5, sticky="ew")
                elif i < lengths_sum[1]:
                    if lengths[1] != 0 and i == lengths_sum[0]:
                        column_count += 1
                    button.grid(column=column_count, row=i-lengths_sum[0], padx=10,
                                pady=5, sticky="ew")
                elif i < lengths_sum[2]:
                    if lengths[2] != 0 and i == lengths_sum[1]:
                        column_count += 1
                    button.grid(column=column_count, row=i-lengths_sum[1], padx=10,
                                pady=5, sticky="ew")
                elif i < lengths_sum[3]:
                    if lengths[3] != 0 and i == lengths_sum[2]:
                        column_count += 1
                    button.grid(column=column_count, row=i-lengths_sum[2], padx=10,
                                pady=5, sticky="ew")
                else:
                    if subject_num == 1:
                        button.grid(column=1, row=max(lengths)-i+lengths_sum[3]+1, padx=10,
                                    pady=5, sticky="ew")
                    else:
                        button.grid(
                            column=subject_num-i+lengths_sum[3], row=max(lengths_sum), padx=10, pady=5, sticky="ew")

            button_title = []
            for a, b in self.button:
                button_title.append(a)
            title_max = [max([len(item) for item in button_title[0:lengths_sum[0]]]) if button_title[0:lengths_sum[0]] else 0,
                         max([len(item) for item in button_title[lengths_sum[0]:lengths_sum[1]]]
                             ) if button_title[lengths_sum[0]:lengths_sum[1]] else 0,
                         max([len(item) for item in button_title[lengths_sum[1]:lengths_sum[2]]]
                             ) if button_title[lengths_sum[1]:lengths_sum[2]] else 0,
                         max([len(item) for item in button_title[lengths_sum[2]:lengths_sum[3]]]) if button_title[lengths_sum[2]:lengths_sum[3]] else 0]

            title_max[0] = int(title_max[0]*0.5)
            window_width = sum(title_max)*13
            if subject_num == 1:
                window_height = max(lengths)*42+84
            else:
                window_height = max(lengths)*42+42
            x = screen_width - window_width - 10
            y = screen_height - window_height - 60
            root.geometry(f"{window_width}x{window_height}+{x}+{y}")

            root.mainloop()

        threading.Thread(target=tk_window, daemon=True).start()

    def set_resolution(self, resolution, a, b):
        try:
            width, height = resolution[0], resolution[1]
            command = ["QRes.exe", '/x:' + str(width), '/y:' + str(height)]
            subprocess.run(command, check=True)
            print(' '.join(command))
        except subprocess.CalledProcessError:
            print(f"Failed to set resolution to {width}x{height}")

    def set_rate(self, refresh_rate, a, b):
        try:
            command = ["QRes.exe", '/r:' + str(refresh_rate)]
            subprocess.run(command, check=True)
            print(' '.join(command))
        except subprocess.CalledProcessError:
            print(f"Failed to set refresh rate to {refresh_rate}Hz")

    def set_dpi(self, scaling_percentage, a, b):
        try:
            command = ["SetDPI.exe", str(scaling_percentage)]
            subprocess.run(command, check=True)
            print(' '.join(command))
        except subprocess.CalledProcessError:
            print(f"Failed to set DPI to {scaling_percentage}%")

    def set_custom_settings(self, preset, a, b):
        width, height, rate, dpi = preset[2], preset[3], preset[4], preset[5]
        try:
            commands = [
                ["QRes.exe", f"/x:{width}", f"/y:{height}"],
                ["QRes.exe", f"/r:{rate}"],
                ["SetDPI.exe", str(dpi)]
            ]
            for cmd in commands:
                subprocess.run(cmd, check=True)
                print(' '.join(cmd))
        except subprocess.CalledProcessError:
            print(f"Failed to set custom settings to {preset[1]}")

    def quit(self):
        self.icon.stop()
        if self.ifkey == 1:
            keyboard.unhook_all_hotkeys()


if __name__ == "__main__":
    res_changer = ResolutionChanger()
