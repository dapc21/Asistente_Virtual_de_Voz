import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'
id2 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'
id3 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0'


# escuchar microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzó la grabación
        print("Ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en Google
            pedido = r.recognize_google(audio, language="es-ve")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendió el audio
            print("Ups, no entendí.")

            # Devolver error
            return "Sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendió el audio
            print("Ups, no hay servicio.")

            # Devolver error
            return "Sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendió el audio
            print("Ups, algo ha salido mal.")

            # Devolver error
            return "Sigo esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id3)

    # pronunciar el mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el día de la semana
def pedir_dia():
    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombre de días
    calendario = {
        0: 'Lunes',
        1: 'Martes',
        2: 'Miércoles',
        3: 'Jueves',
        4: 'Viernes',
        5: 'Sábado',
        6: 'Domingo'
    }

    # decir día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# informar qué hora es
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas, con {hora.minute} minutos y {hora.second} segundos'
    print(hora)

    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(f'{momento}, soy Helena, tu asistente personal. Por favor, dime en qué te puedo ayudar?')


# Funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    global resultado
    saludo_inicial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en Wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            pedido = pedido.strip()  # Eliminar espacios extra
            resultado = ""

            if pedido:  # Verificar que hay algo que buscar
                wikipedia.set_lang('es')
                try:
                    resultado = wikipedia.summary(pedido, sentences=1)
                    hablar("Wikipedia dice lo siguiente:")
                    hablar(resultado)
                except wikipedia.exceptions.DisambiguationError as e:
                    hablar("Hay varias opciones para esa búsqueda. Sé más específico.")
                    print(f"Error de ambigüedad: {e}")
                except wikipedia.exceptions.HTTPTimeoutError:
                    hablar("Hubo un problema de conexión. Intenta de nuevo.")
                except wikipedia.exceptions.PageError:
                    hablar("No encontré información sobre eso en Wikipedia.")
                except wikipedia.exceptions.WikipediaException as e:
                    hablar("Hubo un problema con Wikipedia. Intenta de nuevo.")
                    print(f"Error de Wikipedia: {e}")
                except Exception as e:
                    hablar("Ocurrió un error inesperado.")
                    print(f"Error inesperado: {e}")
                continue
            else:
                hablar("No especificaste qué buscar en Wikipedia.")
            continue
        elif "busca en internet" in pedido:
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            continue
        elif 'reproducir' or 'reproduce' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" or 'broma' in pedido:
            chiste = pyjokes.get_joke("es", "all")
            hablar(chiste)
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {
                'apple':'APPL',
                'amazon':'AMZN',
                'google':'GOOGL'
            }

            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, no la he encontrado.')
                continue
        elif 'adiós' in pedido or 'chao' in pedido or 'hasta luego' in pedido:
            hablar('Hasta luego, fue un placer haberte ayudado, ¡vuelve pronto!')
            break
        else:
            hablar('No entendí lo que dijiste. Puedes repetir?')
            continue

pedir_cosas()

