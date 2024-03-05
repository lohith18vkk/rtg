from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3

class UserTypeScreen(Screen):
    def __init__(self, **kwargs):
        super(UserTypeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Welcome! Please select user type:', size_hint=(1, 0.5)))
        self.layout.add_widget(Button(text='Teacher', on_press=self.show_login_screen))
        self.layout.add_widget(Button(text='Student', on_press=self.show_student_screen))

    def show_login_screen(self, instance):
        self.manager.current = 'login'
        self.layout.add_widget(Button(text='Back to Home', on_press=self.back_to_home))

    def show_student_screen(self, instance):
        self.manager.current = 'student_login'

    def back_to_home(self, instance):
        self.manager.current = 'user_type'

class StudentLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(StudentLoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Welcome Student'))

        self.layout.add_widget(Button(text='Back to Home', on_press=self.back_to_home))

    def back_to_home(self, instance):
        self.manager.current = 'user_type'

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Username:'))
        self.username = TextInput(multiline=False)
        self.layout.add_widget(self.username)

        self.layout.add_widget(Label(text='Password:'))
        self.password = TextInput(password=True, multiline=False)
        self.layout.add_widget(self.password)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.layout.add_widget(self.error_label)

        self.layout.add_widget(Button(text='Login', on_press=self.login))
        self.layout.add_widget(Button(text='Signup', on_press=self.signup))
        self.layout.add_widget(Button(text='Back to Home', on_press=self.back_to_home))

    def login(self, instance):
        username = self.username.text
        password = self.password.text
        if self.check_credentials(username, password):
            self.error_label.text = ''
            self.manager.current = 'success'
        else:
            self.error_label.text = 'Invalid username or password'

    def check_credentials(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = c.fetchone()
        conn.close()
        return result is not None

    def signup(self, instance):
        self.manager.current = 'signup'

    def back_to_home(self, instance):
        self.manager.current = 'user_type'

class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Username:'))
        self.username = TextInput(multiline=False)
        self.layout.add_widget(self.username)

        self.layout.add_widget(Label(text='Password:'))
        self.password = TextInput(password=True, multiline=False)
        self.layout.add_widget(self.password)

        self.error_label = Label(text='', color=(1, 0, 0, 1))
        self.layout.add_widget(self.error_label)

        self.layout.add_widget(Button(text='Signup', on_press=self.register))
        self.layout.add_widget(Button(text='Back to Login', on_press=self.back_to_login))
        self.layout.add_widget(Button(text='Back to Home', on_press=self.back_to_home))

    def register(self, instance):
        username = self.username.text
        password = self.password.text
        if self.check_existing_username(username):
            self.error_label.text = 'Username already exists'
        else:
            self.add_user(username, password)
            self.error_label.text = 'Signup successful, please login'

    def check_existing_username(self, username):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )''')
        c.execute('SELECT * FROM users WHERE username=?', (username,))
        result = c.fetchone()
        conn.close()
        return result is not None

    def add_user(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

    def back_to_login(self, instance):
        self.manager.current = 'login'

    def back_to_home(self, instance):
        self.manager.current = 'user_type'

class SuccessScreen(Screen):
    def __init__(self, **kwargs):
        super(SuccessScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        self.layout.add_widget(Label(text='Login successful!'))

        self.layout.add_widget(Button(text='Logout', on_press=self.logout))
        self.layout.add_widget(Button(text='Back to Login', on_press=self.back_to_login))
        self.layout.add_widget(Button(text='Back to Home', on_press=self.back_to_home))

    def logout(self, instance):
        self.manager.current = 'login'

    def back_to_login(self, instance):
        self.manager.current = 'login'

    def back_to_home(self, instance):
        self.manager.current = 'user_type'

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(UserTypeScreen(name='user_type'))
        sm.add_widget(StudentLoginScreen(name='student_login'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(SuccessScreen(name='success'))
        return sm

if __name__ == '__main__':
    LoginApp().run()
