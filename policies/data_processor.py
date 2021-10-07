from rasa.shared.core.events import SlotSet
from policies.location import LocationProcessor


class DataProccesor():
    def __init__(self):

        self._determinantes = [[], [], []]
        self._popular = [[], [], []]
        self._contenidos = [[], [], []]
        self._par = [[], [], []]
        self._dq = [[], [], []]
        self._forma = [[], [], []]
        self._location = [[], [], []]
        self._zscore = [[], [], []]

        self._location_processor = LocationProcessor()

    def process(self, lamina, tracker, state, rta):
        self.process_contents(tracker.latest_message.text,
                              lamina-1, state, rta)
        self.process_determinants(tracker, lamina-1, state, rta)
        
        # self.process_popular(
        #     lamina, tracker.latest_message.text, lamina-1, state, rta)

        # print('lamina: ' + str(lamina))
        # print('state: ' + str(state))
        # print('rta: ' + str(rta))
        # print('contenidos: ' + str(self._contenidos))
        # print('determinantes: ' + str(self._determinantes))
        # print('popular: ' + str(self._popular))
        # print('par: ' + str(self._par))

    def process_contents(self, latest_response: str, index, state, rta):

        # Contenidos ######:
        # 1 figura humana completa
        _H = {"persona", "humano", "hombre", "mujer", "niño", "niña", "chico", "chica", "señor", "señora", "anciano", "anciana", "viejo", "vieja", "joven", "nene", "bebé", "bebe", "hombrecito", "mujercita", "personita", "personas", "humanos", "hombres", "mujeres", "niños", "niñas", "chicos", "chicas", "señores", "señoras", "ancianos", "ancianas",
              "viejos", "viejas", "jovenes", "nenes", "bebés", "bebes", "hombrecitos", "mujercitas", "personitas", "futbolista", "jugador", "jugadora", "deportista", "ladron", "ladrón", "ladrona", "policía", "futbolistas", "deportistas", "ladrones", "ladronas", "policias", "jugadores", "jugadoras", "guerrero", "guerreros", "guerrera", "guerreras"}
        # 2 figura humana completa irreal, de ficción o mitológica
        _ParentesisH = {"payaso", "payasos", "hada", "hadas", "bruja", "brujas", "fantasma", "fantasmas", "enano", "enanos", "enana", "enanas", "demonio", "demonios",
                        "ángel", "ángeles", "humanoide", "humanoides", "caricaturas", "caricatura", "monstruo", "monstruos", "monstruito", "monstruitos", "duende", "duendes"}
        # 3 Detalle humano
        _Hd = {"brazo", "pierna", "dedos", "pies", "cabeza", "codo", "nariz", "brazos", "piernas",
               "diente", "dientes", "muela", "muelas", "rodilla", "rodillas", "cerebro", "cerebros", "cara"}
        # 4 Detalle humano irreal, de ficción o mitológico
        _ParentesisHd = {"máscara", "mascara", "máscaras", "mascaras"}
        # 5 Experiencia humana
        _Hx = {"amor", "amar", "ama", "amamos", "amo", "odio", "odia", "odiamos", "odiar", "depresión", "deprimido", "deprimida", "deprimidos", "deprimidas", "feliz", "felices", "alegre",
               "alegres", "felicidad", "alegria", "ruido", "ruidoso", "sonido", "suena", "olor", "huele", "oloroso", "miedo", "temor", "miedoso", "contento", "contenta", "contentos", "contentas"}
        # 6 Figura animal completa
        _A = {"escarabajo", "escarabajos", "bicho", "bichos", "araña", "arañas", "cucaracha", "cucarachas", "mariposa", "mariposas", "mantis", "mosca", "mosquito", "moscas", "mosquitos", "murcielago", "murciélago", "murciélagos", "pulga", "pulgas", "águila", "águilas", "avestruz", "ballena", "bisonte", "bug", "búfalo", "búhos", "buitre", "burro", "caballo", "cabra", "camaleón", "camello", "canario", "castor", "cebra", "cerdo", "chancho", "ciervo", "cobra", "colibrí", "comadreja", "cóndor", "conejo", "delfín", "elefante", "faisan", "flamenco", "foca", "gallina", "gallo", "gato", "gorila", "guepardo", "hámster", "hiena", "hipopótamo", "jabalí", "jaguar", "jirafa", "koala", "lagarto", "león", "lobo", "loro", "manatí", "mapache", "mono", "murciélago", "nutria", "ñandú", "orcas", "oso", "pájaro", "paloma", "panda", "pato", "pavo", "pelícano", "perro", "pingüino", "puercoespín", "puma", "rana", "ratón", "reno", "rinoceronte", "salamandra", "sapo", "serpiente", "tapir", "tejon", "tiburón", "tigre", "topo", "toro", "tucán", "vaca", "vicuña", "zorrino", "zorro", "águila", "avestruces", "ballenas", "bisontes", "búfalos", "bugs", "búho", "buitres", "burros", "caballos", "cabras", "camaleones",
              "camellos", "canarios", "castores", "cebras", "cerdos", "chanchos", "ciervos", "cobras", "colibries", "comadrejas", "cóndores", "conejos", "delfines", "elefantes", "faisanes", "flamencos", "focas", "gallinas", "gallos", "gatos", "gorilas", "guepardos", "hámsters", "hienas", "hipopótamos", "jabalies", "jaguares", "jirafas", "koalas", "lagartos", "leones", "lobos", "loros", "manaties", "mapaches", "monos", "murciélagos", "nutrias", "ñandues", "orca", "osos", "pájaros", "palomas", "pandas", "patos", "pavos", "pelícanos", "perros", "pingüinos", "puercoespines", "pumas", "ranas", "ratones", "renos", "rinocerontes", "salamandras", "sapos", "serpientes", "tapires", "tiburones", "tigres", "topos", "toros", "tucanes", "vacas", "víbora", "víboras", "vicuñas", "zorrinos", "zorros""bacteria", "bacterias", "animal", "animales", "arácnido", "aracnido", "arácnidos", "arácnido", "libélula", "libélulas", "libelula", "libelulas", "ciempies", "pescado", "bagre", "escorpión", "escorpion", "escorpiones", "cotorras", "caballito", "elefantito", "camaron", "camarones", "artrópodo", "artropodo", "artrópodos", "artropodos", "garrapata", "garrapatas", "peces", "pez", "langosta", "langostas"}
        # 7 Figura animal completa irreal, de ficción o mitológica
        _ParentesisA = {"fiera", "bruja", "brujas", "ángel", "angel", "ángeles", "angeles", "demonio", "demonios", "fantasma", "fantasmas", "unicornio", "unicornios", "dragón",
                        "dragon", "dragones", "minotauro", "minotauros", "krampus", "hada", "guason", "batman", "superman", "korioto", "koriotos", "pato donald", "mickey", "yeti", "yetis", }
        # 8 Figura animal incompleta
        _Ad = {"pata", "patas", "cola", "pinza", "hocico", "cuero", "pezuñas", "garras",
               "vasos", "pico", "melena", "trompa", "cuerno", "colmillo", "colmillos"}
        # 9 Figura animal irreal, de ficción o mitológica incompleta. PENDIENTE
        # 10 Anatomía
        _An = {"ósea", "osea", "cráneo", "cráneo", "torax", "toracica", "tórax", "corazón", "corazon", "pulmón", "pulmon", "estomágo",
               "estomago", "panza", "hígado", "higado", "musculo", "articulaciones", "vértebral", "vértebra", "vertebras", "cerebro", "cerebros"}
        # 11 Arte
        _Art = {"pintura", "dibujo", "pinturas", "dibujos", "ilustración", "ilustracion", "ilustraciones", "acuarela", "acuarelas", "arte", "estatua", "estatuas", "escultura",
                "esculturas", "joya", "joyas", "insignia", "insignias", "escudo", "escudos", "adornos", "espada", "espadas", "cuadros", "lienzos", "cuadro", "lienzo", "logo", "logos"}
        # 12 Antropología
        _Ay = {"tótem", "totem", "templo", "prehistórica", "prehistorica", "prehistóricas", "prehistorica", "incaica",
               "incaicas", "azteca", "aztecas", "maya", "mayas", "romano", "romanos", "griego", "griegos", "persa", "persas"}
        # 13 Sangre
        _Bl = {"sangre", "sanguíneo", "sanguínea", "sanguinario",
               "sanguinaria", "sangriento", "sangrienta"}
        # 14 Botánica
        _Bt = {"vegetal", "vegetales", "arbusto", "arbustos", "flor", "flores", "floral", "alga", "algas", "arbol", "árbol", "árboles", "arboles",
               "hoja", "hojas", "pétalo", "pétalos", "tronco", "tronco", "raiz", "raíces", "nido", "hongo", "hongos", "pino", "palmera", "pinos", "palmeras"}
        # 15 Vestidos
        _Cg = {"sombrero", "sombreros", "gorro", "gorros", "gorras", "gorra", "bota", "botas", "botines", "cinturón", "cinturon", "cinturones", "corbata", "corbatas", "moño", "moños", "chaqueta",
               "chaquetas", "saco", "sacos", "polera", "poleras", "pantalón", "pantalon", "pantalones", "bufanda", "bufandas", "bermudas", "short", "shorts", "medias", "calzoncillos", "musculosa"}
        # 16 Nubes
        _Cl = {"nubes", "nube", "nubarrón", "nubarrones", "nublado", "nublada"}
        # 17 Explosión
        _Ex = {"explosión", "explosión", "explotar", "implotar", "bomba", "explosivos",
               "estallido", "estallidos", "detonación", "detonaciones", "bombardeo", "bombardeos"}
        # 18 Fuego
        _Fi = {"fuego", "fuegos", "llama", "llamas", "incendio", "incendios", "humo", "humos",
               "fogata", "fogatas", "chispa", "chispas", "hoguera", "hogueras", "quema", "quemas"}
        # 19 Comida
        _Fd = {"pollo", "pollos", "carne", "carnes", "pescado", "pescados", "helado", "helados", "panqueque", "panqueques", "verdura", "verduras", "papa", "papas", "zapallo", "zapallos", "lechuga", "lechugas", "tomates", "tomate", "zanahoria", "zanahorias", "sandía", "sandías",
               "melón", "melones", "kiwi", "kiwis", "mandarina", "naranja", "mandarinas", "naranjas", "banana", "bananas", "palta", "frutas", "verdura", "fruta", "torta", "budín", "tostadas", "sandwich", "sandwiches", "pan", "panes", "sopa", "pasta", "sopas", "pastas", "spaghetti"}
        # 20 Geografía
        _Ge = {"mapa", "mapas", "plano", "planos", "cartográfico", "cartografía", "continente",
               "continentes", "país", "paises", "ciudad", "ciudad", "region", "regiones"}
        # 21 Hogar
        _Hh = {"cama", "cucheta", "sommier", "sillón", "silla", "mesa", "lámpara", "cuchillo", "olla", "alfombra", "cortina", "mueble", "horno", "cocina", "pieza", "habitación", "baño", "cochera", "garage",
               "camas", "cuchetas", "sommiers", "sillones", "sillas", "mesas", "lámparas", "cuchillos", "ollas", "alfombras", "cortinas", "muebles", "hornos", "cocinas", "piezas", "habitaciones", "baños", "cocheras"}
        # 22 Paisaje
        _Ls = {"montaña", "montañas", "cordillera", "cordilleras", "colina", "colinas", "cerro", "cerros", "sierra", "sierras", "isla", "islas", "cueva", "cuevas",
               "roca", "rocas", "piedra", "piedras", "bosque", "bosques", "desierto", "desierto", "llanura", "llanuras", "pantano", "pantanos", "glaciar", "glaciares"}
        # 23 Naturaleza
        _Na = {"lago", "laguna", "lagos", "lagunas", "sol", "luna", "mar", "mar", "océano", "océanos", "agua", "hielo", "hielos", "lluvia", "lluvias", "niebla",
               "neblina", "bruma", "tormenta", "brisa", "viento", "arco iris", "tormenta", "noche", "día", "dia", "granizo", "trueno", "relámpago", "relampago", "bosque"}
        # 24 Ciencia
        _Sc = {"avión", "aviones", "avion", "edificio", "edificios", "puente", "puentes", "auto", "autos", "moto", "motos", "microscopio", "microscopios", "laboratorio", "laboratorios", "motor", "motores", "turbina", "turbinas",
               "telescopio", "telescopios", "arma", "armas", "armamento", "cohete", "cohetes", "nave", "naves", "ovni", "OVNI", "ovnis", "OVNIS", "barco", "barcos", "antena", "antenas", "satélite", "satélites", "satelite", "satelites"}
        # 25 Sexo
        _Sx = {"pene", "penes", "verga", "vergas", "pito", "pitos", "vagina", "vaginas", "concha", "conchas", "nalgas", "cachas", "pechos", "teta", "tetas",
               "testículos", "huevos", "bolas", "menstruación", "aborto", "abortar", "coito", "coger", "garchar", "cogiendo", "teniendo sexo", "garchando"}
        # 26 Radiografía
        _Xy = {"radiografía", "radiografia", "placa", "placas", "rayos x",
               "tomografía", "ecografía", "tomografía", "ultrasonido", "resonancia"}

        contenidos = ''

        respuesta = latest_response.split()

        while _H and ' H,' not in contenidos:  # 1 figura humana completa
            subconjunto = _H.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' H,' not in contenidos:
                        contenidos += ' H,'
                    elif contenidos == '':
                        contenidos = ' H,'

        # 2 figura humana completa irreal, de ficción o mitológica
        while _ParentesisH and ' (H),' not in contenidos:
            subconjunto = _ParentesisH.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' (H),' not in contenidos:
                        contenidos += ' (H),'
                    elif contenidos == '':
                        contenidos = ' (H),'

        while _Hd and ' Hd,' not in contenidos:  # 3 Detalle humano
            subconjunto = _Hd.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Hd,' not in contenidos:
                        contenidos += ' Hd,'
                    elif contenidos == '':
                        contenidos = ' Hd,'

        # 4 Detalle humano irreal, de ficción o mitológico
        while _ParentesisHd and ' (Hd),' not in contenidos:
            subconjunto = _ParentesisHd.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' (Hd),' not in contenidos:
                        contenidos += ' (Hd),'
                    elif contenidos == '':
                        contenidos = ' (Hd),'

        while _Hx and ' Hx,' not in contenidos:  # 5 Experiencia humana
            subconjunto = _Hx.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Hx,' not in contenidos:
                        contenidos += ' Hx,'
                    elif contenidos == '':
                        contenidos = ' Hx,'

        while _A and ' A,' not in contenidos:  # 6 Figura animal completa
            subconjunto = _A.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' A,' not in contenidos:
                        contenidos += ' A,'
                    elif contenidos == '':
                        contenidos = ' A,'

        # 7 Figura animal completa irreal, de ficción o mitológica
        while _ParentesisA and ' (A),' not in contenidos:
            subconjunto = _ParentesisA.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' (A),' not in contenidos:
                        contenidos += ' (A),'
                    elif contenidos == '':
                        contenidos = ' (A),'

        while _Ad and ' Ad,' not in contenidos:  # 8 Figura animal incompleta
            subconjunto = _Ad.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Ad,' not in contenidos:
                        contenidos += ' Ad,'
                    elif contenidos == '':
                        contenidos = ' Ad,'

        while _An and ' An,' not in contenidos:  # 10 Anatomía
            subconjunto = _An.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' An,' not in contenidos:
                        contenidos += ' An,'
                    elif contenidos == '':
                        contenidos = ' An,'

        while _Art and ' Art,' not in contenidos:  # 11 Arte
            subconjunto = _Art.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Art,' not in contenidos:
                        contenidos += ' Art,'
                    elif contenidos == '':
                        contenidos = ' Art,'

        while _Ay and ' Ay,' not in contenidos:  # 12 Antropológica
            subconjunto = _Ay.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Ay,' not in contenidos:
                        contenidos += ' Ay,'
                    elif contenidos == '':
                        contenidos = ' Ay,'

        while _Bl and ' Bl,' not in contenidos:  # 13 Sangre
            subconjunto = _Bl.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Bl,' not in contenidos:
                        contenidos += ' Bl,'
                    elif contenidos == '':
                        contenidos = ' Bl,'

        while _Bt and ' Bt,' not in contenidos:  # 14 Botánica
            subconjunto = _Bt.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Bt,' not in contenidos:
                        contenidos += ' Bt,'
                    elif contenidos == '':
                        contenidos = ' Bt,'

        while _Cg and ' Cg,' not in contenidos:  # 15 Vestidos
            subconjunto = _Cg.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Cg,' not in contenidos:
                        contenidos += ' Cg,'
                    elif contenidos == '':
                        contenidos = ' Cg,'

        while _Cl and ' Cl,' not in contenidos:  # 16 Nubes
            subconjunto = _Cl.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Cl,' not in contenidos:
                        contenidos += ' Cl,'
                    elif contenidos == '':
                        contenidos = ' Cl,'

        while _Ex and ' Ex,' not in contenidos:  # 17 Explosión
            subconjunto = _Ex.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Ex,' not in contenidos:
                        contenidos += ' Ex,'
                    elif contenidos == '':
                        contenidos = ' Ex,'

        while _Fi and ' Fi,' not in contenidos:  # 18 Fuego
            subconjunto = _Fi.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Fi,' not in contenidos:
                        contenidos += ' Fi,'
                    elif contenidos == '':
                        contenidos = ' Fi,'

        while _Fd and ' Fd,' not in contenidos:  # 19 Comida
            subconjunto = _Fd.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Fd,' not in contenidos:
                        contenidos += ' Fd,'
                    elif contenidos == '':
                        contenidos = ' Fd,'

        while _Ge and ' Ge,' not in contenidos:  # 20 Geografía
            subconjunto = _Ge.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Ge,' not in contenidos:
                        contenidos += ' Ge,'
                    elif contenidos == '':
                        contenidos = ' Ge,'

        while _Hh and ' Hh,' not in contenidos:  # 21 Hogar
            subconjunto = _Hh.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Hh,' not in contenidos:
                        contenidos += ' Hh,'
                    elif contenidos == '':
                        contenidos = ' Hh,'

        while _Ls and ' Ls,' not in contenidos:  # 22 Paisaje
            subconjunto = _Ls.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Ls,' not in contenidos:
                        contenidos += ' Ls,'
                    elif contenidos == '':
                        contenidos = ' Ls,'

        while _Na and ' Na,' not in contenidos:  # 23 Naturaleza
            subconjunto = _Na.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Na,' not in contenidos:
                        contenidos += ' Na,'
                    elif contenidos == '':
                        contenidos = ' Na,'

        while _Sc and ' Sc,' not in contenidos:  # 24 Ciencia
            subconjunto = _Sc.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Sc,' not in contenidos:
                        contenidos += ' Sc,'
                    elif contenidos == '':
                        contenidos = ' Sc,'

        while _Sx and ' Sx,' not in contenidos:  # 25 sexo
            subconjunto = _Sx.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Sx,' not in contenidos:
                        contenidos += ' Sx,'
                    elif contenidos == '':
                        contenidos = ' Sx,'

        while _Xy and ' Xy,' not in contenidos:  # 26 Radiografía
            subconjunto = _Xy.pop()
            for i in respuesta:
                if subconjunto == i:
                    if ' Xy,' not in contenidos:
                        contenidos += ' Xy,'
                    elif contenidos == '':
                        contenidos = ' Xy,'

        if state == 1:
            self._contenidos[index].append(contenidos)
        else:
            self._contenidos[index][rta] += contenidos
            # Todo lo que no entra en un conjunto es contenido ideográfico "Id"
            if self._contenidos[index][rta] == '':
                self._contenidos[index][rta] = "Id"

    def process_determinants(self, tracker, index, state, rta):

        if state == 1:
            determinantes = '?'
            par = 'no'
        else:
            determinantes = self._determinantes[index][rta]
            par = self._par[index][rta]

        forma = 'None'

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

        if slot_paridad == "true":
            par = 'si'

        if slot_vista == "true":
            if determinantes == '?':
                determinantes = ' V,'
            elif ' V,' not in determinantes:
                determinantes += ', V,'

        if slot_ccromatico == "true":
            if determinantes == '?':
                determinantes = ' C,'
            elif ' C,' not in determinantes:
                determinantes += ' C,'

        if slot_cacromatico == "true":
            if determinantes == '?':
                determinantes = ' C\','
            elif ' C\',' not in determinantes:
                determinantes += ' C\','
        if ((slot_forma == "humana") or (slot_forma == "animal") or (slot_forma == "inanimada")):
            if determinantes == '?':
                determinantes = ' F,'
            elif ' F,' not in determinantes:
                determinantes += ' F,'
            forma = slot_forma

        if slot_movimiento == "true":
            if slot_forma == 'humana' or (state == 2 and self._forma[index][rta] == 'humana'):
                if determinantes == '?':
                    determinantes = ' M,'
                elif ' M,' not in determinantes:
                    determinantes += ' M,'
            elif slot_forma == 'inanimada' or (state == 2 and self._forma[index][rta] == 'inanimada'):
                if determinantes == '?':
                    determinantes = ' m,'
                elif ' m,' not in determinantes:
                    determinantes += ' m,'
            else:
                if determinantes == '?':
                    determinantes = ' ind,'
                elif ' ind,' not in determinantes:
                    determinantes += ' ind,'

        if slot_textura == "true":
            if determinantes == '?':
                determinantes = ' T,'
            elif ' T,' not in determinantes:
                determinantes += ' T,'
        if slot_reflejo == "true":
            if determinantes == '?':
                determinantes = ' r,'
            elif ' r,' not in determinantes:
                determinantes += ' r,'
        if slot_sombreado == "true":
            if determinantes == '?':
                determinantes = ' Y,'
            elif ' Y,' not in determinantes:
                determinantes += ' Y,'

        if state == 1:
            self._determinantes[index].append(determinantes)
            self._par[index].append(par)
            self._forma[index].append(forma)
        else:
            self._determinantes[index][rta] = determinantes
            self._par[index][rta] = par

        tracker.update(SlotSet("par", "false"))
        tracker.update(SlotSet("vista", "false"))
        tracker.update(SlotSet("color_cromatico", "false"))
        tracker.update(SlotSet("color_acromatico", "false"))
        tracker.update(SlotSet("forma", "false"))
        tracker.update(SlotSet("movimiento", "false"))
        tracker.update(SlotSet("textura", "false"))
        tracker.update(SlotSet("reflejo", "false"))
        tracker.update(SlotSet("sombreado", "false"))

    def process_popular(self, lamina, response, response_number):
        
        # 27 Popular1
        _Po1 = {"escarabajo", "escarabajos", "bicho", "bichos", "araña", "arañas", "cucaracha", "cucarachas",
                "mariposa", "mariposas", "mantis", "mosca", "mosquito", "moscas", "mosquitos", "insecto", "insectos", "gusano"}
        # 28 Popular3
        _Po3 = {"persona", "humano", "hombre", "mujer", "niño", "niña", "chico", "chica", "señor", "señora", "personas", "humanos", "hombres", "mujeres", "niños", "niñas", "chicos", "chicas", "señores", "señoras", "payaso", "payasos", "hada",
                "hadas", "bruja", "brujas", "fantasma", "fantasmas", "enano", "enanos", "enana", "enanas", "demonio", "demonios", "ángel", "ángeles", "humanoide", "humanoides", "caricaturas", "caricatura", "monstruo", "monstruos", "duende", "duendes"}
        
        popular = 'no'

        if lamina == 1 and self._location[lamina-1][response_number] == 'W':
            while _Po1 and popular == 'no':  # 27 populares
                subconjunto = _Po1.pop()
                if subconjunto in response:
                        popular = 'si'

        # La imagen 2 no tiene respuestas populares

        if lamina == 3 and (self._location[lamina-1][response_number] == 'W' or self._location[lamina-1][response_number] == 'D2'):
            while _Po3 and popular == 'no':  # 28 populares
                subconjunto = _Po3.pop()
                if subconjunto in response:
                        popular = 'si'

        self._popular[lamina-1].append(popular)
        

    def process_developmental_quality(self, intent_name, index):
        if intent_name == "respuestasv":
            self._dq[index].append("v")
        elif intent_name == "respuestasvmas":
            self._dq[index].append("v/+")
        elif intent_name == "respuestaso":
            self._dq[index].append("o")
        elif intent_name == "respuestas+":
            self._dq[index].append("+")

    def process_location(self, user_name, responses):
        for lamina in range(0,3):
            for response_number in range(0,len(responses[lamina])):
                self._location[lamina].append(self._location_processor.process_response_location(
                    user_name, responses[lamina][response_number], lamina+1, response_number+1))

                self.process_popular(lamina+1, responses[lamina][response_number], response_number)
                self.process_zscore(lamina+1, responses[lamina][response_number], response_number)

        print(self._location)

    def process_zscore(self, lamina, response, response_number):
        zscore = '?'
        adjacent_areas_lamina2_d0 = ["animales", "camarones", "animal"]
        distant_areas_lamina2_d1 = ["vegetacion", "algas", "ojos verdes"]
        adjacent_areas_lamina3_d2 = ["persona", "humano", "hombre", "mujer", "niño", "niña", "chico", "chica", "señor", "señora", "personas", "humanos", "hombres", "mujeres", "niños", "niñas", "chicos", "chicas", "señores", "señoras", "payaso", "payasos", "hada",
                "hadas", "bruja", "brujas", "fantasma", "fantasmas", "demonio", "demonios", "ángel", "ángeles", "humanoide", "humanoides", "caricaturas", "caricatura", "monstruo", "monstruos"]      
        distant_areas_lamina3_d1 = ["duendes", "enanos", "gnomos", "indios", "aborigenes", "muñecos"]
        
        if 'F' in self._determinantes[lamina-1][response_number] and self._location[lamina-1][response_number] == 'W' and self._dq[lamina-1][response_number] != 'v':
            zscore = 'ZW'

        if zscore == '?' and ('M' in self._determinantes[lamina-1][response_number] or 'm' in self._determinantes[lamina-1][response_number] or 'ind' in self._determinantes[lamina-1][response_number]):
            if lamina == 2:
                for area in adjacent_areas_lamina2_d0:
                    if area in response and self._location[lamina-1][response_number] == 'D0':
                        zscore = 'ZA'
                        break
                if zscore == '?':
                    for area in distant_areas_lamina2_d1:
                        if area in response and self._location[lamina-1][response_number] == 'D1':
                            zscore = 'ZD'
                            break

            if zscore == '?' and lamina == 3:
                for area in adjacent_areas_lamina3_d2:
                    if area in response and (self._location[lamina-1][response_number] == 'D2' or self._location[lamina-1][response_number] == 'W'):
                        zscore = 'ZA'
                        break
                if zscore == '?':
                    for area in distant_areas_lamina3_d1:
                        if area in response and self._location[lamina-1][response_number] == 'D1':
                            zscore = 'ZD'
                            break

        if zscore == '?' and 'S' in self._location[lamina-1][response_number]:
            zscore = 'ZS'

        self._zscore[lamina-1].append(zscore)

