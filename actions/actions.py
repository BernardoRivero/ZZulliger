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
        #1 figura humana completa
        _H = {"persona","humano","hombre","mujer","niño","niña","chico","chica","señor","señora","personas","humanos","hombres","mujeres","niños","niñas","chicos","chicas","señores","señoras"}
        #2 figura humana completa irreal, de ficción o mitológica
        _ParentesisH = {"payaso","payasos","hada","hadas","bruja","brujas","fantasma","fantasmas","enano","enanos","enana","enanas","demonio","demonios","ángel","ángeles","humanoide","humanoides","caricaturas","caricatura","monstruo","monstruos","duende","duendes"}
        #3 Detalle humano
        _Hd = {"brazo","pierna","dedos","pies","cabeza","codo","nariz"}        
        #5 Experiencia humana
        _Hx = {"amor","amar","ama","amamos","amo","odio","odia","odiamos","odiar","depresión","deprimido","deprimida","deprimidos","deprimidas","feliz","felices","alegre","alegres","felicidad","alegria","ruido","ruidoso","sonido","suena","olor","huele","oloroso","miedo","temor","miedoso","contento","contenta","contentos","contentas"}
        #6 Figura animal completa
        _A = {"escarabajo","escarabajos","bicho","bichos","araña","arañas","cucaracha","cucarachas","mariposa","mariposas","mantis","mosca","mosquito","moscas","mosquitos","murcielago","murciélago","murciélagos","pulga","pulgas","águila","águilas","avestruz","ballena","bisonte","búfalo","búhos","buitre","burro","caballo","cabra","camaleón","camello","canario","castor","cebra","cerdo","chancho","ciervo","cobra","colibrí","comadreja","cóndor","conejo","delfín","elefante","faisan","flamenco","foca","gallina","gallo","gato","gorila","guepardo","hámster","hiena","hipopótamo","jabalí","jaguar","jirafa","koala","lagarto","león","lobo","loro","manatí","mapache","mono","murciélago","nutria","ñandú","orcas","oso","pájaro","paloma","panda","pato","pavo","pelícano","perro","pingüino","puercoespín","puma","rana","ratón","reno","rinoceronte","salamandra","sapo","serpiente","tapir","tejon","tiburón","tigre","topo","toro","tucán","vaca","vicuña","zorrino","zorro","águila","avestruces","ballenas","bisontes","búfalos","búho","buitres","burros","caballos","cabras","camaleones","camellos","canarios","castores","cebras","cerdos","chanchos","ciervos","cobras","colibries","comadrejas","cóndores","conejos","delfines","elefantes","faisanes","flamencos","focas","gallinas","gallos","gatos","gorilas","guepardos","hámsters","hienas","hipopótamos","jabalies","jaguares","jirafas","koalas","lagartos","leones","lobos","loros","manaties","mapaches","monos","murciélagos","nutrias","ñandues","orca","osos","pájaros","palomas","pandas","patos","pavos","pelícanos","perros","pingüinos","puercoespines","pumas","ranas","ratones","renos","rinocerontes","salamandras","sapos","serpientes","tapires","tiburones","tigres","topos","toros","tucanes","vacas","víbora","víboras","vicuñas","zorrinos","zorros"}
        #7 Figura animal completa irreal, de ficción o mitológica
        _ParentesisA = {"unicornio","unicornios","dragón","dragon","dragones","minotauro","minotauros"}
        #8 Figura animal incompleta
        _Ad = {"pata","patas","cola","pinza","hocico", "cuero","pezuñas","garras","vasos","pico"}
        #10 Anatomía
        _An = {"ósea","osea","cráneo","cráneo","torax","toracica","tórax","corazón","corazon","pulmón","pulmon","estomágo","estomago","panza","hígado","higado","musculo","articulaciones","vértebral","vértebra","vertebras","cerebro","cerebros"}
        #11 Arte
        _Art = {"pintura","dibujo","pinturas","dibujos","ilustración","ilustracion","ilustraciones","acuarela","acuarelas","arte","estatua","estatuas","escultura","esculturas","joya","joyas","insignia","insignias","escudo","escudos","adornos","espada","espadas","cuadros","lienzos","cuadro","lienzo"}
        #13 Sangre
        _Bl = {"sangre","sanguíneo","sanguínea","sanguinario","sanguinaria","sangriento","sangrienta"}
        #14 Botánica
        _Bt = {"vegetal","vegetales","arbusto","arbustos","flor","flores","floral","alga","algas","arbol","árbol","árboles","arboles","hoja","hojas","pétalo","pétalos","tronco","tronco","raiz","raíces","nido","hongo","hongos","pino","palmera","pinos","palmeras"} 
        #15 Vestidos
        _Cg = {"sombrero","sombreros","gorro","gorros","gorras","gorra","bota","botas","botines","cinturón","cinturon","cinturones","corbata","corbatas","moño","moños","chaqueta","chaquetas","saco","sacos","polera","poleras","pantalón","pantalon","pantalones","bufanda","bufandas","bermudas","short","shorts","medias","calzoncillos","musculosa"}
        #16 Nubes
        _Cl = {"nubes","nube","nubarrón","nubarrones","nublado","nublada"}
        #17 Explosión
        _Ex = {"explosión","explosión","explotar","implotar","bomba","explosivos","estallido","estallidos","detonación","detonaciones","bombardeo","bombardeos"}
        #18 Fuego
        _Fi = {"fuego","fuegos","llama","llamas","incendio","incendios","humo","humos","fogata","fogatas","chispa","chispas","hoguera","hogueras","quema","quemas"}
        #19 Comida
        _Fd = {"pollo","pollos","carne","carnes","pescado","pescados","helado","helados","panqueque","panqueques","verdura","verduras","papa","papas","zapallo","zapallos","lechuga","lechugas","tomates","tomate","zanahoria","zanahorias","sandía","sandías","melón","melones","kiwi","kiwis","mandarina","naranja","mandarinas","naranjas","banana","bananas","palta","frutas","verdura","fruta","torta","budín","tostadas","sandwich","sandwiches","pan","panes","sopa","pasta","sopas","pastas","spaghetti"}
        #20 Geografía
        _Ge = {"mapa","mapas","plano","planos","cartográfico","cartografía","continente","continentes","país","paises","ciudad","ciudad","region","regiones"}
        #21 Hogar
        _Hh = {"cama","cucheta","sommier","sillón","silla","mesa","lámpara","cuchillo","olla","alfombra","cortina","mueble","horno","cocina","pieza","habitación","baño","cochera","garage","camas","cuchetas","sommiers","sillones","sillas","mesas","lámparas","cuchillos","ollas","alfombras","cortinas","muebles","hornos","cocinas","piezas","habitaciones","baños","cocheras"}
        #22 Paisaje
        _Ls = {"montaña","montañas","cordillera","cordilleras","colina","colinas","cerro","cerros","sierra","sierras","isla","islas","cueva","cuevas","roca","rocas","piedra","piedras","bosque","bosques","desierto","desierto","llanura","llanuras","pantano","pantanos","glaciar","glaciares"}
        #23 Naturaleza
        _Na = {"lago","laguna","lagos","lagunas","sol","luna","mar","mar","océano","océanos","agua","hielo","hielos","lluvia","lluvias","niebla","neblina","bruma","tormenta","brisa","viento","arco iris","tormenta","noche","día","dia","granizo","trueno","relámpago","relampago"}
        #24 Ciencia
        _Sc = {"avión","aviones","avion","edificio","edificios","puente","puentes","auto","autos","moto","motos","microscopio","microscopios","laboratorio","laboratorios","motor","motores","turbina","turbinas","telescopio","telescopios","arma","armas","armamento","cohete","cohetes","nave","naves","ovni","OVNI","ovnis","OVNIS","barco","barcos","antena","antenas","satélite","satélites","satelite","satelites"}
        #25 Sexo
        _Sx = {"pene","penes","verga","vergas","pito","pitos","vagina","vaginas","concha","conchas","nalgas","cachas","pechos","teta","tetas","testículos","huevos","bolas","menstruación","aborto","abortar","coito","coger","garchar","cogiendo","teniendo sexo","garchando"}
        #26 Radiografía
        _Xy = {"radiografía","radiografia","placa","placas","rayos x"}
        #27 Popular1
        _Po1 = {"escarabajo","escarabajos","bicho","bichos","araña","arañas","cucaracha","cucarachas","mariposa","mariposas","mantis","mosca","mosquito","moscas","mosquitos","insecto","insectos","gusano"}
        #28 Popular3
        _Po3 = {"persona","humano","hombre","mujer","niño","niña","chico","chica","señor","señora","personas","humanos","hombres","mujeres","niños","niñas","chicos","chicas","señores","señoras","payaso","payasos","hada","hadas","bruja","brujas","fantasma","fantasmas","enano","enanos","enana","enanas","demonio","demonios","ángel","ángeles","humanoide","humanoides","caricaturas","caricatura","monstruo","monstruos","duende","duendes"}
        #IMAGEN 2 NO TIENE RESPUESTAS POPULARES

        slot_paridad = tracker.get_slot("par")
        slot_vista = tracker.get_slot("vista")
        slot_ccromatico = tracker.get_slot("color_cromatico")
        slot_cacromatico = tracker.get_slot("color_acromatico")
        slot_forma = tracker.get_slot("forma")
        slot_movimiento = tracker.get_slot("movimiento")
        slot_textura = tracker.get_slot("textura")
        slot_reflejo = tracker.get_slot("reflejo")       
        respuesta = tracker.latest_message['text']
        dispatcher.utter_message(text="CONTENIDOS:")
        while _H:#1
            subconjunto = _H.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay figura humana completa(contenido)")        
                #agregar setear un slot en true para usar al final
        while _ParentesisH:#2
            subconjunto = _ParentesisH.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay figura completa irreal, de ficción o mitológica(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Hd: #3
            subconjunto = _Hd.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay detalle humano(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Hx: #5
            subconjunto = _Hx.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay experiencia humana(contenido)")        
                #agregar setear un slot en true para usar al final
        while _A: #6
            subconjunto = _A.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay figura animal completa(contenido)")        
                #agregar setear un slot en true para usar al final
        while _ParentesisA: #7
            subconjunto = _ParentesisA.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay figura animal completa irreal, de ficción o mitológica(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Ad: #8
            subconjunto = _Ad.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay figura animal incompleta(contenido)")        
                #agregar setear un slot en true para usar al final
        while _An: #10
            subconjunto = _An.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay anatomía(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Art: #11
            subconjunto = _Art.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay arte(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Bl: #13
            subconjunto = _Bl.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay sangre(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Bt: #14
            subconjunto = _Bt.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay botánica(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Cg: #15
            subconjunto = _Cg.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay vestidos(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Cl: #16
            subconjunto = _Cl.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay nubes(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Ex: #17
            subconjunto = _Ex.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay explosión(contenido)")        
                #agrgear setear un slot en true para usar al final
        while _Fi: #18
            subconjunto = _Fi.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay fuego(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Fd: #19
            subconjunto = _Fd.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay comida(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Ge: #20
            subconjunto = _Ge.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay geografía(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Hh: #21
            subconjunto = _Hh.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay hogar(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Na: #23
            subconjunto = _Na.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay naturaleza(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Sc: #24
            subconjunto = _Sc.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay ciencia(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Sx: #25
            subconjunto = _Sx.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay sexo(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Xy: #26
            subconjunto = _Xy.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay radiografía(contenido)")        
                #agregar setear un slot en true para usar al final
        while _Po1: #27 populares
            subconjunto = _Po1.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay respuesta popular de imagen 1(contenido)")        
                #agregar setear un slot en true para usar al final

        #IMAGEN 2 NO TIENE RESPUESTAS POPULARES

        while _Po3: #28 populares
            subconjunto = _Po3.pop()
            if subconjunto in respuesta:
                dispatcher.utter_message(text="Hay respuesta popular de imagen 3(contenido)")        
                #agregar setear un slot en true para usar al final

        #####comprobar populares al final según orden de las respuestas

        ##todo lo que no entra en un conjunto es contenido ideográfico "Id"
        sender = tracker.sender_id
        dispatcher.utter_message(text="DETERMINANTES:")
        if slot_paridad == "true":
            dispatcher.utter_message(text="Hay par(determinante)")
        else:
            dispatcher.utter_message(text="No hay par(determinante)")
        if slot_vista == "true":
            dispatcher.utter_message(text="Hay vista(determinante)")
        else:
            dispatcher.utter_message(text="No hay vista(determinante)")
        if slot_ccromatico == "true":
            dispatcher.utter_message(text="Hay color cromático(determinante)")
        else:
            dispatcher.utter_message(text="No hay color cromático(determinante)")
        if slot_cacromatico == "true":
            dispatcher.utter_message(text="Hay color acromático(determinante)")
        else:
            dispatcher.utter_message(text="No hay color acromático(determinante)")
        if slot_forma == "humana":
            dispatcher.utter_message(text="Hay forma humana(determinante)")
        else:
            if slot_forma == "animal":
                dispatcher.utter_message(text="Hay forma animal(determinante)")
            else:
                if slot_forma == "inanimada":
                    dispatcher.utter_message(text="Hay forma inanimada(determinante)")
                else:
                    dispatcher.utter_message(text="No hay forma(determinante)")
        if slot_movimiento == "true" and slot_forma == 'humana':
            dispatcher.utter_message(text="Hay movimiento humano M(determinante)")
        else:
            if slot_movimiento == "true" and slot_forma == 'inanimada':
                dispatcher.utter_message(text="Hay movimiento inanimado m(determinante)")
            elif slot_movimiento == "true":
                dispatcher.utter_message(text="Hay movimiento indefinido(determinante)")
        if slot_textura == "true":
            dispatcher.utter_message(text="Hay textura(determinante)")
        else:
            dispatcher.utter_message(text="No hay textura(determinante)") 
        if slot_reflejo == "true":
            dispatcher.utter_message(text="Hay reflejo(determinante)")
        else:
            dispatcher.utter_message(text="No hay reflejo(determinante)")
        
        # Lo que hace es mostrar el mensaje con la próxima imagen: utter_Lamina2 ó utter_Lamina3
        next_response = tracker.get_slot("response")
        if next_response != "None":
            dispatcher.utter_message(response=next_response)  


        return [SlotSet("par","false"),SlotSet("vista","false"),SlotSet("color_cromatico","false"),SlotSet("color_acromatico","false"),SlotSet("forma","false"),SlotSet("movimiento","false"),SlotSet("textura","false"),SlotSet("reflejo","false"),SlotSet("response", "None")]

