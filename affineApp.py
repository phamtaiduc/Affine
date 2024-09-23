from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

# Set background color to golden yellow
from kivy.core.window import Window
Window.clearcolor = (1, 0.84, 0, 1)  # Màu vàng hoàng kim

def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(((a * (ord(char) - ord('A')) + b) % 26) + ord('A'))
            else:
                result += chr(((a * (ord(char) - ord('a')) + b) % 26) + ord('a'))
        else:
            result += char
    return result

def affine_decrypt(text, a, b):
    result = ""
    mod_inv_a = pow(a, -1, 26)
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr(((mod_inv_a * ((ord(char) - ord('A')) - b)) % 26) + ord('A'))
            else:
                result += chr(((mod_inv_a * ((ord(char) - ord('a')) - b)) % 26) + ord('a'))
        else:
            result += char
    return result

class AffineCipherApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title_label = Label(text="MÃ HÓA VÀ GIẢI MÃ", font_size=48, bold=True, color=(0, 0, 0, 1),
                            size_hint=(1, 0.2))
        main_layout.add_widget(title_label)

        middle_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.7))

        left_layout = GridLayout(cols=1, spacing=10, size_hint=(0.5, 1))

        self.input_text = TextInput(hint_text="Nhập tin nhắn", multiline=False, size_hint=(1, 0.3),
                                    background_color=(1, 1, 0.8, 1), padding=(10, 10), foreground_color=(0, 0, 0, 1))
        left_layout.add_widget(self.input_text)

        self.input_a = TextInput(hint_text="Nhập a", multiline=False, size_hint=(1, 0.3),
                                 background_color=(1, 1, 0.8, 1), padding=(10, 10), foreground_color=(0, 0, 0, 1))
        left_layout.add_widget(self.input_a)

        self.input_b = TextInput(hint_text="Nhập b", multiline=False, size_hint=(1, 0.3),
                                 background_color=(1, 1, 0.8, 1), padding=(10, 10), foreground_color=(0, 0, 0, 1))
        left_layout.add_widget(self.input_b)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

        self.output_text = TextInput(hint_text="Kết quả", readonly=True, size_hint=(1, 1),
                                     background_color=(1, 1, 0.8, 1), padding=(10, 10), foreground_color=(0, 0, 0, 1))
        right_layout.add_widget(self.output_text)

        middle_layout.add_widget(left_layout)
        middle_layout.add_widget(right_layout)

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        encrypt_button = Button(text="Mã hóa", background_color=(0.44, 0.44, 0.44, 1), color=(1, 1, 1, 1),
                                size_hint=(0.5, 1))
        encrypt_button.bind(on_press=self.start_encryption)
        button_layout.add_widget(encrypt_button)

        decrypt_button = Button(text="Giải mã", background_color=(0.44, 0.44, 0.44, 1), color=(1, 1, 1, 1),
                                size_hint=(0.5, 1))
        decrypt_button.bind(on_press=self.start_decryption)
        button_layout.add_widget(decrypt_button)

        main_layout.add_widget(middle_layout)
        main_layout.add_widget(button_layout)

        return main_layout

    def show_progress_popup(self, title):
        content = BoxLayout(orientation='vertical', padding=10)
        with content.canvas.before:
            Color(1, 0.84, 0, 1)  # Màu vàng hoàng kim
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self._update_rect, pos=self._update_rect)

        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=70, size_hint_x=1)  # Chiều rộng lớn hơn
        self.progress_bar.color = (0, 1, 0, 1)  # Màu xanh cho thanh tiến trình
        content.add_widget(self.progress_bar)

        popup = Popup(title=title, content=content, size_hint=(0.6, 0.2), background_color=(1, 1, 0, 0))  # Bỏ màu đen bên ngoài
        popup.open()
        return popup

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_progress(self, dt):
        if self.progress_bar.value < 100:
            self.progress_bar.value += 20  # Tăng thanh tiến trình
        else:
            self.popup.dismiss()  # Đóng popup khi hoàn tất

    def start_encryption(self, instance):
        self.popup = self.show_progress_popup("Đang mã hóa...")
        Clock.schedule_interval(self.update_progress, 1)  # Cập nhật tiến trình mỗi giây
        Clock.schedule_once(lambda dt: self.encrypt_message(instance), 5)  # Thực hiện mã hóa sau 5 giây

    def start_decryption(self, instance):
        self.popup = self.show_progress_popup("Đang giải mã...")
        Clock.schedule_interval(self.update_progress, 1)
        Clock.schedule_once(lambda dt: self.decrypt_message(instance), 5)

    def encrypt_message(self, instance):
        try:
            a = int(self.input_a.text)
            b = int(self.input_b.text)
            text = self.input_text.text
            encrypted_text = affine_encrypt(text, a, b)
            self.output_text.text = encrypted_text
        except ValueError:
            self.output_text.text = "Vui lòng nhập giá trị hợp lệ cho a và b."
        finally:
            self.popup.dismiss()  # Đóng popup khi hoàn thành

    def decrypt_message(self, instance):
        try:
            a = int(self.input_a.text)
            b = int(self.input_b.text)

            if a % 2 == 0:
                self.output_text.text = "Giá trị a phải là số nguyên lẻ."
                return
            if 26 % a == 0:
                self.output_text.text = "Giá trị a phải coprime với 26."
                return

            text = self.input_text.text
            decrypted_text = affine_decrypt(text, a, b)
            self.output_text.text = decrypted_text
        except ValueError:
            self.output_text.text = "Vui lòng nhập giá trị hợp lệ cho a và b."
        finally:
            self.popup.dismiss()  # Đóng popup khi hoàn thành

if __name__ == "__main__":
    AffineCipherApp().run()
