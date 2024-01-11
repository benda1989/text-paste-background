

import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QColorDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw, ImageFont


def draw_text(text, font_size=200, font_stroke=0, color="red", font='DOUYUFONT.OTF',
              background_image="bg.jpg",
              border=20, border_color="white",
              max_fill=60, raw_y=0, save_name="output_image.jpg",):
    background_image = Image.open(background_image)
    font = ImageFont.truetype(font, font_size)
    text_width, text_height = font.getsize(text)
    max_text_width = int(background_image.width * max_fill / 100)
    wrapped_text = text
    wrapped_lines = []
    if "##" in text:
        wrapped_lines = text.split("##")
        maxlen = len(wrapped_lines[0])
        for i in wrapped_lines[1:]:
            leni = len(i)
            if leni > maxlen:
                maxlen = leni
        for i, v in enumerate(wrapped_lines):
            wrapped_lines[i] = " "*(maxlen-len(v))*3 + v
    elif text_width > max_text_width:
        line = ""
        for word in text:
            if font.getsize(line + word)[0] <= max_text_width:
                line += word
            else:
                wrapped_lines.append(line)
                line = word
        if line:
            wrapped_lines.append(line)
    if len(wrapped_lines) > 0:
        wrapped_text = "\n".join(wrapped_lines)
        text_width, text_height = font.getsize_multiline(wrapped_text)
    x = (background_image.width - text_width) // 2
    y = (background_image.height - text_height) // 2 + raw_y
    draw = ImageDraw.Draw(background_image)

    if font_stroke:
        draw.text((x-font_stroke, y), wrapped_text, fill=color, font=font, stroke_width=border, stroke_fill=border_color)
        draw.text((x+font_stroke, y), wrapped_text, fill=color, font=font, stroke_width=border, stroke_fill=border_color)
        draw.text((x, y-font_stroke), wrapped_text, fill=color, font=font, stroke_width=border, stroke_fill=border_color)
        draw.text((x, y+font_stroke), wrapped_text, fill=color, font=font, stroke_width=border, stroke_fill=border_color)
        draw.text((x, y), wrapped_text, fill=color, font=font)
    else:
        draw.text((x, y), wrapped_text, fill=color, font=font, stroke_width=border, stroke_fill=border_color)
    try:
        background_image.save(save_name)
    except:
        background_image.save("result_%d_.jpg" % time.time())


