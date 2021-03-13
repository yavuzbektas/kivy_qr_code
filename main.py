
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
import sqlite3,time
from PIL import Image as pImage

from pyzbar import pyzbar
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    
    BoxLayout:
        orientation:'vertical'
        spacing:3
        padding:([20,20,20,20])
        
        Button:
            text: 'Ayarlar'
            color:'white'
            size_hint: (.3, .3)
            background_color:'yellow'
            on_press: root.manager.current = 'settings'
        Button:
            text: 'Giris Sayfası'
            color:'white'
            size_hint: (.3, .3)
            background_color:'blue'
            on_press: root.manager.current = 'login'
        Button:
            color:'white'
            size_hint: (.3, .3)
            background_color:'grey'
            text: 'Çıkış'
            on_press:app.stop()
<SearchScreen>:
    id:search
    FloatLayout:
        Button:
            text: 'Geri'
            size_hint: (.1, .1)
            pos_hint:{'x':.9,'y':.9}
            on_press: root.manager.current = 'menu'
        GridLayout:
            size_hint: (0.5, 0.5)
            
            height: 25
            cols: 2
            Image:
                id: resim
                source:''
            Widget:
                id:widget
            Label:
                text: "Oda"
                id:lb_oda
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:oda_adi
                text:oda_adi.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "Dolap"
                id:lb_dolap
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:dolap_adi
                text:dolap_adi.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "Raf"
                id:lb_raf
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:raf_adi
                text:raf_adi.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "stok"
                id:lb_stok
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:stok_kod
                text:stok_kod.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "Mevcut"
                id:lb_mevcut
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:mevcut_adet
                text:mevcut_adet.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "kullan"
                id:lb_kullan
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:kullan_adet
                text:kullan_adet.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Button:
                text        : 'Ara'
                id          : btn_ara
                size_hint   : (.3, .1)
                pos_hint    : {'x':.5,'y':.4}
                on_press    : root.image_change(btn_ara)
        GridLayout:
            size_hint: (0.5, 0.5)
            pos_hint    : {'x':.5,'y':.5}
            height: 25
            cols: 1
            Camera:
                id: camera
                resolution: (640, 480)
                play: False
            Widget:
                id:widget
            ToggleButton:
                text: 'Play'
                on_press: camera.play = not camera.play
                size_hint_y: None
                height: '48dp'
            Button:
                text: 'Capture'
                size_hint_y: None
                height: '48dp'
                on_press: root.capture()
<LoginScreen>:
    id:login
    username:username
    password:password
    FloatLayout:
        Button:
            text: 'Geri'
            size_hint: (.1, .1)
            pos_hint:{'x':.9,'y':.9}
            on_press: root.manager.current = 'menu'
        GridLayout:
            size_hint: (0.5, 0.5)
            
            height: 25
            cols: 2
            
            Label:
                text: "KULLANICI"
                id:lb_username
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:username
                text:username.text
                size_hint: (.5, None)
                height: 30
                multiline: False
            Label:
                text: "SIFRE"
                id:lb_password
                size_hint: (.5, None)
                height: 30
            TextInput:
                id:password
                text:password.text
                size_hint: (.5, None)
                height: 30
                multiline: False
                password:True
    
        Button:
            text        : 'Giris'
            id          : btn_login
            size_hint   : (.3, .1)
            pos_hint    : {'x':.5,'y':.4}
            on_press    : root.check_user(btn_login)
<SettingsScreen>:
    FloatLayout:
        Button:
            text: 'Geri'
            size_hint: (.1, .1)
            pos_hint:{'x':.9,'y':.9}
            on_press: root.manager.current = 'menu'
    BoxLayout:
       
        Button:
            text: 'Giris Sayfası'
            on_press: root.manager.current = 'login'
        Button:
            text: 'Ana Menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    pass
class LoginScreen(Screen):
    #btn_login = ObjectProperty(None)
    #username=ObjectProperty(None)
    #password=ObjectProperty(None)
    
    def check_user(self,instance):
        conn = sqlite3.connect('C:\\Users\\aliyi\\Documents\\.venv\\myproject\\kivy\\myapp\\stockDB')
        with conn:
            cur = conn.cursor()
            query = ("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(self.username.text,self.password.text))
            cur.execute(query)
            data = cur.fetchall()
            
            if data!=[]:
                print("kullanıcı girisi basarılı")
                self.parent.current='search'
            else:
                print("kullanıcı girisi HATALI")
class SettingsScreen(Screen):
    pass

class SearchScreen(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        img_name="QR_code.png"
        camera.export_to_png(img_name)
        self.ids['resim'].source=img_name
        try:
            barcode=pyzbar.decode(pImage.open(img_name))
            print(barcode)
        except:
            print('resim Hatalı')
        if barcode!=[]:
            code=barcode[0][0].decode("utf-8")
            
            self.search_stock_code(code)
            print("Captured")
        else:
            
            print("Resim içersinde BArkod okunamadı. Tekrar deneyiniz")
    def search_stock_code(self,code):
        conn = sqlite3.connect('C:\\Users\\aliyi\\Documents\\.venv\\myproject\\kivy\\myapp\\stockDB')
        with conn:
            cur = conn.cursor()
            query = ("SELECT * FROM stock WHERE code = '{}'".format(code))
            cur.execute(query)
            data = cur.fetchone()
            
            if data!=[]:
                print("Arama Tamamlandı ve kayıt getirildi")
                self.ids['stok_kod'].text=code
                
                self.ids['oda_adi'].text=code.split("-")[2]
                self.ids['raf_adi'].text=code.split("-")[3]+code.split("-")[4]
                self.ids['dolap_adi'].text=code.split("-")[5]+code.split("-")[6]
                self.ids['kullan_adet'].text=""
                self.ids['mevcut_adet'].text=str(data[4])
            else:
                print("kullanıcı girisi HATALI")
    def image_change(self,instance):
        self.ids['resim'].source='tex3.jpg'
        self.ids['oda_adi'].text="MD"
        self.ids['raf_adi'].text="RF3"
        self.ids['dolap_adi'].text="CB2"
        self.ids['stok_kod'].text="STK-123-MD-CB2-RF3"
class TestApp(App):

    def build(self):
        # Create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SearchScreen(name='search'))
        return self.sm

if __name__ == '__main__':
    TestApp().run()