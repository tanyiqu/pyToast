import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QColor, QPainter, QPainterPath, QFont
import time

class TanToast(QWidget):
    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        # 窗口属性设置[10](@ref)
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # 无边框
            Qt.WindowType.WindowStaysOnTopHint |  # 置顶显示
            Qt.WindowType.Tool  # 关键属性：不显示任务栏图标[5,7](@ref)
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(36)
        self.setMinimumWidth(120)

        # UI组件初始化
        self.layout = QHBoxLayout()
        self.label = QLabel()
        self.label.setStyleSheet("""
color: #333333; 
font: 14px '微软雅黑';
padding: 0 16px;
""")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # 动画配置[1,9](@ref)
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.anim.setDuration(500)
        
        self.opacity_anim = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_anim.setDuration(300)

    def show_toast(self, message, duration=1500):
        """显示带滑动效果的Toast"""
        self.label.setText(message)
        self.adjustSize()  # 自适应宽度[2](@ref)

        # 计算左上角位置[10](@ref)
        screen = QApplication.primaryScreen().availableGeometry()
        target_x = 20  # 左侧留白20px
        target_y = 20  # 顶部留白20px
        
        # 初始位置（左侧隐藏）
        start_pos = QPoint(-self.width(), target_y)
        end_pos = QPoint(target_x, target_y)

        # 配置组合动画
        self.anim.setStartValue(start_pos)
        self.anim.setEndValue(end_pos)
        
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(0.96)

        # 启动动画队列
        self.show()
        self.anim.start()
        self.opacity_anim.start()
        QTimer.singleShot(duration, self.hide_toast)

    def hide_toast(self):
        """隐藏动画"""
        self.opacity_anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.start()
        self.opacity_anim.start()
        self.anim.finished.connect(self.close)

    def paintEvent(self, event):
        """绘制浅色背景和小圆角[11](@ref)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        # 设置8px圆角半径[11](@ref)
        path.addRoundedRect(self.rect(), 8, 8)  
        painter.fillPath(path, QColor(255, 255, 255, 230))  # 半透明白色背景
        
        # 添加细边框
        painter.setPen(QColor(240, 240, 240))
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), 8, 8)

    # @classmethod
    def make_toast(cls, message, duration=1500):
        if not cls._instance:
            cls._instance = TanToast()
        cls._instance.show_toast(message, duration)



# 使用示例
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # MinimalToast.make_toast("文件保存成功")
    # MinimalToast.make_toast("发现3个新通知", 2000)
    # MinimalToast().make_toast("发现3个新通知", 20000)
    # MinimalToast().make_toast("发现3个新通知222", 2000)

    # a = MinimalToast()
    # a.make_toast("发现3个新通知222", 22000)

    b = TanToast()
    b.make_toast("发现3个新通知333", 2000)

    sys.exit(app.exec())