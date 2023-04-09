import os
import platform
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from qfluentwidgets import PushButton, TextEdit
from .gallery_interface import GalleryInterface


class LaunchInterface(GalleryInterface):
    def __init__(self, parent=None):
        super().__init__(
            title="一键启动",
            subtitle='',
            parent=parent
        )

        self.system_label = QLabel()
        self.graphics_label = QLabel()
        self.memory_label = QLabel()
        self.git_label = QLabel()
        self.start_button = PushButton("启动")

        # 设置字体
        font = QFont("Segoe UI")
        font.setPointSize(12)
        self.system_label.setFont(font)
        self.graphics_label.setFont(font)
        self.memory_label.setFont(font)
        self.git_label.setFont(font)
        self.start_button.setFont(font)

        # 布局控件
        info_widget = QWidget(self)
        info_widget_layout = QVBoxLayout(info_widget)
        info_widget_layout.addWidget(self.system_label)
        info_widget_layout.addWidget(self.graphics_label)
        info_widget_layout.addWidget(self.memory_label)
        info_widget_layout.addWidget(self.git_label)

        self.addExampleCard(
            self.tr('相关信息'),
            info_widget,
        )

        # 添加启动参数
        default_param = "--autolaunch --no-half --disable-safe-unpickle --opt-sub-quad-attention --disable-nan-check"
        lowvram_param = ""
        medvram_param = ""
        use_cpu_param = ""
        graphics_memory = self.get_graphics_memory()
        graphics_card = self.get_graphics_card()

        if "错误" not in graphics_memory:
            if int(graphics_memory.split()[0]) <= 6:
                lowvram_param = "--lowvram "
            if int(graphics_memory.split()[0]) > 6 & int(graphics_memory.split()[0]) <= 8:
                medvram_param = "--medvram"
            if int(graphics_memory.split()[0]) > 6 & int(graphics_memory.split()[0]) <= 8:
                medvram_param = "--medvram"

        self.launch_params = default_param + " " + lowvram_param + \
            " " + medvram_param + " " + use_cpu_param
        line_edit = TextEdit(self)
        line_edit.setText(self.launch_params)

        self.addExampleCard(
            title=self.tr("启动参数"),
            widget=line_edit,
            sourcePath='',
            stretch=1
        )

        self.addExampleCard(
            self.tr('一键启动，启动完成后打开浏览器'),
            self.start_button,
        )

        self.system_label.setText(
            "操作系统: " + platform.system() + " " + platform.release())
        self.graphics_label.setText("显卡: " + graphics_card)
        self.memory_label.setText("显存: " + graphics_memory)
        self.git_label.setText("Git版本: " + self.get_git_version())

        self.start_button.clicked.connect(self.start_script)

    def get_graphics_card(self):
        command = "wmic path win32_VideoController get name"
        output = subprocess.check_output(
            command, shell=True).decode("utf-8").strip()
        return output.split("\n")[1]

    # 获取显存信息
    def get_graphics_memory(self):
        try:
            command = 'powershell "Get-ItemProperty -Path \\"HKLM:\\SYSTEM\\ControlSet001\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0*\\" -Name HardwareInformation.qwMemorySize -ErrorAction SilentlyContinue | Select-Object -ExpandProperty HardwareInformation.qwMemorySize"'
            output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
            memory = int(output)
            memory_gb = round(memory / (1024**3))
            return str(memory_gb) + " " + "GB"
        except:
            return "错误"

    def get_git_version(self):
        try:
            output = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD']).decode().strip()
            return output
        except:
            return "当前目录不是一个Git项目"

    def start_script(self):
        # 启动脚本
        os.environ['http_proxy'] = ''
        os.environ['https_proxy'] = ''
        subprocess.Popen(['cmd.exe', '/c', '.\\venv\\Scripts\\activate.bat && python launch.py'] + self.launch_params.split())
