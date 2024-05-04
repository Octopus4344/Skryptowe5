from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager, Screen


class FileSelection(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(size_hint=(1, None), height=100)

        self.label = Label(text='Wybierz plik z logami SSH do analizy')
        top_layout.add_widget(self.label)

        layout.add_widget(top_layout)

        self.file_chooser = FileChooserListView()
        layout.add_widget(self.file_chooser)

        bottom_layout = BoxLayout(size_hint=(1,None), height=100)
        select_button = Button(text='WYBIERZ', background_color=(0.2,0.6,1,1), color=(1,1,1,1), size=(50,50), size_hint=(0.5,None))
        select_button.bind(on_press=self.get_log_file)
        bottom_layout.add_widget(select_button)

        layout.add_widget(bottom_layout)

        return layout

    def get_log_file(self, instance):
        file = self.file_chooser.selection
        if file:
            file = file[0]
            self.label.text = f"Wybrany plik: {file}"
        else:
            popup = Popup(title='Blad', content=Label(text='Nie wybrano żadnego plliku'),
                          size_hint=(None, None), size=(200, 100))
            popup.open()


if __name__ == '__main__':
    FileSelection().run()
