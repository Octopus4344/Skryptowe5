from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from zad_1 import file_reader_new


class FileSelection(Screen):

    def __init__(self, **kwargs):
        super(FileSelection, self).__init__(**kwargs)
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

        self.add_widget(layout)


    def get_log_file(self, instance):
        file = self.file_chooser.selection
        if file:
            file = file[0]
            self.manager.get_screen('Logs').process_file(file)
            self.manager.current = 'Logs'
        else:
            popup = Popup(title='Blad', content=Label(text='Nie wybrano żadnego pliku'),
                          size_hint=(None, None), size=(200, 100))
            popup.open()


class DisplayLogs(Screen):
    def __init__(self, **kwargs):
        super(DisplayLogs, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.selected_file_label = Label(text='Wybrany plik: ')
        layout.add_widget(self.selected_file_label)

        scroll_view = ScrollView(size_hint=(1, None))
        scroll_view.bind(size=self.adjust_height)

        self.log_buttons_layout = BoxLayout(orientation='vertical')
        scroll_view.add_widget(self.log_buttons_layout)

        layout.add_widget(scroll_view)

        self.add_widget(layout)


    def process_file(self, selected_file):
        try:
                logs_dic, log_list = file_reader_new(selected_file)
                self.selected_file_label.text = f"Wybrany plik: {selected_file}"

                for i,log in enumerate(log_list):
                    button = Button(text= log, size_hint_y=None, height=40)
                    button.bind(on_press=lambda instance, index = i: self.log_button_pressed(instance, index))
                    self.log_buttons_layout.add_widget(button)
        except IOError:
            self.selected_file_label.text = "Wystapil blad podczas odczytu"

    def log_button_pressed(self, instance, index):
        print(index)

    def adjust_height(self, instance, height):
        self.log_buttons_layout.height=self.log_buttons_layout.minimum_height


class GUI(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(FileSelection(name='Select file'))
        screen_manager.add_widget(DisplayLogs(name='Logs'))

        return screen_manager


if __name__ == '__main__':
    GUI().run()
