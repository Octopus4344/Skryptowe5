import os.path
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput

from zad_1 import file_reader


def show_error_popup(message):
    popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(400, 150))
    popup.open()


class FileSelection(Screen):
    def __init__(self, **kwargs):
        super(FileSelection, self).__init__(**kwargs)
        wrapper = BoxLayout(orientation='vertical')

        top_panel = BoxLayout(size_hint=(1, None), height=100)
        self.label = Label(text='Select SSH log file to analyze')
        top_panel.add_widget(self.label)
        wrapper.add_widget(top_panel)

        self.file_chooser = FileChooserListView()
        wrapper.add_widget(self.file_chooser)

        footer = BoxLayout(size_hint=(1, None), height=100)
        select_button = Button(text='Select', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1),
                               size_hint=(0.5, None))
        select_button.bind(on_press=self.get_log_file)
        footer.add_widget(select_button)
        wrapper.add_widget(footer)

        self.add_widget(wrapper)

    def get_log_file(self, instance):
        file = self.file_chooser.selection
        if file:
            file = file[0]
            self.manager.get_screen('Logs').process_file(file)
            self.manager.current = 'Logs'
        else:
            # TODO: change to popup
            # show_error_popup("No file selected")
            file = 'plik.txt'
            self.manager.get_screen('Logs').process_file(file)
            self.manager.current = 'Logs'


