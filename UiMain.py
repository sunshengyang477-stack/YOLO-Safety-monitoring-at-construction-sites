from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QSlider, QTableWidget,
                              QTableWidgetItem, QGroupBox, QComboBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon
try:
    import qtawesome as qta
    QTAWESOME_AVAILABLE = True
except ImportError:
    QTAWESOME_AVAILABLE = False


class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基于YOLO的施工现场安全智能监测系统")
        self.setWindowIcon(QIcon("icon.png"))  # 请替换为你的图标路径
        self.resize(1200, 800)

        # 主窗口中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QHBoxLayout(self.central_widget)

        # 左侧面板 (图像显示)
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel, 70)  # 70%宽度

        # 原始图像显示
        self.original_image_group = QGroupBox("原始图像")
        self.original_image_layout = QVBoxLayout()
        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setMinimumSize(640, 360)
        self.original_image_label.setText("未加载图像\n请选择图片进行检测")
        self.original_image_label.setStyleSheet("color: #95a5a6; font-style: italic;")
        self.original_image_label.setWordWrap(True)
        self.original_image_layout.addWidget(self.original_image_label)
        self.original_image_group.setLayout(self.original_image_layout)
        self.left_panel.addWidget(self.original_image_group)

        # 检测结果图像显示
        self.result_image_group = QGroupBox("检测结果")
        self.result_image_layout = QVBoxLayout()
        self.result_image_label = QLabel()
        self.result_image_label.setAlignment(Qt.AlignCenter)
        self.result_image_label.setMinimumSize(640, 360)
        self.result_image_label.setText("未加载图像\n检测结果将在此显示")
        self.result_image_label.setStyleSheet("color: #95a5a6; font-style: italic;")
        self.result_image_label.setWordWrap(True)
        self.result_image_layout.addWidget(self.result_image_label)
        self.result_image_group.setLayout(self.result_image_layout)
        self.left_panel.addWidget(self.result_image_group)

        # 右侧面板 (控制面板)
        self.right_panel = QVBoxLayout()
        self.main_layout.addLayout(self.right_panel, 30)  # 30%宽度

        # 模型选择
        self.model_group = QGroupBox("模型设置")
        self.model_layout = QVBoxLayout()

        self.model_combo = QComboBox()
        self.model_combo.addItems(["best"])
        self.model_layout.addWidget(QLabel("选择模型:"))
        self.model_layout.addWidget(self.model_combo)

        self.model_group.setLayout(self.model_layout)
        self.right_panel.addWidget(self.model_group)

        # 检测参数
        self.params_group = QGroupBox("检测参数")
        self.params_layout = QVBoxLayout()

        # 置信度阈值 - 水平布局
        confidence_layout = QHBoxLayout()
        self.confidence_label = QLabel("置信度阈值: 0.25")
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setRange(0, 100)
        self.confidence_slider.setValue(25)
        self.confidence_spinbox = QDoubleSpinBox()
        self.confidence_spinbox.setRange(0.0, 1.0)
        self.confidence_spinbox.setSingleStep(0.05)
        self.confidence_spinbox.setValue(0.25)
        confidence_layout.addWidget(self.confidence_label)
        confidence_layout.addWidget(self.confidence_slider)
        confidence_layout.addWidget(self.confidence_spinbox)

        # IoU阈值 - 水平布局
        iou_layout = QHBoxLayout()
        self.iou_label = QLabel("IoU阈值: 0.45")
        self.iou_slider = QSlider(Qt.Horizontal)
        self.iou_slider.setRange(0, 100)
        self.iou_slider.setValue(45)
        self.iou_spinbox = QDoubleSpinBox()
        self.iou_spinbox.setRange(0.0, 1.0)
        self.iou_spinbox.setSingleStep(0.05)
        self.iou_spinbox.setValue(0.45)
        iou_layout.addWidget(self.iou_label)
        iou_layout.addWidget(self.iou_slider)
        iou_layout.addWidget(self.iou_spinbox)

        self.params_layout.addLayout(confidence_layout)
        self.params_layout.addLayout(iou_layout)

        self.params_group.setLayout(self.params_layout)
        self.right_panel.addWidget(self.params_group)

        # Animation tracking for button states
        self._button_animations = {}

        # 功能按钮
        self.buttons_group = QGroupBox("功能")
        self.buttons_layout = QVBoxLayout()

        self.image_btn = QPushButton("图片检测")
        self.image_btn.setObjectName("techBtn")
        self.video_btn = QPushButton("视频检测")
        self.video_btn.setObjectName("techBtn")
        self.camera_btn = QPushButton("摄像头检测")
        self.camera_btn.setObjectName("techBtn")
        self.stop_btn = QPushButton("停止检测")
        self.stop_btn.setObjectName("warningBtn")
        self.save_btn = QPushButton("保存结果")
        self.save_btn.setObjectName("successBtn")
        
        # Add icons if qtawesome is available
        if QTAWESOME_AVAILABLE:
            self.image_btn.setIcon(qta.icon('fa5s.image', color='white'))
            self.video_btn.setIcon(qta.icon('fa5s.video', color='white'))
            self.camera_btn.setIcon(qta.icon('fa5s.video-slash', color='white'))  # or fa5s.camera
            self.stop_btn.setIcon(qta.icon('fa5s.stop-circle', color='white'))
            self.save_btn.setIcon(qta.icon('fa5s.save', color='white'))

        self.buttons_layout.addWidget(self.image_btn)
        self.buttons_layout.addWidget(self.video_btn)
        self.buttons_layout.addWidget(self.camera_btn)
        self.buttons_layout.addWidget(self.stop_btn)
        self.buttons_layout.addWidget(self.save_btn)

        self.buttons_group.setLayout(self.buttons_layout)
        self.right_panel.addWidget(self.buttons_group)

        # 检测结果表格
        self.results_group = QGroupBox("检测结果")
        self.results_layout = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["类别", "置信度", "位置(x)", "位置(y)"])
        self.results_table.setColumnWidth(0, 100)
        self.results_table.setColumnWidth(1, 80)
        self.results_table.setColumnWidth(2, 80)
        self.results_table.setColumnWidth(3, 80)

        self.results_layout.addWidget(self.results_table)
        self.results_group.setLayout(self.results_layout)
        self.right_panel.addWidget(self.results_group)

        # 状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")

        # 美化样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                font-family: "Microsoft YaHei", "Segoe UI", Arial, sans-serif;
            }
            QGroupBox {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 20px;
                font-weight: 600;
                font-size: 14px;
                color: #495057;
                background-color: white;
            }
            QGroupBox:hover {
                border-color: #3498db;
                box-shadow: 0 4px 8px rgba(52, 152, 219, 0.15);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2c3e50;
                background-color: white;
            }
            QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                color: white;
                padding: 10px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 13px;
                font-weight: 500;
                margin: 6px 4px;
                border-radius: 6px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2980b9;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: #2472a4;
                transform: translateY(0);
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
            /* Tech Blue Buttons (default) */
            QPushButton#techBtn {
                background-color: #3498db;
            }
            QPushButton#techBtn:hover {
                background-color: #2980b9;
            }
            QPushButton#techBtn:pressed {
                background-color: #2472a4;
            }
            /* Warning Red Button */
            QPushButton#warningBtn {
                background-color: #e74c3c;
            }
            QPushButton#warningBtn:hover {
                background-color: #c0392b;
                transform: translateY(-2px);
            }
            QPushButton#warningBtn:pressed {
                background-color: #a93226;
                transform: translateY(0);
            }
            /* Success Green Button */
            QPushButton#successBtn {
                background-color: #2ecc71;
            }
            QPushButton#successBtn:hover {
                background-color: #27ae60;
                transform: translateY(-2px);
            }
            QPushButton#successBtn:pressed {
                background-color: #219a52;
                transform: translateY(0);
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                gridline-color: #f1f3f5;
                selection-background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: 1px solid #e9ecef;
                font-weight: 600;
                font-size: 12px;
                color: #495057;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #f1f3f5;
            }
            QTableWidget::item:alternate {
                background-color: #f8f9fa;
            }
            QSlider::groove:horizontal {
                height: 10px;
                background: #e9ecef;
                border-radius: 5px;
                margin: 4px 0;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: 1px solid #2980b9;
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                width: 22px;
            }
            QDoubleSpinBox, QComboBox {
                padding: 8px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                min-width: 80px;
            }
            QDoubleSpinBox:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: #f8fdff;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                width: 20px;
                border-radius: 3px;
                background-color: #ecf0f1;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #d5dbdb;
            }
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
                font-weight: 500;
                font-size: 12px;
                border-top: 1px solid #bdc3c7;
                padding: 4px;
            }
            /* Running state for detection buttons */
            QPushButton#techBtn[running="true"] {
                background-color: #1abc9c;
            }
            QPushButton#techBtn[running="true"]:hover {
                background-color: #16a085;
            }
            QPushButton#warningBtn[running="true"] {
                background-color: #16a085;
            }
            QPushButton#warningBtn[running="true"]:hover {
                background-color: #1abc9c;
            }
            QPushButton#successBtn[running="true"] {
                background-color: #16a085;
            }
            QPushButton#successBtn[running="true"]:hover {
                background-color: #1abc9c;
            }
        """)

        # 连接信号和槽
        self.confidence_slider.valueChanged.connect(self.update_confidence)
        self.confidence_spinbox.valueChanged.connect(self.update_confidence_slider)
        self.iou_slider.valueChanged.connect(self.update_iou)
        self.iou_spinbox.valueChanged.connect(self.update_iou_slider)

    def update_confidence(self, value):
        confidence = value / 100.0
        self.confidence_spinbox.setValue(confidence)
        self.confidence_label.setText(f"置信度阈值: {confidence:.2f}")

    def update_confidence_slider(self, value):
        self.confidence_slider.setValue(int(value * 100))

    def update_iou(self, value):
        iou = value / 100.0
        self.iou_spinbox.setValue(iou)
        self.iou_label.setText(f"IoU阈值: {iou:.2f}")

    def update_iou_slider(self, value):
        self.iou_slider.setValue(int(value * 100))

    def display_image(self, label, image):
        if image is not None:
            h, w, ch = image.shape
            bytes_per_line = ch * w
            q_img = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # Clear placeholder styling when image is displayed
            label.setStyleSheet("")
        else:
            # Restore placeholder styling when no image
            if label == self.original_image_label:
                label.setText("未加载图像\n请选择图片进行检测")
                label.setStyleSheet("color: #95a5a6; font-style: italic;")
            elif label == self.result_image_label:
                label.setText("未加载图像\n检测结果将在此显示")
                label.setStyleSheet("color: #95a5a6; font-style: italic;")

    def clear_results(self):
        self.results_table.setRowCount(0)

    def add_detection_result(self, class_name, confidence, x, y):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)

        self.results_table.setItem(row, 0, QTableWidgetItem(class_name))
        self.results_table.setItem(row, 1, QTableWidgetItem(f"{confidence:.2f}"))
        self.results_table.setItem(row, 2, QTableWidgetItem(str(x)))
        self.results_table.setItem(row, 3, QTableWidgetItem(str(y)))

    def update_status(self, message):
        self.status_bar.showMessage(message)

    def set_detection_running(self, running):
        """Set visual state for detection buttons when detection is running/stopped"""
        buttons = [self.image_btn, self.video_btn, self.camera_btn, self.stop_btn, self.save_btn]
        for button in buttons:
            button.setProperty("running", running)
            # Force style refresh
            button.style().unpolish(button)
            button.style().polish(button)
             
        # Also update button enabled states to prevent multiple clicks
        if running:
            self.image_btn.setEnabled(False)
            self.video_btn.setEnabled(False)
            self.camera_btn.setEnabled(False)
            self.save_btn.setEnabled(False)
            # Stop button should remain enabled to allow stopping
            self.stop_btn.setEnabled(True)
        else:
            self.image_btn.setEnabled(True)
            self.video_btn.setEnabled(True)
            self.camera_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)  # Stop button disabled when not running

    def animate_button_background(self, button, target_color, duration=1000):
        """
        Animate button background color with fade-in/fade-out effect
        :param button: QPushButton to animate
        :param target_color: Target color in hex format (e.g., "#1abc9c")
        :param duration: Animation duration in milliseconds
        """
        # Stop any existing animation for this button
        if button in self._button_animations:
            self._button_animations[button].stop()
        
        # Create color animation
        animation = QPropertyAnimation(button, b"styleSheet")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Get current stylesheet
        current_style = button.styleSheet()
        
        # Create target stylesheet with new background color
        # Extract button type to apply correct selector
        obj_name = button.objectName()
        if obj_name == "techBtn":
            target_style = f"""
                QPushButton#{obj_name} {{
                    background-color: {target_color};
                }}
                QPushButton#{obj_name}:hover {{
                    background-color: {self._adjust_color_brightness(target_color, -15)};
                }}
                QPushButton#{obj_name}:pressed {{
                    background-color: {self._adjust_color_brightness(target_color, -30)};
                }}
            """
        elif obj_name == "warningBtn":
            target_style = f"""
                QPushButton#{obj_name} {{
                    background-color: {target_color};
                }}
                QPushButton#{obj_name}:hover {{
                    background-color: {self._adjust_color_brightness(target_color, -15)};
                }}
                QPushButton#{obj_name}:pressed {{
                    background-color: {self._adjust_color_brightness(target_color, -30)};
                }}
            """
        elif obj_name == "successBtn":
            target_style = f"""
                QPushButton#{obj_name} {{
                    background-color: {target_color};
                }}
                QPushButton#{obj_name}:hover {{
                    background-color: {self._adjust_color_brightness(target_color, -15)};
                }}
                QPushButton#{obj_name}:pressed {{
                    background-color: {self._adjust_color_brightness(target_color, -30)};
                }}
            """
        else:
            # Fallback for other buttons
            target_style = f"""
                QPushButton#{obj_name} {{
                    background-color: {target_color};
                }}
            """
        
        # For simplicity in this context, we'll animate by changing the running property
        # and letting the stylesheet handle the color change
        animation.setStartValue(current_style)
        animation.setEndValue(target_style)
        
        # Store animation reference
        self._button_animations[button] = animation
        animation.start()

    def _adjust_color_brightness(self, hex_color, adjustment):
        """
        Adjust the brightness of a hex color
        :param hex_color: Color in hex format (e.g., "#1abc9c")
        :param adjustment: Adjustment value (-255 to 255)
        :return: Adjusted hex color
        """
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, min(255, c + adjustment)) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def start_detection_animation(self):
        """Start pulsing animation for active detection buttons"""
        buttons = [self.image_btn, self.video_btn, self.camera_btn, self.stop_btn, self.save_btn]
        for button in buttons:
            if button.isEnabled():  # Only animate enabled buttons
                # Animate to running state color
                obj_name = button.objectName()
                if obj_name == "techBtn":
                    self.animate_button_background(button, "#1abc9c", 800)
                elif obj_name == "warningBtn":
                    self.animate_button_background(button, "#16a085", 800)
                elif obj_name == "successBtn":
                    self.animate_button_background(button, "#16a085", 800)

    def stop_detection_animation(self):
        """Stop animations and return buttons to normal state"""
        buttons = [self.image_btn, self.video_btn, self.camera_btn, self.stop_btn, self.save_btn]
        for button in buttons:
            # Stop any ongoing animation
            if button in self._button_animations:
                self._button_animations[button].stop()
                del self._button_animations[button]
            
            # Return to normal state based on objectName
            obj_name = button.objectName()
            if obj_name == "techBtn":
                self.animate_button_background(button, "#3498db", 500)
            elif obj_name == "warningBtn":
                self.animate_button_background(button, "#e74c3c", 500)
            elif obj_name == "successBtn":
                self.animate_button_background(button, "#2ecc71", 500)