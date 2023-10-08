import kivy
import requests
import speech_recognition as sr
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import notification

class PCControlApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        nyala_button = Button(text='Nyala')
        matikan_button = Button(text='Matikan')
        rekam_suara_button = Button(text='Rekam Suara')  # Tambahan tombol rekam suara

        nyala_button.bind(on_release=self.turn_on_pc)
        matikan_button.bind(on_release=self.turn_off_pc)
        rekam_suara_button.bind(on_release=self.record_audio)  # Bind tombol rekam suara

        layout.add_widget(nyala_button)
        layout.add_widget(matikan_button)
        layout.add_widget(rekam_suara_button)  # Tambahan tombol rekam suara

        return layout

    def show_notification(self, message):
        notification.notify(
            title='Pemberitahuan',
            message=message,
            app_name='PC Control App'
        )

    def turn_on_pc(self, instance):
        response = requests.get("http://192.168.1.6:8085/short?key=nakumi")
        if response.status_code == 200:
            message = "Komputer telah dinyalakan."
            print(message)
            self.show_notification(message)
        else:
            message = "Gagal mengirim perintah ke module."
            print(message)

    def turn_off_pc(self, instance):
        response = requests.get("http://192.168.1.6:8085/long?key=nakumi")
        if response.status_code == 200:
            message = "Komputer telah dimatikan."
            print(message)
            self.show_notification(message)
        else:
            message = "Gagal mengirim perintah untuk mematikan komputer."
            print(message)

    def record_audio(self, instance):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Silakan ucapkan perintah Anda...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("Anda mengatakan: " + command)
            self.handle_voice_command(command)
        except sr.UnknownValueError:
            print("Maaf, saya tidak bisa mengenali suara Anda.")
        except sr.RequestError as e:
            print("Error dalam mengambil data suara: {0}".format(e))

    def handle_voice_command(self, command):
        if "nyala" in command:
            self.turn_on_pc(None)
        elif "matikan" in command:
            self.turn_off_pc(None)
        else:
            print("Perintah tidak dikenali: " + command)

if __name__ == '__main__':
    PCControlApp().run()
