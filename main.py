import kivy
import requests
import speech_recognition as sr
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import notification  # Mengimpor modul notifikasi dari plyer

class PCControlApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        nyala_button = Button(text='Nyala')
        matikan_button = Button(text='Matikan')

        nyala_button.bind(on_release=self.turn_on_pc)
        matikan_button.bind(on_release=self.turn_off_pc)

        layout.add_widget(nyala_button)
        layout.add_widget(matikan_button)

        return layout

    def show_notification(self, message):
        # Menampilkan pemberitahuan pada perangkat Android
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

if __name__ == '__main__':
    PCControlApp().run()