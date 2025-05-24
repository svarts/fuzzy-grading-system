from PySide6 import QtWidgets, QtCore, QtGui
from controller import sim

class GradeApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎓 Fuzzy Öğrenci Notlandırma 🌈")
        self.setGeometry(150, 100, 600, 800)
        self.setStyleSheet("background-color: #f0f4f8;")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        header = QtWidgets.QLabel("Öğrenci Performans Değerlendirme")
        header.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("color: #334155;")
        main_layout.addWidget(header)

        self.sliders = {}
        params = [
            ("Vize Sınavı", 'midterm', 0, 100, "#F87171"),
            ("Final Sınavı", 'final', 0, 100, "#60A5FA"),
            ("Ödev Ortalaması", 'homework', 0, 100, "#34D399"),
            ("Devam Oranı", 'attendance', 0, 100, "#FBBF24"),
            ("Katılım", 'participation', 0, 10, "#A78BFA"),
        ]
        for label, key, lo, hi, color in params:
            box = QtWidgets.QGroupBox(label)
            box.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: #1E293B; }}")
            vbox = QtWidgets.QVBoxLayout()

            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setRange(lo, hi)
            slider.setValue((lo+hi)//2)
            slider.setStyleSheet(
                f"QSlider::groove:horizontal {{ background: #E2E8F0; height: 8px; border-radius: 4px; }}"
                f"QSlider::handle:horizontal {{ background: {color}; width: 16px; border-radius: 8px; margin: -4px 0; }}"
            )
            slider.valueChanged.connect(lambda val, k=key: self.on_change(k, val))

            pb = QtWidgets.QProgressBar()
            pb.setRange(lo, hi)
            pb.setValue(slider.value())
            pb.setTextVisible(True)
            pb.setStyleSheet(
                f"QProgressBar {{ background: #E2E8F0; border-radius: 5px; text-align: center; }}"
                f"QProgressBar::chunk {{ background-color: {color}; border-radius: 5px; }}"
            )

            vbox.addWidget(slider)
            vbox.addWidget(pb)
            box.setLayout(vbox)
            main_layout.addWidget(box)

            self.sliders[key] = (slider, pb)

        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setStyleSheet("color: #CBD5E1;")
        main_layout.addWidget(sep)

        output_box = QtWidgets.QGroupBox("Sonuçlar")
        output_box.setStyleSheet("QGroupBox { font-weight: bold; color: #1E293B; }")
        out_layout = QtWidgets.QVBoxLayout()

        self.grade_label = QtWidgets.QLabel("Final Notu: —")
        self.grade_label.setFont(QtGui.QFont("Segoe UI", 14))
        self.grade_label.setStyleSheet("color: #0F172A;")
        out_layout.addWidget(self.grade_label)

        self.grade_bar = QtWidgets.QProgressBar()
        self.grade_bar.setRange(0, 100)
        self.grade_bar.setFixedHeight(20)
        self.grade_bar.setStyleSheet(
            "QProgressBar { background: #E2E8F0; border-radius: 5px; }"
            "QProgressBar::chunk { background-color: #3B82F6; border-radius: 5px; }"
        )
        out_layout.addWidget(self.grade_bar)

        self.tutor_label = QtWidgets.QLabel("Destek İhtiyacı: —")
        self.tutor_label.setFont(QtGui.QFont("Segoe UI", 14))
        self.tutor_label.setStyleSheet("color: #0F172A;")
        out_layout.addWidget(self.tutor_label)

        self.tutor_bar = QtWidgets.QProgressBar()
        self.tutor_bar.setRange(0, 10)
        self.tutor_bar.setFixedHeight(20)
        self.tutor_bar.setStyleSheet(
            "QProgressBar { background: #E2E8F0; border-radius: 5px; }"
            "QProgressBar::chunk { background-color: #6366F1; border-radius: 5px; }"
        )
        out_layout.addWidget(self.tutor_bar)

        output_box.setLayout(out_layout)
        main_layout.addWidget(output_box)

        self.evaluate()

    def on_change(self, key, value):
        sim.input[key] = value
        _, pb = self.sliders[key]
        pb.setValue(value)
        self.evaluate()

    def evaluate(self):
        for key, (slider, _) in self.sliders.items():
            sim.input[key] = slider.value()
        sim.compute()
        g = sim.output['grade']
        t = sim.output['tutoring']
        self.grade_label.setText(f"Final Notu: {g:.1f}")
        self.grade_bar.setValue(int(g))
        self.tutor_label.setText(f"Destek İhtiyacı: {t:.1f}")
        self.tutor_bar.setValue(int(t))


def run_app():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = GradeApp()
    window.show()
    sys.exit(app.exec())