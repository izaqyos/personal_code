import tkinter as tk
from PIL import Image, ImageDraw
import numpy as np
import tensorflow as tf
from modelutils import create_model

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.image = Image.new('L', (400, 400), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.predict_digit)

        self.model = self.load_model()

    def paint(self, event):
        x1, y1 = (event.x - 5), (event.y - 5)
        x2, y2 = (event.x + 5), (event.y + 5)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black', width=10)
        self.draw.ellipse([x1, y1, x2, y2], fill='black')

    def predict_digit(self, event):
        self.image.save('digit.png')
        img = self.image.resize((28, 28)).convert('L')
        img = np.array(img)
        img = np.clip(img, 0, 255)
        img = 255 - img
        img = img / 255.0
        img = img.reshape(1, 28, 28, 1)
        pred = self.model.predict(img)
        digit = np.argmax(pred)
        print(f'Predicted Digit: {digit}')

        pred = self.model.predict(img)[0]
        
        # Display the probabilities for all digits
        for i, prob in enumerate(pred):
            print(f"Digit {i}: {prob * 100:.2f}%")

        self.canvas.delete('all')
        self.image = Image.new('L', (400, 400), 'white')
        self.draw = ImageDraw.Draw(self.image)

    def load_model(self):
        model = create_model()
        model.load_weights('mnist_model.weights.h5')  # Ensure you have the model weights saved in this file
        return model

if __name__ == '__main__':
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()
