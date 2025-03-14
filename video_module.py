import cv2
import numpy as np
import tkinter as tk
from tkinter import Canvas

# Коэффициент максимального масштабирования (1 - нет масштабирования, 2 - увеличение в 2 раза при максимальной громкости)
max_scale = 0.65
# Размер квадрата отображаемого видео
square_size = 600

class PulsatingSphereWindow:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("")
        self.root.geometry(f"{square_size}x{square_size}")
        self.root.resizable(False, False)


        # Установка пользовательской иконки
        icon_image = tk.PhotoImage(file='AI_Icon.png')  # Замените 'path/to/your/icon.png' на путь к вашей иконке
        self.root.iconphoto(False, icon_image)


        # Получение размеров экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Расчет координат для центрирования окна
        x = (screen_width // 2) - (square_size // 2)
        y = (screen_height // 2) - (square_size // 2)

        # Установка геометрии с новыми координатами
        self.root.geometry(f"{square_size}x{square_size}+{x}+{y}")

        self.root.configure(bg='black')
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.canvas = Canvas(self.root, width=square_size, height=square_size, bg='black', highlightthickness=0)
        self.canvas.pack()
        self.amplitude = 0.5  # Начальное масштабирование
        self.target_amplitude = 1.0
        self.photo = None
        self.update()

    def set_amplitude(self, amplitude):
        self.target_amplitude = amplitude

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        # Плавное изменение амплитуды
        self.amplitude += (self.target_amplitude - self.amplitude) * 0.05

        # Извлечение центрального квадрата из видео
        height, width, _ = frame.shape
        min_dim = min(width, height)
        start_x = (width - min_dim) // 2
        start_y = (height - min_dim) // 2
        frame = frame[start_y:start_y + min_dim, start_x:start_x + min_dim]

        # Изменение масштаба видео в зависимости от амплитуды
        scale = 0.5 + (max_scale - 0.5) * self.amplitude
        new_size = int(min_dim * scale)
        frame = cv2.resize(frame, (new_size, new_size))

        # Обрезка или добавление черных полей для сохранения размеров square_size x square_size
        if new_size > square_size:
            start = (new_size - square_size) // 2
            frame = frame[start:start + square_size, start:start + square_size]
        else:
            delta = square_size - new_size
            top, bottom = delta // 2, delta - (delta // 2)
            left, right = delta // 2, delta - (delta // 2)
            frame = cv2.copyMakeBorder(frame, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Преобразование изображения OpenCV в формат, пригодный для Tkinter
        img = np.array(frame)
        img = np.require(img, np.uint8, 'C')
        self.photo = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.root.after(int(1000 / 120), self.update)  # Обновление каждые ~16 мс для 60 FPS
