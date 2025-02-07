# ScreenSetting  
屏幕设置  
Simple and quick modification screen settings  
一个快速切换屏幕配置小工具，包含切换分辨率、刷新率、Dpi  

### 前置设置
请确保系统设置中可以切换对应的分辨率、刷新率、Dpi，本程序无法设置系统不支持的屏幕配置  
Nvidia用户可以通过Nvidia控制面板添加自定义配置  
![image](https://github.com/user-attachments/assets/3066dff5-9660-47ba-9208-4ae45e4a8d23)

### 配置读取
程序启动时自动读取配置：  
1、优先读取`D:\Tools`下的`Screen.config`文件，不存在则读取程序同目录下的`Screen.config`文件  
2、上述文件均不存在时会在程序同目录创建`Screen.config`配置文件  
配置文件修改后需要重启生效  
配置文件示例：  
```
预设:
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

固定窗口:
False
```
配置文件中每一行为一个记录  
预设的记录格式为：快捷键、预设名称、分辨率、刷新率、DPI  
当不设置快捷键时需要写成`None`  
请注意严格按照格式编写，否则会导致程序运行出错  

### 程序功能
程序启动后会在系统右下角显示托盘图标，请注意托盘图标折叠  
- 右键图标将显示设置菜单：    
![image](https://github.com/user-attachments/assets/81166c64-c221-4940-bb2f-87bc168667ab)  
其中第一行显示配置文件来源：  
  `Tools`表示配置读取自`D:\Tools`目录的配置文件  
  `Native`表示配置读取自程序同目录下的配置文件  

- 左键点击图标显示程序窗口  
![image](https://github.com/user-attachments/assets/e2314188-b0d0-4301-8934-a5d046e91730)
程序窗口弹出位置为屏幕右下角，内容与右键菜单相同  

### 致谢
本程序基于[https://github.com/SelfEnough/ScreenResolutionSwitcher](https://github.com/SelfEnough/ScreenResolutionSwitcher)修改  

### 后记
本程序适用于使用Moonlight等远控时快速切换屏幕设置  
源代码为ScreenSetting.py，可使用build.txt中的指令打包成exe  
仅在Windows10与Windows11上测试1080p、2K分辨率，其它平台尚未测试  
欢迎阅读我的代码并提出宝贵修改意见  

### 更新
v1.2  - 新增主窗口标题显示配置文件位置：`控制台: Native/Tools`
      - 新增窗口锁定功能，可在配置文件和主窗口中点击图标修改
        锁定：🔒   点击按钮后需点击确定按键关闭窗口
        解锁；🔓   点击任意按钮后自动关闭窗口（默认）
        注意与v1.0版本配置文件不兼容，需删除后重新生成并设置config配置文件
