import os.path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from zad_1 import file_reader_new


class FileSelection(Screen):

    def __init__(self, **kwargs):
        super(FileSelection, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        top_layout = BoxLayout(size_hint=(1, None), height=100)

        self.label = Label(text='Select SSH log file to analyze')
        top_layout.add_widget(self.label)

        layout.add_widget(top_layout)

        self.file_chooser = FileChooserListView()
        layout.add_widget(self.file_chooser)

        bottom_layout = BoxLayout(size_hint=(1, None), height=100)
        select_button = Button(text='CONFIRM', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), size=(50, 50),
                               size_hint=(0.5, None))
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
            file = 'plik.txt'
            self.manager.get_screen('Logs').process_file(file)
            self.manager.current = 'Logs'
            # popup = Popup(title='Blad', content=Label(text='Nie wybrano żadnego pliku'),
            #               size_hint=(None, None), size=(200, 100))
            # popup.open()


class DisplayLogs(Screen):
    def __init__(self, **kwargs):
        super(DisplayLogs, self).__init__(**kwargs)
        self.curr_index = 0
        self.list_of_logs = []
        self.list_of_dics = []

        self.layout = BoxLayout(orientation='vertical')

        self.top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100, spacing=50, padding=30)
        self.selected_file_label = Label(text='Current file: ')
        self.top_layout.add_widget(self.selected_file_label)
        self.return_button = Button(text='BACK', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), size=(100, 50),
                                    size_hint=(0.5, None))
        self.return_button.bind(on_press=self.choose_a_new_file)
        self.top_layout.add_widget(self.return_button)
        self.layout.add_widget(self.top_layout)

        self.filter_layout = BoxLayout(size_hint=(1, None), height=100)
        self.layout.add_widget(self.filter_layout)
        # tutaj będzie pokazane filtrowanie i przyciski do sterowania nim

        self.logs_layout = GridLayout(cols=2, spacing=25, height=400)

        self.scroll_view_layout = BoxLayout(padding=10)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(300, 400), do_scroll_x=False, do_scroll_y=True)
        self.scroll_view.bind(size=self.adjust_height)

        self.log_buttons_layout = GridLayout(cols=1, spacing=3, size_hint_y=None)
        self.log_buttons_layout.bind(minimum_height=self.layout.setter('height'))
        self.scroll_view.add_widget(self.log_buttons_layout)
        self.scroll_view_layout.add_widget(self.scroll_view)

        self.detail_view = BoxLayout(orientation='vertical', height=400)

        self.host_name_layout = BoxLayout(orientation='horizontal')
        self.hostname_key = Label(text='Hostname: ')
        self.hostname_value = Label()
        # self.hostname_value.bind(size=self.hostname_value.setter('size'), pos=self.hostname_value.setter('pos'))
        # with self.hostname_value.canvas.before:
        #     Color(0.2, 0.6, 1, 1)
        #     Rectangle(pos=self.hostname_value.pos, size=self.hostname_value.size)

        self.host_name_layout.add_widget(self.hostname_key)
        self.host_name_layout.add_widget(self.hostname_value)
        self.detail_view.add_widget(self.host_name_layout)

        self.app_component_and_pid_layout = GridLayout(cols=2, spacing=3)

        self.app_component_layout = BoxLayout(orientation='horizontal')
        self.app_component_key = Label(text='App component: ')
        self.app_component_value = Label()
        self.app_component_layout.add_widget(self.app_component_key)
        self.app_component_layout.add_widget(self.app_component_value)
        self.app_component_and_pid_layout.add_widget(self.app_component_layout)

        self.pid_layout = BoxLayout(orientation='horizontal')
        self.pid_key = Label(text='PID: ')
        self.pid_value = Label()
        self.pid_layout.add_widget(self.pid_key)
        self.pid_layout.add_widget(self.pid_value)
        self.app_component_and_pid_layout.add_widget(self.pid_layout)

        self.detail_view.add_widget(self.app_component_and_pid_layout)

        self.ip_layout = BoxLayout(orientation='horizontal')
        self.ip_key = Label(text='IP address: ')
        self.ip_value = Label()
        self.ip_layout.add_widget(self.ip_key)
        self.ip_layout.add_widget(self.ip_value)
        self.detail_view.add_widget(self.ip_layout)

        self.time_layout = BoxLayout(orientation='horizontal')
        self.time_key = Label(text='Time: ')
        self.time_value = Label()
        self.time_layout.add_widget(self.time_key)
        self.time_layout.add_widget(self.time_value)
        self.detail_view.add_widget(self.time_layout)

        self.logs_layout.add_widget(self.scroll_view_layout)
        self.logs_layout.add_widget(self.detail_view)
        self.layout.add_widget(self.logs_layout)

        self.bottom_layout = BoxLayout(orientation='horizontal', height=300)
        self.layout.add_widget(self.bottom_layout)
        # to jest layout dp przycisków previous i next

        self.add_widget(self.layout)

    def process_file(self, selected_file):
        try:
            logs_dic, log_list = file_reader_new(os.path.basename(selected_file))
            self.selected_file_label.text = f"Current file: {selected_file}"
            self.list_of_logs = log_list
            self.list_of_dics = logs_dic
            self.curr_index = 0

            for i, log in enumerate(log_list):
                button = Button(text=log[:45] + "...", size_hint_y=None, height=40, background_color=(0.2, 0.6, 1, 1),
                                color=(1, 1, 1, 1))
                button.bind(on_press=lambda instance, index=i: self.log_button_pressed(instance, index))
                self.log_buttons_layout.add_widget(button)
            # self.update_dict()
        except IOError:
            self.selected_file_label.text = "An error occurred while reading the file"

    def log_button_pressed(self, instance, index):
        self.curr_index = index
        self.update_dict()

    def adjust_height(self, instance, height):
        self.log_buttons_layout.height = self.log_buttons_layout.minimum_height

    def update_dict(self):
        try:
            curr = self.list_of_dics[self.curr_index]
            self.hostname_value.text = curr['host_name']
            self.app_component_value.text = curr['app_component']
            self.pid_value.text = str(curr['PID'])
            if curr['IPv4']:
                self.ip_value.text = curr['IPv4'][0]
            else:
                self.ip_value.text = 'brak'
            self.time_value.text = curr['time'].strftime('%Y-%m-%d %H:%M:%S')
        except KeyError:
            popup = Popup(title='Error', content=Label(text='Not supported log format'),
                          size_hint=(None, None), size=(200, 100))
            popup.open()

    def choose_a_new_file(self, instance):
        # self.manager.get_screen('Select file').get_log_file
        self.manager.current = 'Select file'


class GUI(App):
    def build(self):
        screen_manager = ScreenManager()

        screen_manager.add_widget(FileSelection(name='Select file'))
        screen_manager.add_widget(DisplayLogs(name='Logs'))

        return screen_manager


if __name__ == '__main__':
    GUI().run()