class DisplayLogs(Screen):
    def __init__(self, **kwargs):
        super(DisplayLogs, self).__init__(**kwargs)
        self.curr_index = 0
        self.logs = []

        self.layout = BoxLayout(orientation='vertical')

        self.top_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=100, spacing=50, padding=30)
        self.selected_file_label = Label(text='Current file: ')
        self.top_layout.add_widget(self.selected_file_label)
        self.return_button = Button(text='Back', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1), size=(100, 50),
                                    size_hint=(0.5, None))
        self.return_button.bind(on_press=self.choose_a_new_file)
        self.top_layout.add_widget(self.return_button)
        self.layout.add_widget(self.top_layout)

        self.filter_layout = BoxLayout(size_hint=(1, None), height=100)
        self.layout.add_widget(self.filter_layout)
        # tutaj będzie pokazane filtrowanie i przyciski do sterowania nim

        self.date_range_layout = BoxLayout(size_hint=(1, None), height=100, spacing=10, padding=30)
        self.start_date_input = TextInput(hint_text='Start Date (DD-MM)', multiline=False)
        self.end_date_input = TextInput(hint_text='End Date (DD-MM)', multiline=False)
        self.apply_filter_button = Button(text='Apply Filter', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1),
                                          size=(100, 50), size_hint=(0.5, None))
        self.apply_filter_button.bind(on_press=self.apply_date_filter)
        self.date_range_layout.add_widget(self.start_date_input)
        self.date_range_layout.add_widget(self.end_date_input)
        self.date_range_layout.add_widget(self.apply_filter_button)
        self.layout.add_widget(self.date_range_layout)

        self.logs_layout = GridLayout(cols=2, spacing=25, height=400)

        self.scroll_view_layout = BoxLayout(padding=10)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(300, 400), do_scroll_x=False, do_scroll_y=True)
        self.scroll_view.bind(size=self.adjust_height)

        self.log_buttons_layout = GridLayout(cols=1, spacing=3, size_hint_y=None)
        self.log_buttons_layout.bind(minimum_height=self.layout.setter('height'))
        self.scroll_view.add_widget(self.log_buttons_layout)
        self.scroll_view_layout.add_widget(self.scroll_view)

        self.detail_view = BoxLayout(orientation='vertical', height=400, padding=10)

        self.host_name_layout = BoxLayout(orientation='horizontal')
        self.hostname_key = Label(text='Hostname: ')
        self.hostname_value = Label()

        self.host_name_layout.add_widget(self.hostname_key)
        self.host_name_layout.add_widget(self.hostname_value)
        self.detail_view.add_widget(self.host_name_layout)

        #self.app_component_and_pid_layout = GridLayout(cols=2, spacing=1)

        self.app_component_layout = BoxLayout(orientation='horizontal')
        self.app_component_key = Label(text='App component:')
        self.app_component_value = Label()
        self.app_component_layout.add_widget(self.app_component_key)
        self.app_component_layout.add_widget(self.app_component_value)
        self.detail_view.add_widget(self.app_component_layout)

        self.pid_layout = BoxLayout(orientation='horizontal')
        self.pid_key = Label(text='PID: ')
        self.pid_value = Label()
        self.pid_layout.add_widget(self.pid_key)
        self.pid_layout.add_widget(self.pid_value)
        self.detail_view.add_widget(self.pid_layout)

        #self.detail_view.add_widget(self.app_component_and_pid_layout)

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
        self.previous_button = Button(text='Previous Log', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1),
                                      size_hint=(0.5, None))
        self.previous_button.bind(on_press=self.previous_log)
        self.bottom_layout.add_widget(self.previous_button)

        self.next_button = Button(text='Next Log', background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1),
                                  size_hint=(0.5, None))
        self.next_button.bind(on_press=self.next_log)
        self.bottom_layout.add_widget(self.next_button)

        self.add_widget(self.layout)

        with self.detail_view.canvas.before:
            Color(19/255, 53/255, 88/255, 1)
            self.detail_background=Rectangle(pos=(self.detail_view.x, self.detail_view.y), size =self.detail_view.size)

        self.detail_view.bind(size=self.update_detail_background, pos=self.update_detail_background)

    def process_file(self, selected_file):
        try:
            logs = file_reader(os.path.basename(selected_file))
            self.selected_file_label.text = f"Current file: {selected_file}"

            # try:
            #     start_date = datetime.strptime(start_date, '%d-%m')
            #     end_date = datetime.strptime(end_date, '%d-%m')
            # except ValueError:
            #     show_error_popup("Provide valid date in DD-MM format")

            # logs = [log for log in logs if start_date <= log['time'] <= end_date]

            self.logs = logs
            self.curr_index = 0

            for i, log in enumerate(logs):
                button = Button(text=log['content'][:45] + '...', size_hint_y=None, height=40,
                                background_color=(0.2, 0.6, 1, 1),
                                color=(1, 1, 1, 1))
                button.bind(on_press=lambda instance, index=i: self.log_button_pressed(instance, index))
                self.log_buttons_layout.add_widget(button)
            # self.update_dict()
        except IOError:
            self.selected_file_label.text = "An error occurred while reading the file"

    def log_button_pressed(self, instance, index):
        self.curr_index = index
        self.update_dict()

    def next_log(self, instance):
        if self.curr_index < len(self.logs) - 1:
            self.curr_index += 1
            self.update_dict()

    def previous_log(self, instance):
        if self.curr_index > 0:
            self.curr_index -= 1
            self.update_dict()

    def adjust_height(self, instance, height):
        self.log_buttons_layout.height = self.log_buttons_layout.minimum_height

    def update_dict(self):
        try:
            curr = self.logs[self.curr_index]
            self.hostname_value.text = curr['host_name']
            self.app_component_value.text = curr['app_component']
            self.pid_value.text = str(curr['PID'])
            if curr['IPv4']:
                self.ip_value.text = curr['IPv4'][0]
            else:
                self.ip_value.text = 'none'
            self.time_value.text = curr['time'].strftime('%d %B %H:%M:%S')
        except KeyError:
            show_error_popup('Unsupported log format')

    def choose_a_new_file(self, instance):
        self.manager.current = 'Select file'

    def apply_date_filter(self, instance):
        start_date_str = self.start_date_input.text.strip()
        end_date_str = self.end_date_input.text.strip()

        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%d-%m')
                end_date = datetime.strptime(end_date_str, '%d-%m')
                filtered_logs = [log for log in self.logs if start_date <= log['time'] <= end_date]
                self.update_logs_layout(filtered_logs)
            except ValueError:
                show_error_popup("Invalid date format. Please use DD-MM.")
        else:
            show_error_popup("Please provide both start and end dates.")

    def update_logs_layout(self, logs):
        self.log_buttons_layout.clear_widgets()
        for i, log in enumerate(logs):
            button = Button(text=log['content'][:45] + "...", size_hint_y=None, height=40, background_color=(0.2, 0.6, 1, 1),
                            color=(1, 1, 1, 1))
            button.bind(on_press=lambda instance, index=i: self.log_button_pressed(instance, index))
            self.log_buttons_layout.add_widget(button)
        self.curr_index = 0
        self.logs = logs
        if not logs:
            show_error_popup("No logs found in the selected date range.")

    def update_detail_background(self, instance, value):
        self.detail_view.y=self.scroll_view.y
        self.detail_background.pos=self.detail_view.x, self.detail_view.y
        self.detail_background.size=self.detail_view.size


class GUI(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(FileSelection(name='Select file'))
        screen_manager.add_widget(DisplayLogs(name='Logs'))
        return screen_manager


if __name__ == '__main__':
    GUI().run()
