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
        return "action_imprimir_determinantes"
        
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #contenidos:
        #figura humana completa
        _H = {"persona","humano","hombre","mujer","niño","niña","chico","chica","señor","señora","personas","humanos","hombres","mujeres","niños","niñas","chicos","chicas","señores","señoras"}
        #figura humana completa irreal, de ficción o mitológica
        _ParentesisH = {"payaso","payasos","hada","hadas","bruja","brujas","fantasma","fantasmas","enano","enanos","enana","enanas","demonio","demonios","ángel","ángeles","humanoide","humanoides","caricaturas","caricatura","monstruo","monstruos","duende","duendes"}
        #Detalle humano
        #self._Hd = {        
        #Experiencia humana
        _Hx = {"amor","amar","ama","amamos","amo","odio","odia","odiamos","odiar","depresión","deprimido","deprimida","deprimidos","deprimidas","feliz","felices","alegre","alegres","felicidad","alegria","ruido","ruidoso","sonido","suena","olor","huele","oloroso","miedo","temor","miedoso","contento","contenta","contentos","contentas"}
        #Figura animal completa
        _A = {"escarabajo","escarabajos","bicho","bichos","araña","arañas","cucaracha","cucarachas","mariposa","mariposas","mantis","mosca","mosquito","moscas","mosquitos","pulga","pulgas","águila","águilas","avestruz","ballena","bisonte","búfalo","búhos","buitre","burro","caballo","cabra","camaleón","camello","canario","castor","cebra","cerdo","chancho","ciervo","cobra","colibrí","comadreja","cóndor","conejo","delfín","elefante","faisan","flamenco","foca","gallina","gallo","gato","gorila","guepardo","hámster","hiena","hipopótamo","jabalí","jaguar","jirafa","koala","lagarto","león","llama","lobo","loro","manatí","mapache","mono","murciélago","nutria","ñandú","orcas","oso","pájaro","paloma","panda","pato","pavo","pelícano","perro","pingüino","puercoespín","puma","rana","ratón","reno","rinoceronte","salamandra","sapo","serpiente","tapir","tejon","tiburón","tigre","topo","toro","tucán","vaca","vicuña","zorrino","zorro","águila","avestruces","ballenas","bisontes","búfalos","búho","buitres","burros","caballos","cabras","camaleones","camellos","canarios","castores","cebras","cerdos","chanchos","ciervos","cobras","colibries","comadrejas","cóndores","conejos","delfines","elefantes","faisanes","flamencos","focas","gallinas","gallos","gatos","gorilas","guepardos","hámsters","hienas","hipopótamos","jabalies","jaguares","jirafas","koalas","lagartos","leones","llamas","lobos","loros","manaties","mapaches","monos","murciélagos","nutrias","ñandues","orca","osos","pájaros","palomas","pandas","patos","pavos","pelícanos","perros","pingüinos","puercoespines","pumas","ranas","ratones","renos","rinocerontes","salamandras","sapos","serpientes","tapires","tiburones","tigres","topos","toros","tucanes","vacas","víbora","víboras","vicuñas","zorrinos","zorros"}
        
        slot_paridad = tracker.get_slot("par")
        slot_vista = tracker.get_slot("vista")
        slot_ccromatico = tracker.get_slot("color_cromatico")
        slot_cacromatico = tracker.get_slot("color_acromatico")
        slot_forma = tracker.get_slot("forma")
        slot_movimiento = tracker.get_slot("movimiento")
        slot_textura = tracker.get_slot("textura")
        slot_reflejo = tracker.get_slot("reflejo")       
        respuesta = tracker.latest_message['text']
        while _H:
            s = _H.pop()
            if s in respuesta:
                dispatcher.utter_message(text="Hay figura humana completa")        
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
        
        ############################# ESTO LO AGREGO BELEN ##############################
        # Lo que hace es mostrar el mensaje con la próxima imagen: utter_Lamina2 ó utter_Lamina3
        next_response = tracker.get_slot("response")
        if next_response != "None":
            dispatcher.utter_message(response=next_response)  

        ############## (tambien setee el slot al final del return con "None") ############

        return [SlotSet("par","false"),SlotSet("vista","false"),SlotSet("color_cromatico","false"),SlotSet("color_acromatico","false"),SlotSet("forma","false"),SlotSet("movimiento","false"),SlotSet("textura","false"),SlotSet("reflejo","false"),SlotSet("response", "None")]

