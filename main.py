from turtle import down
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
import requests
import json
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class HomeScreen(Screen):
    pass
class BmiScreen(Screen):
    pass
class BmrScreen(Screen):
    pass
class IbwScreen(Screen):
    pass
class CustomDropDown(DropDown):
    pass
class LabelButton(ButtonBehavior, Label):
    pass
class SummaryScreen(Screen):
    pass
class DietPlanScreen(Screen):
    pass
class WorkoutScreen(Screen):
    pass



GUI = Builder.load_file("main.kv")

class MainApp(App):

    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    #Realtime database
    #firebase_url = "https://vfit-demo-default-rtdb.firebaseio.com/users/.json"
    
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition
        screen_manager.current = screen_name
    
    def checkbox_click(self, value, gender):
        self.manOrwoman = ''
        if value == "down":
            self.manOrWoman = gender
        
    def calculate_bmi(self, height, weight):
        #if self.manOrWoman == Null:
            
        kg = int(weight)
        m = int(height)/100
        bmi = kg/(m*m)
        bmi = round(bmi, 1)
        self.weight_status = ""
        if bmi<18.5:
            self.weight_status = "Underweight"
        elif bmi>=18.5 and bmi<=25:
            self.weight_status = "Healthy Weight"
        elif bmi>=25.5 and bmi<=29.9:
            self.weight_status = "Overweight"
        else:
            self.weight_status = "Obesity"

        
        time_now=datetime.datetime.now()
        self.data_time = time_now.strftime('%m_%d_%Y_%H_%M_%S')
        
        #Realtime database
        #json_data = {user: {bmi_time: {"gender": self.manOrWoman, "height": height, "weight": weight, "bmi": bmi,
        #"weight_status": self.weight_status}}}
        #res = requests.patch(url=self.firebase_url, json=json_data)
        #print(res)

        
        #Use "add" to create documents with auto ID
        #self.db.collection("users").add({"bmi_time": self.bmi_time, "gender":self.manOrWoman, 
        #"height":height, "weight":weight, "bmi":bmi, "weight_status": self.weight_status})

        #Use "set" to create documents with custom ID
        try:
            self.db.collection("users").document(f"sirka_{self.data_time}").update({"data_time": self.data_time, "gender":self.manOrWoman, 
            "height":height, "weight":weight, "bmi":bmi, "weight_status": self.weight_status})
        except:
            self.db.collection("users").document(f"sirka_{self.data_time}").set({"data_time": self.data_time, "gender":self.manOrWoman, 
            "height":height, "weight":weight, "bmi":bmi, "weight_status": self.weight_status})

        #Printing BMI results
        self.root.ids["bmi_screen"].ids["user_bmi"].text = str(bmi)
        self.root.ids["bmi_screen"].ids["weight_status"].text = str(self.weight_status)

        #Disabling the widgets
        self.root.ids["bmi_screen"].ids["weight"].disabled = False
        self.root.ids["bmi_screen"].ids["height"].disabled = False
        self.root.ids["bmi_screen"].ids["calculate_btn"].disabled = True
        self.root.ids["bmi_screen"].ids["male"].disabled = True
        self.root.ids["bmi_screen"].ids["female"].disabled = True

        #Passing data to ibw_screen
        if self.manOrWoman == "male":
            self.root.ids["ibw_screen"].ids["male"].state = "down"
        else:
            self.root.ids["ibw_screen"].ids["female"].state = "down"

        self.root.ids["ibw_screen"].ids["male"].disabled = True
        self.root.ids["ibw_screen"].ids["female"].disabled = True

        self.root.ids["ibw_screen"].ids["height"].text = height
        self.root.ids["ibw_screen"].ids["height"].disabled = True
        self.root.ids["ibw_screen"].ids["weight"].text = weight
        self.root.ids["ibw_screen"].ids["weight"].disabled = True


        #Passing data to bmr_screen
        if self.manOrWoman == "male":
            self.root.ids["bmr_screen"].ids["male"].state = "down"
        else:
            self.root.ids["bmr_screen"].ids["female"].state = "down"

        self.root.ids["bmr_screen"].ids["male"].disabled = True
        self.root.ids["bmr_screen"].ids["female"].disabled = True

        self.root.ids["bmr_screen"].ids["height"].text = height
        self.root.ids["bmr_screen"].ids["height"].disabled = True
        self.root.ids["bmr_screen"].ids["weight"].text = weight
        self.root.ids["bmr_screen"].ids["weight"].disabled = True

        #Passing data to summary_screen
        self.root.ids["summary_screen"].ids["gender"].text = self.manOrWoman
        self.root.ids["summary_screen"].ids["weight"].text = "{0} Kg".format(weight)
        self.root.ids["summary_screen"].ids["height"].text = "{0} cm".format(height)
        self.root.ids["summary_screen"].ids["bmi"].text = "{0}".format(bmi)

    def calculate_ibw(self, height, weight):
        kg = int(weight)
        if self.manOrWoman == "male":
            ibw = 50+(0.91*(int(height)-152.4))
            if ibw < int(weight):
                usr_suggestion = int(weight) - ibw
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = f"You need to LOOSE at least {round(usr_suggestion, 2)} kg to reach ideal weight."
            elif ibw > int(weight):
                usr_suggestion = ibw-int(weight)
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = f"You need to GAIN at least {round(usr_suggestion, 2)} kg to reach ideal weight."
            else:
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = "You have a perfecf body weight. Good job!"
        else:
            ibw = 45.5+(0.91*(int(height)-152.4))
            if ibw < int(weight):
                usr_suggestion = int(weight) - ibw
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = f"You need to LOOSE at least {round(usr_suggestion, 2)} kg to reach ideal weight."
            elif ibw > int(weight):
                usr_suggestion = ibw-int(weight)
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = f"You need to GAIN at least {round(usr_suggestion, 2)} kg to reach ideal weight."
            else:
                self.root.ids["ibw_screen"].ids["usr_suggestion"].text = "You have a perfect body weight. Good job!"

        #Printing IBW results
        self.root.ids["ibw_screen"].ids["user_iwr"].text = str(round(ibw, 2))

        #Disabling the widgets
        self.root.ids["ibw_screen"].ids["weight"].disabled = True
        self.root.ids["ibw_screen"].ids["height"].disabled = True
        self.root.ids["ibw_screen"].ids["calculate_btn"].disabled = True
        self.root.ids["ibw_screen"].ids["male"].disabled = True
        self.root.ids["ibw_screen"].ids["female"].disabled = True

        #Passing Data to summary_screen
        self.root.ids["summary_screen"].ids["ibw"].text = "{0} Kg".format(ibw)

        #Adding IBW data into database
        try:
            self.db.collection("users").document(f"sirka_{self.data_time}").update({"ibw": round(ibw, 2)})
        except:
            time_now=datetime.datetime.now()
            self.data_time = time_now.strftime('%m_%d_%Y_%H_%M_%S')
            self.db.collection("users").document(f"sirka_{self.data_time}").set({"data_time": self.data_time, "ibw": round(ibw, 2)})


    def calculate_bmr(self, weight, height, age):
        kg = int(weight)
        cm = int(height)
        age = int(age)
        if self.manOrWoman == "male":
            bmr = 66.47+13.75*kg+5*cm-6.8*age
        else:
            bmr = 66.5+9.6*kg+1.8*cm-4.7*age
        
        #Printing BMR results
        self.root.ids["bmr_screen"].ids["user_bmr"].text = str(round(bmr, 2))

        #passing data to summary_screen
        self.root.ids["summary_screen"].ids["bmr"].text = "{0} kcal".format(bmr)
        self.root.ids["summary_screen"].ids["age"].text = "{0} Yrs".format(age)

        #Disabling the widgets
        self.root.ids["bmr_screen"].ids["weight"].disabled = True
        self.root.ids["bmr_screen"].ids["height"].disabled = True
        self.root.ids["bmr_screen"].ids["age"].disabled = True
        self.root.ids["bmr_screen"].ids["calculate_btn"].disabled = True
        self.root.ids["bmr_screen"].ids["male"].disabled = True
        self.root.ids["bmr_screen"].ids["female"].disabled = True

        #Adding BMR data into database
        try:
            self.db.collection("users").document(f"sirka_{self.data_time}").update({"bmr": round(bmr, 2)})
        except:
            time_now=datetime.datetime.now()
            self.data_time = time_now.strftime('%m_%d_%Y_%H_%M_%S')
            self.db.collection("users").document(f"sirka_{self.data_time}").set({"data_time": self.data_time, "bmr": round(bmr, 2)})


MainApp().run()