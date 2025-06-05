# app/widgets/animated_stack.py
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import QRect, Qt, QPropertyAnimation, QEasingCurve

class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation_duration = 300  # ms
        self._is_animating = False

    def slide_to_index(self, index):
        """
        Hiệu ứng slide từ trang hiện tại → trang có index mới.
        """
        if self._is_animating or index == self.currentIndex():
            return
        self._is_animating = True
        old_widget = self.currentWidget()
        new_widget = self.widget(index)
        direction = 1 if index > self.currentIndex() else -1

        # Kích thước stack
        width = self.frameRect().width()
        height = self.frameRect().height()

        # Vị trí ban đầu của new_widget (ở bên phải hoặc trái)
        new_widget.setGeometry( QRect(direction * width, 0, width, height) )
        new_widget.show()

        # Animation cho new_widget vào vị trí (0,0)
        anim_new = QPropertyAnimation(new_widget, b"geometry")
        anim_new.setDuration(self.animation_duration)
        anim_new.setStartValue( QRect(direction * width, 0, width, height) )
        anim_new.setEndValue( QRect(0, 0, width, height) )
        anim_new.setEasingCurve(QEasingCurve.OutCubic)

        # Animation cho old_widget ra phía đối diện
        anim_old = QPropertyAnimation(old_widget, b"geometry")
        anim_old.setDuration(self.animation_duration)
        anim_old.setStartValue( QRect(0, 0, width, height) )
        anim_old.setEndValue( QRect(-direction * width, 0, width, height) )
        anim_old.setEasingCurve(QEasingCurve.OutCubic)

        # Khi animation old_widget kết thúc, setCurrentIndex
        def on_finished():
            self.setCurrentIndex(index)
            old_widget.hide()
            # Đặt lại vị trí old_widget về vị trí gốc (để lần sau hiển thị không bị lệch)
            old_widget.setGeometry( QRect(0, 0, width, height) )
            self._is_animating = False

        anim_old.finished.connect(on_finished)

        # Chạy đồng thời hai animation
        anim_new.start()
        anim_old.start()
    