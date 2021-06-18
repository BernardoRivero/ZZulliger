# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,AllSlotsReset
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class imprimirSlot(Action):
    def name(self) -> Text:
        return "action_imprimir_slot"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_paridad = tracker.get_slot("par")
        slot_vista = tracker.get_slot("vista")
        slot_ccromatico = tracker.get_slot("color_cromatico")
        slot_cacromatico = tracker.get_slot("color_acromatico")
        slot_forma = tracker.get_slot("forma")
        slot_movimiento = tracker.get_slot("movimiento")
        slot_textura = tracker.get_slot("textura")
        slot_reflejo = tracker.get_slot("reflejo")
        ##slot_insecto = tracker.get_slot("insecto")
        sender = tracker.sender_id
        if slot_paridad == "true":
            dispatcher.utter_message(text="Hay par")
        else:
            dispatcher.utter_message(text="No hay par")
        if slot_vista == "true":
            dispatcher.utter_message(text="Hay vista")
        else:
            dispatcher.utter_message(text="No hay vista")
        if slot_ccromatico == "true":
            dispatcher.utter_message(text="Hay color cromático")
        else:
            dispatcher.utter_message(text="No hay color cromático")
        if slot_cacromatico == "true":
            dispatcher.utter_message(text="Hay color acromático")
        else:
            dispatcher.utter_message(text="No hay color acromático")
        if slot_forma == "humana":
            dispatcher.utter_message(text="Hay forma humana")
        else:
            if slot_forma == "animal":
                dispatcher.utter_message(text="Hay forma animal")
            else:
                if slot_forma == "inanimada":
                    dispatcher.utter_message(text="Hay forma inanimada")
                else:
                    dispatcher.utter_message(text="No hay forma")
        if slot_movimiento == "true" and slot_forma == 'humana':
            dispatcher.utter_message(text="Hay movimiento humano M")
        else:
            if slot_movimiento == "true" and slot_forma == 'inanimada':
                dispatcher.utter_message(text="Hay movimiento inanimado m")
            else:
                dispatcher.utter_message(text="Hay movimiento indefinido")
        if slot_textura == "true":
            dispatcher.utter_message(text="Hay textura")
        else:
            dispatcher.utter_message(text="No hay textura") 
        if slot_reflejo == "true":
            dispatcher.utter_message(text="Hay reflejo")
        else:
            dispatcher.utter_message(text="No hay reflejo")    
        return [SlotSet("par","false"),SlotSet("vista","false"),SlotSet("color_cromatico","false"),SlotSet("color_acromatico","false"),SlotSet("forma","false"),SlotSet("movimiento","false"),SlotSet("textura","false"),SlotSet("reflejo","false")]

