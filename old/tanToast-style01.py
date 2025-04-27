import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPainter, QPainterPath

class Toast(QWidget):
    _instance = None  # 单例模式实现

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(40)
        
        # 初始化UI
        self.layout = QHBoxLayout()
        self.label = QLabel()
        self.label.setStyleSheet("color: white; font: 14px '微软雅黑'; padding: 0 12px;")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
        # 动画设置
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(500)
        self.position_animation = QPropertyAnimation(self, b"pos")
        self.position_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def show_toast(self, message, duration=2000):
        """显示Toast的核心方法"""
        self.label.setText(message)
        self.adjustSize()  # 根据文本长度自适应宽度
        
        # 计算显示位置（屏幕底部居中）
        screen_geo = QApplication.primaryScreen().availableGeometry()
        x = (screen_geo.width() - self.width()) // 2
        y = screen_geo.height() - 100
        
        # 初始化动画参数
        self.setGeometry(x, y, self.width(), self.height())
        self.opacity_animation.setStartValue(0.0)
        self.opacity_animation.setEndValue(0.9)
        self.opacity_animation.finished.connect(lambda: QTimer.singleShot(duration, self.hide_toast))
        
        # 启动动画
        self.show()
        self.opacity_animation.start()

    def hide_toast(self):
        """隐藏动画"""
        self.opacity_animation.setStartValue(0.9)
        self.opacity_animation.setEndValue(0.0)
        self.opacity_animation.finished.connect(self.close)
        self.opacity_animation.start()

    def paintEvent(self, event):
        """绘制圆角和背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 20, 20)
        painter.fillPath(path, QColor(50, 50, 50, 200))  # 深灰色半透明背景

    @classmethod
    def make_toast(cls, message, duration=2000):
        """静态调用方法"""
        if not cls._instance:
            cls._instance = Toast()
        cls._instance.show_toast(message, duration)

# 使用示例
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 显示基础Toast
    Toast.make_toast("操作成功！", 2000)
    
    # 显示带样式的Toast（可扩展）
    # Toast.make_toast("<img src='icon.png'> 文件已保存", 3000)
    
    sys.exit(app.exec())