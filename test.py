from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Tworzenie etykiety
        label = Label(text="Hello, world!")

        # Dodawanie koloru tła za pomocą canvas
        with label.canvas.before:
            Color(0.2, 0.5, 0.7, 1)  # (R, G, B, A)
            label.rect = Rectangle(size=label.size, pos=label.pos)

        label.bind(size=label.setter('size'), pos=label.setter('pos'))

        # Dodawanie etykiety do układu
        layout.add_widget(label)

        return layout


if __name__ == '__main__':
    TestApp().run()
