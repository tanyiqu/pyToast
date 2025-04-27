import sys
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QColor, QPainter, QPainterPath, QFont, QFontDatabase

class ProgressToast(QWidget):
    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        # 窗口属性设置[2,8](@ref)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool  # 禁止任务栏显示
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(60)
        self.duration = 2000

        # 初始化UI
        self.init_ui()
        self.init_animation()

    def init_ui(self):
        # 主布局[3,11](@ref)
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)
        
        # 文字标签
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.text_label.setStyleSheet("color: #333333; font: 14px '微软雅黑';")
        
        # 进度条[9,11](@ref)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: #00000020;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background: #2196F3;
                border-radius: 1px;
            }
        """)

        layout.addWidget(self.text_label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

    def init_animation(self):
        # 滑动动画[1,8](@ref)
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        self.pos_anim.setDuration(500)
        
        # 透明度动画
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)

    def show_toast(self, message, duration=2000):
        """显示带进度条的Toast"""
        self.text_label.setText(message)
        self.duration = duration
        self.adjustSize()

        # 初始位置计算[1,5](@ref)
        screen = QApplication.primaryScreen().availableGeometry()
        start_x = -self.width()
        start_y = 20  # 顶部留白20px
        end_x = 20
        
        # 动画参数设置
        self.pos_anim.setStartValue(QPoint(start_x, start_y))
        self.pos_anim.setEndValue(QPoint(end_x, start_y))
        
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(0.95)

        # 启动动画
        self.show()
        self.pos_anim.start()
        self.opacity_anim.start()
        
        # 进度条更新[9,10](@ref)
        self.progress.setValue(100)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)  # 50ms更新一次

    def update_progress(self):
        current = self.progress.value()
        step = 100 * 50 / self.duration
        self.progress.setValue(current - step)
        if self.progress.value() <= 0:
            self.timer.stop()
            self.hide_toast()

    def hide_toast(self):
        """隐藏动画"""
        self.opacity_anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.pos_anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.opacity_anim.start()
        self.pos_anim.start()
        self.pos_anim.finished.connect(self.close)

    def paintEvent(self, event):
        """绘制带小圆角的背景[3,5](@ref)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 8, 8)  # 8px圆角
        painter.fillPath(path, QColor(255, 255, 255, 230))  # 半透明白色背景
        
        # 添加细边框
        painter.setPen(QColor(240, 240, 240))
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 8, 8)

    @classmethod
    def make_toast(cls, message, duration=2000):
        if not cls._instance:
            cls._instance = ProgressToast()
        cls._instance.show_toast(message, duration)

# 使用示例
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ProgressToast.make_toast("文件保存成功", 2500)
    sys.exit(app.exec())