class Dialog(QWidget):
    color_board = '#ffffff'
    color_font = '#3b2dff'
    font = "default.otf"
    background = "bg.jpg"

    def __init__(self):
        super().__init__()
        self.setWindowTitle('文字图片批量生成 by GKK')

        # 创建布局
        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("\n\n\n多张图片时使用 回车换行，\n单张文字中输入## 替换 换行，\n文本默认自动换行\n字体默认使用：default.otf\n背景图片默认使用：bg.jpg\n")
        self.text_input.setMinimumWidth(400)
        left_layout.addWidget(self.text_input)

        # 右侧布局
        right_layout = QVBoxLayout()
        # 背景图片选择框
        self.background_button = QPushButton('选择背景图片')
        self.background_button.clicked.connect(self.choose_background)
        right_layout.addWidget(self.background_button)
        self.background_label = QLabel()
        self.background_label.setPixmap(QPixmap(self.background).scaledToWidth(220))
        right_layout.addWidget(self.background_label)
        # 字体选择框
        self.font_button = QPushButton('选择字体')
        self.font_button.setText(os.path.basename(self.font))
        self.font_button.clicked.connect(self.choose_font)
        right_layout.addWidget(self.font_button)
        # 字体大小
        self.number1_input = QLineEdit()
        self.number1_input.setText("250")
        number1_layout = QHBoxLayout()
        number1_layout.addWidget(QLabel('字体大小'))
        number1_layout.addWidget(self.number1_input)
        right_layout.addLayout(number1_layout)
        # 字体颜色
        self.color1_button = QPushButton('字体颜色')
        self.color1_button.clicked.connect(self.choose_color1)
        self.color1_label = QLabel('')
        self.color1_label.setStyleSheet(f'background-color: {self.color_font};')
        color1_layout = QHBoxLayout()
        color1_layout.addWidget(self.color1_button)
        color1_layout.addWidget(self.color1_label)
        right_layout.addLayout(color1_layout)
        self.number5_input = QLineEdit()
        self.number5_input.setText("0")
        number5_layout = QHBoxLayout()
        number5_layout.addWidget(QLabel('字体加粗'))
        number5_layout.addWidget(self.number5_input)
        # right_layout.addLayout(number5_layout)
        # 边框大小
        self.number2_input = QLineEdit()
        self.number2_input.setText("30")
        number2_layout = QHBoxLayout()
        number2_layout.addWidget(QLabel('边框大小'))
        number2_layout.addWidget(self.number2_input)
        right_layout.addLayout(number2_layout)
        # 边框颜色
        self.color2_button = QPushButton('边框颜色')
        self.color2_button.clicked.connect(self.choose_color2)
        self.color2_label = QLabel('')
        self.color2_label.setStyleSheet(f'background-color: {self.color_board};')
        color2_layout = QHBoxLayout()
        color2_layout.addWidget(self.color2_button)
        color2_layout.addWidget(self.color2_label)
        right_layout.addLayout(color2_layout)
        # 占比
        self.number3_input = QLineEdit()
        self.number3_input.setText("80")
        number3_layout = QHBoxLayout()
        number3_layout.addWidget(QLabel('自动换行宽度百分比'))
        number3_layout.addWidget(self.number3_input)
        right_layout.addLayout(number3_layout)

        self.number4_input = QLineEdit()
        self.number4_input.setText("-10")
        number4_layout = QHBoxLayout()
        number4_layout.addWidget(QLabel('文字上下偏移（向上偏填负值）'))
        number4_layout.addWidget(self.number4_input)
        right_layout.addLayout(number4_layout)
        # 开始
        self.start_button = QPushButton('开始生成')
        self.start_button.clicked.connect(self.start)
        right_layout.addWidget(self.start_button)
        # self.start_label = QLabel('')
        # start_layout = QHBoxLayout()
        # start_layout.addWidget(self.start_button)
        # start_layout.addWidget(self.start_label)
        # right_layout.addLayout(start_layout)
        # 添加右侧布局到主布局
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 创建文本输出框
        self.text_output = QTextEdit()
        self.text_output.setMaximumHeight(200)
        self.text_output.setReadOnly(True)

        # 添加主布局和文本输出框到窗口
        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        # layout.addWidget(self.text_output)
        self.setLayout(layout)

    def start(self):
        if self.background:
            try:
                for i, text in enumerate(self.text_input.toPlainText().splitlines()):
                    draw_text(text,
                              int(self.number1_input.text()),
                              int(self.number5_input.text()),
                              self.color_font,
                              self.font,
                              self.background,
                              int(self.number2_input.text()),
                              self.color_board,
                              int(self.number3_input.text()),
                              int(self.number4_input.text()),
                              "r_"+text.replace(" ", "").replace(".", "").replace("##", "")+".jpg"
                              )
                QMessageBox.about(self, "帮助", '生成完成，总数：%d ' % (i+1))
            except Exception as e:
                QMessageBox.warning(self, '警告', e)

    def choose_font(self):
        self.font, _ = QFileDialog.getOpenFileName(self, '选择字体', '', 'Font files (*.ttf *.otf)')
        self.font_button.setText(os.path.basename(self.font))

    def choose_background(self):
        self.background, _ = QFileDialog.getOpenFileName(self, '选择背景图片', '', 'Image files (*.png *.jpg *.bmp)')
        self.background_label.clear()
        self.background_label.setPixmap(QPixmap(self.background).scaledToHeight(100))

    def choose_color1(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_font = color.name()
        self.color1_label.setStyleSheet(f'background-color: {self.color_font};')

    def choose_color2(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_board = color.name()
        self.color2_label.setStyleSheet(f'background-color: {self.color_board};')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
