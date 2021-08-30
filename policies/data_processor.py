from rasa.shared.core.events import SlotSet

class DataProccesor():
    def __init__(self):        

        self._determinantes = ['?','?','?']        
        self._popular = ['?','?','?']
        self._contenidos = ['','','']
        self._par = ['?','?','?']
        self._dq = ['?','?','?']

    def process(self, lamina, tracker):
        self.process_contents( tracker.latest_message.text, lamina-1)
        self.process_determinants(tracker, lamina-1)
        self.process_popular(lamina, tracker.latest_message.text, lamina-1)
        
        # print('lamina: ' + str(lamina))
        # print('contenidos: ' + str(self._contenidos))
        # print('determinantes: ' + str(self._determinantes))
        # print('popular: ' + str(self._popular))
        # print('par: ' + str(self._par))

    def process_contents(self, latest_response, index):

        ###### Contenidos ######:        
        #1 figura humana completa
        _H = {"persona","humano","hombre","mujer","niño","niña","chico","chica","señor","señora","anciano","anciana","viejo","vieja","joven","nene","bebé","bebe","hombrecito","mujercita","personita","personas","humanos","hombres","mujeres","niños","niñas","chicos","chicas","señores","señoras","ancianos","ancianas","viejos","viejas","jovenes","nenes","bebés","bebes","hombrecitos","mujercitas","personitas","futbolista","jugador","jugadora","deportista","ladron","ladrón","ladrona","policía","futbolistas","deportistas","ladrones","ladronas","policias","jugadores","jugadoras","guerrero","guerreros","guerrera","guerreras"}
        #2 figura humana completa irreal, de ficción o mitológica
        _ParentesisH = {"payaso","payasos","hada","hadas","bruja","brujas","fantasma","fantasmas","enano","enanos","enana","enanas","demonio","demonios","ángel","ángeles","humanoide","humanoides","caricaturas","caricatura","monstruo","monstruos","monstruito","monstruitos","duende","duendes"}
        #3 Detalle humano
        _Hd = {"brazo","pierna","dedos","pies","cabeza","codo","nariz","brazos","piernas","diente","dientes","muela","muelas","rodilla","rodillas","cerebro","cerebros",}        
        #4 Detalle humano irreal, de ficción o mitológico
        _ParentesisHd = {"máscara","mascara","máscaras","mascaras"}
        #5 Experiencia humana
        _Hx = {"amor","amar","ama","amamos","amo","odio","odia","odiamos","odiar","depresión","deprimido","deprimida","deprimidos","deprimidas","feliz","felices","alegre","alegres","felicidad","alegria","ruido","ruidoso","sonido","suena","olor","huele","oloroso","miedo","temor","miedoso","contento","contenta","contentos","contentas"}
        #6 Figura animal completa
        _A = {"escarabajo","escarabajos","bicho","bichos","araña","arañas","cucaracha","cucarachas","mariposa","mariposas","mantis","mosca","mosquito","moscas","mosquitos","murcielago","murciélago","murciélagos","pulga","pulgas","águila","águilas","avestruz","ballena","bisonte","bug","búfalo","búhos","buitre","burro","caballo","cabra","camaleón","camello","canario","castor","cebra","cerdo","chancho","ciervo","cobra","colibrí","comadreja","cóndor","conejo","delfín","elefante","faisan","flamenco","foca","gallina","gallo","gato","gorila","guepardo","hámster","hiena","hipopótamo","jabalí","jaguar","jirafa","koala","lagarto","león","lobo","loro","manatí","mapache","mono","murciélago","nutria","ñandú","orcas","oso","pájaro","paloma","panda","pato","pavo","pelícano","perro","pingüino","puercoespín","puma","rana","ratón","reno","rinoceronte","salamandra","sapo","serpiente","tapir","tejon","tiburón","tigre","topo","toro","tucán","vaca","vicuña","zorrino","zorro","águila","avestruces","ballenas","bisontes","búfalos","bugs","búho","buitres","burros","caballos","cabras","camaleones","camellos","canarios","castores","cebras","cerdos","chanchos","ciervos","cobras","colibries","comadrejas","cóndores","conejos","delfines","elefantes","faisanes","flamencos","focas","gallinas","gallos","gatos","gorilas","guepardos","hámsters","hienas","hipopótamos","jabalies","jaguares","jirafas","koalas","lagartos","leones","lobos","loros","manaties","mapaches","monos","murciélagos","nutrias","ñandues","orca","osos","pájaros","palomas","pandas","patos","pavos","pelícanos","perros","pingüinos","puercoespines","pumas","ranas","ratones","renos","rinocerontes","salamandras","sapos","serpientes","tapires","tiburones","tigres","topos","toros","tucanes","vacas","víbora","víboras","vicuñas","zorrinos","zorros""bacteria","bacterias","animal","animales","arácnido","aracnido","arácnidos","arácnido","libélula","libélulas","libelula","libelulas","ciempies","pescado","bagre","escorpión","escorpion","escorpiones","cotorras","caballito","elefantito","camaron","camarones","artrópodo","artropodo","artrópodos","artropodos","garrapata","garrapatas","peces","pez","langosta","langostas"}
        #7 Figura animal completa irreal, de ficción o mitológica
        _ParentesisA = {"fiera","bruja","brujas","ángel","angel","ángeles","angeles","demonio","demonios","fantasma","fantasmas","unicornio","unicornios","dragón","dragon","dragones","minotauro","minotauros","krampus","hada","guason","batman","superman","korioto","koriotos","pato donald","mickey","yeti","yetis",}
        #8 Figura animal incompleta
        _Ad = {"pata","patas","cola","pinza","hocico", "cuero","pezuñas","garras","vasos","pico","melena","trompa","cuerno","colmillo","colmillos"}
        #9 Figura animal irreal, de ficción o mitológica incompleta. PENDIENTE
        #10 Anatomía
        _An = {"ósea","osea","cráneo","cráneo","torax","toracica","tórax","corazón","corazon","pulmón","pulmon","estomágo","estomago","panza","hígado","higado","musculo","articulaciones","vértebral","vértebra","vertebras","cerebro","cerebros"}
        #11 Arte
        _Art = {"pintura","dibujo","pinturas","dibujos","ilustración","ilustracion","ilustraciones","acuarela","acuarelas","arte","estatua","estatuas","escultura","esculturas","joya","joyas","insignia","insignias","escudo","escudos","adornos","espada","espadas","cuadros","lienzos","cuadro","lienzo","logo","logos"}
        #12 Antropología
        _Ay = {"tótem","totem","templo","prehistórica","prehistorica","prehistóricas","prehistorica","incaica","incaicas","azteca","aztecas","maya","mayas","romano","romanos","griego","griegos","persa","persas"}
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
        _Na = {"lago","laguna","lagos","lagunas","sol","luna","mar","mar","océano","océanos","agua","hielo","hielos","lluvia","lluvias","niebla","neblina","bruma","tormenta","brisa","viento","arco iris","tormenta","noche","día","dia","granizo","trueno","relámpago","relampago","bosque"}
        #24 Ciencia
        _Sc = {"avión","aviones","avion","edificio","edificios","puente","puentes","auto","autos","moto","motos","microscopio","microscopios","laboratorio","laboratorios","motor","motores","turbina","turbinas","telescopio","telescopios","arma","armas","armamento","cohete","cohetes","nave","naves","ovni","OVNI","ovnis","OVNIS","barco","barcos","antena","antenas","satélite","satélites","satelite","satelites"}
        #25 Sexo
        _Sx = {"pene","penes","verga","vergas","pito","pitos","vagina","vaginas","concha","conchas","nalgas","cachas","pechos","teta","tetas","testículos","huevos","bolas","menstruación","aborto","abortar","coito","coger","garchar","cogiendo","teniendo sexo","garchando"}
        #26 Radiografía
        _Xy = {"radiografía","radiografia","placa","placas","rayos x","tomografía","ecografía","tomografía","ultrasonido","resonancia"}

        while _H: #1 figura humana completa
            subconjunto = _H.pop()
            if subconjunto in latest_response:
                if ' H,' not in self._contenidos[index]:
                    self._contenidos[index] += ' H,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' H,'    
                break   
        while _ParentesisH: #2 figura humana completa irreal, de ficción o mitológica
            subconjunto = _ParentesisH.pop()
            if subconjunto in latest_response:
                if ' (H),' not in self._contenidos[index]:
                    self._contenidos[index] += ' (H),'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' (H),'    
                break
        while _Hd: #3 Detalle humano
            subconjunto = _Hd.pop()
            if subconjunto in latest_response:
                if ' Hd,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Hd,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Hd,'    
                break
        while _ParentesisHd: #4 Detalle humano irreal, de ficción o mitológico
            subconjunto = _ParentesisHd.pop()
            if subconjunto in latest_response:
                if ' (Hd),' not in self._contenidos[index]:
                    self._contenidos[index] += ' (Hd),'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' (Hd),'    
                break    
        while _Hx: #5 Experiencia humana
            subconjunto = _Hx.pop()
            if subconjunto in latest_response:
                if ' Hx,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Hx,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Hx,'    
                break
        while _A: #6 Figura animal completa
            subconjunto = _A.pop()
            if subconjunto in latest_response:
                if ' A,' not in self._contenidos[index]:
                    self._contenidos[index] += ' A,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' A,'    
                break
        while _ParentesisA: #7 Figura animal completa irreal, de ficción o mitológica
            subconjunto = _ParentesisA.pop()
            if subconjunto in latest_response:
                if ' (A),' not in self._contenidos[index]:
                    self._contenidos[index] += ' (A),'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' (A),'    
                break
        while _Ad: #8 Figura animal incompleta
            subconjunto = _Ad.pop()
            if subconjunto in latest_response:
                if ' Ad,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Ad,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Ad,'    
                break
        while _An: #10 Anatomía
            subconjunto = _An.pop()
            if subconjunto in latest_response:
                if ' An,' not in self._contenidos[index]:
                    self._contenidos[index] += ' An,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' An,'    
                break
        while _Art: #11 Arte
            subconjunto = _Art.pop()
            if subconjunto in latest_response:
                if ' Art,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Art,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Art,'    
                break
        while _Ay: #12 Antropológica
            subconjunto = _Ay.pop()
            if subconjunto in latest_response:
                if ' Ay,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Ay,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Ay,'    
                break
        while _Bl: #13 Sangre
            subconjunto = _Bl.pop()
            if subconjunto in latest_response:
                if ' Bl,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Bl,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Bl,'    
                break
        while _Bt: #14 Botánica
            subconjunto = _Bt.pop()
            if subconjunto in latest_response:
                if ' Bt,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Bt,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Bt,'    
                break
        while _Cg: #15 Vestidos
            subconjunto = _Cg.pop()
            if subconjunto in latest_response:
                if ' Cg,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Cg,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Cg,'    
                break
        while _Cl: #16 Nubes
            subconjunto = _Cl.pop()
            if subconjunto in latest_response:
                if ' Cl,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Cl,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Cl,'    
                break
        while _Ex: #17 Explosión
            subconjunto = _Ex.pop()
            if subconjunto in latest_response:
                if ' Ex,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Ex,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Ex,'    
                break
        while _Fi: #18 Fuego
            subconjunto = _Fi.pop()
            if subconjunto in latest_response:
                if ' Fi,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Fi,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Fi,'    
                break
        while _Fd: #19 Comida
            subconjunto = _Fd.pop()
            if subconjunto in latest_response:
                if ' Fd,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Fd,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Fd,'    
                break
        while _Ge: #20 Geografía
            subconjunto = _Ge.pop()
            if subconjunto in latest_response:
                if ' Ge,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Ge,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Ge,'    
                break
        while _Hh: #21 Hogar
            subconjunto = _Hh.pop()
            if subconjunto in latest_response:
                if ' Hh,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Hh,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Hh,'    
                break
        while _Ls: #21 Paisaje
            subconjunto = _Ls.pop()
            if subconjunto in latest_response:
                if ' Ls,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Ls,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Ls,'    
                break
        while _Na: #23 Naturaleza
            subconjunto = _Na.pop()
            if subconjunto in latest_response:
                if ' Na,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Na,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Na,'    
                break
        while _Sc: #24 Ciencia
            subconjunto = _Sc.pop()
            if subconjunto in latest_response:
                if ' Sc,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Sc,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Sc,'    
                break
        while _Sx: #25 sexo
            subconjunto = _Sx.pop()
            if subconjunto in latest_response:
                if ' Sx,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Sx,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Sx,'    
                break
        while _Xy: #26 Radiografía
            subconjunto = _Xy.pop()
            if subconjunto in latest_response:
                if ' Xy,' not in self._contenidos[index]:
                    self._contenidos[index] += ' Xy,'
                elif self._contenidos[index] == '':
                    self._contenidos[index] = ' Xy,'    
                break
        ##todo lo que no entra en un conjunto es contenido ideográfico "Id"
        

    
    def process_determinants(self, tracker, index):

        ###### Determinantes #####
        slot_paridad = tracker.get_slot("par")
        slot_vista = tracker.get_slot("vista")
        slot_ccromatico = tracker.get_slot("color_cromatico")
        slot_cacromatico = tracker.get_slot("color_acromatico")
        slot_forma = tracker.get_slot("forma")
        slot_movimiento = tracker.get_slot("movimiento")
        slot_textura = tracker.get_slot("textura")
        slot_reflejo = tracker.get_slot("reflejo") 
        slot_sombreado = tracker.get_slot("sombreado")    

        # print(slot_paridad)  
        # print(slot_vista)
        # print(slot_ccromatico)
        # print(slot_cacromatico) 
        # print(slot_forma)
        # print(slot_movimiento)
        # print(slot_textura)
        # print(slot_reflejo) 
        # print(slot_sombreado)    
        
        if slot_paridad == "true":
            self._par[index] = '2'

        if slot_vista == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' V,'
            elif ' V,' not in self._determinantes[index]:
                self._determinantes[index] += ', V,'

        if slot_ccromatico == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' C,'
            elif ' C,' not in self._determinantes[index]:
                self._determinantes[index] += ' C,'

        if slot_cacromatico == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' C\','
            elif ' C\',' not in self._determinantes[index]:
                self._determinantes[index] += ' C\','
        if ((slot_forma == "humana") or (slot_forma == "animal") or (slot_forma == "inanimada")):
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' F,'
            elif ' F,' not in self._determinantes[index]:           #and' F,' in ws['F'+ str(lamina)].value: 
                self._determinantes[index] += ' F,'
        if slot_movimiento == "true": 
            if slot_forma == 'humana':
                if self._determinantes[index] == '?':
                    self._determinantes[index] = ' M,'
                elif ' M,' not in self._determinantes[index]:
                    self._determinantes[index] += ' M,'
            elif slot_forma == 'inanimada':
                if self._determinantes[index] == '?':
                    self._determinantes[index] = ' m,'
                elif ' m,' not in self._determinantes[index]: 
                    self._determinantes[index] += ' m,'
            else:
                if self._determinantes[index] == '?':
                    self._determinantes[index] = ' ind,'
                elif ' ind,' not in self._determinantes[index]:
                    self._determinantes[index] += ' ind,'
        if slot_textura == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' T,'
            elif ' T,' not in self._determinantes[index]:
                self._determinantes[index] += ' T,'
        if slot_reflejo == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' r,'
            elif ' r,' not in self._determinantes[index]:
                self._determinantes[index] += ' r,'
        if slot_sombreado == "true":
            if self._determinantes[index] == '?':
                self._determinantes[index] = ' Y,'
            elif ' Y,' not in self._determinantes[index]:
                self._determinantes[index] += ' Y,'
        
        tracker.update(SlotSet("par","false"))
        tracker.update(SlotSet("vista","false"))
        tracker.update(SlotSet("color_cromatico","false"))
        tracker.update(SlotSet("color_acromatico","false"))
        tracker.update(SlotSet("forma","false"))
        tracker.update(SlotSet("movimiento","false"))
        tracker.update(SlotSet("textura","false"))
        tracker.update(SlotSet("reflejo","false"))
        tracker.update(SlotSet("sombreado","false"))


    ########### Preguntar esto como es ############
    def process_popular(self, lamina, latest_response, index):
        #27 Popular1
        _Po1 = {"escarabajo","escarabajos","bicho","bichos","araña","arañas","cucaracha","cucarachas","mariposa","mariposas","mantis","mosca","mosquito","moscas","mosquitos","insecto","insectos","gusano"}
        #28 Popular3
        _Po3 = {"persona","humano","hombre","mujer","niño","niña","chico","chica","señor","señora","personas","humanos","hombres","mujeres","niños","niñas","chicos","chicas","señores","señoras","payaso","payasos","hada","hadas","bruja","brujas","fantasma","fantasmas","enano","enanos","enana","enanas","demonio","demonios","ángel","ángeles","humanoide","humanoides","caricaturas","caricatura","monstruo","monstruos","duende","duendes"}
        #IMAGEN 2 NO TIENE latest_responseS POPULARES
        
        while _Po1: #27 populares
            subconjunto = _Po1.pop()
            if subconjunto in latest_response:
                if lamina == 1: #and zona corresponde
                    self._popular[index] = 'Po1'  # hay que revisar si coincide con sector de la imagen
                    break
                else: 
                    self._popular[index] = '?'            

        # IMAGEN 2 NO TIENE RESPUESTAS POPULARES

        while _Po3: #28 populares
            subconjunto = _Po3.pop()
            if subconjunto in latest_response:
                if lamina == 3: #and zona corresponde
                    self._popular[index] = 'Po3'       
                    break
                else: self._popular[index] ='?'

    def process_developmental_quality(self, intent_name, index):
        if intent_name == "respuestasv":
            self._dq[index] = "v"
        elif intent_name == "respuestasvmas":
            self._dq[index] = "v/+"
        elif intent_name == "respuestaso":
            self._dq[index] = "o"
        elif intent_name == "respuestas+":
            self._dq[index] = "+"
        


