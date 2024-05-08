from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class MojaKlasa(BoxLayout):
    def __init__(self, **kwargs):
        super(MojaKlasa, self).__init__(**kwargs)

        # Tworzenie niebieskiego tła
        with self.canvas.before:
            Color(0, 0, 1, 1)  # Ustawienie koloru na niebieski w formacie RGBA
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MyApp(App):
    def build(self):
        return MojaKlasa()

if __name__ == "__main__":
    MyApp().run()
