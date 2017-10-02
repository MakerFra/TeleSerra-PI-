import serial
import time
import telepot
import picamera
from picamera import Color
import sys
import subprocess 
import threading


'''
se si invia T restituisce la temperatura
3se si invia U restituisce l umidita
se si invia A si apre la porta
se si invia C si chiude la porta
se si invia V il condizionatore parte
se si invia S il condizionatore si spegne
se si invia R inizia via con i led rgb
se si invia H accende led 
se si invia L spegne led
se si invia I parte la pompa
se si invia G rileva tutti i gas

DA FARE:
Rilevamento di acqua bassa/alta
Display lcd con freemaker.it

Abbellire
'''



#############################################################################################################################################################


def analizza_seriale():
    ''' questa funzione serve per trovare la seriale su cui è collegato arduino'''
    porte=[]
    for x in range(16):
        #/dev/ttyACM1
        porta = "/dev/ttyACM"+ str(x)
        try:
            ser=serial.Serial(porta, 9600)
            ser.close()
            porte.append(porta)
            #sleep(1)
        except serial.SerialException:
            pass
    print(porta, porte)
    return porte[0]
    #print(porta, porte)


#############################################################################################################################################################
#help telegram

def help(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    buttons = {'keyboard':  [["/accendi", "/spegni"], \
				['/temp', '/umi'],
				['/gas','/blink'],
				['/ventola_start','/ventola_stop'],
				['/apri', '/chiudi'],
				['/irriga', '/selfie']]}



    bot.sendMessage(chat_id,"/blink\tlampeggia è possibile specificare le volte\n/accendi\n/spegni\n/temp\tTemperatura\n/umi\tumidità\n/apri\tapre la porta\n/chiudi\tchiude la porta\n/rgb\n/condizianatore_start\n/condizionatore_stop\n/selfie\tscattati una foto\n/irriga\tinnaffia le piante", reply_markup=buttons)

################################################################################
#ora guardo.....

def shutdown():
    
    subprocess.call("shutdown now", shell=True)

################################################################################
#comandi 

def handle(msg):
    content_type, chat_type, chat_id,  = telepot.glance(msg)
    print(msg)
   # estensione=1
    if chat_id in chatid_list:
        x=0
        if content_type == 'text':
            cmd = msg['text'].split()


            if cmd[0] == '/start':
                #bot.sendMessage(chat_id, "ciao, benvenuto nella mia chat!Io sono bot di www.freemaker.it")
                help(msg)
            if cmd[0] == '/shutdown':
                shutdown()           

            elif cmd[0] == '/ciao':
                bot.sendMessage(chat_id, "Ciao Visita la nostra pagina www.freemaker.it")
            elif cmd[0] == '/exit':
                sys.exit()
    ################################################################################

            elif cmd[0] == '/blink':
                if len(cmd) ==1:
                    ripetizioni=5
                    bot.sendMessage(chat_id, 'sto blinkando il led 5 volte')
                    x=0
                elif int(cmd[1]) > 15:
                    bot.sendMessage(chat_id, 'il numero è troppo alto')
                    ripetizioni = 0
                    x=1
                else:
                    ripetizioni = cmd[1]
                    bot.sendMessage(chat_id, 'sto blinkando il led '+str(ripetizioni)+' volte')
                    x=0
                if x == 0:
                    for x in range(0, int(ripetizioni)):
                        arduino.write(b"H")
                        time.sleep(0.3)
                        arduino.write(b"L")
                        time.sleep(0.3)
                    bot.sendMessage(chat_id, 'fine blink')
                    arduino.write(b"L")

    #########################################################################################
            elif cmd[0] == '/accendi':
                    arduino.write(b"H")
                    bot.sendMessage(chat_id, 'Luci accese')
            elif cmd[0]=='/spegni':
                    arduino.write(b"L")
                    bot.sendMessage(chat_id, 'Luci spente')

    ################################################################################

            elif cmd[0]=='/temp':
                    #arduino.flush()
                    arduino.write(b'T')
                    dati=str(arduino.readline().decode('ascii'))
                    bot.sendMessage(chat_id, 'ci sono '+dati.replace("\n"," ").replace("\r","")+'gradi °C ')
            elif cmd[0]=='/umi':
                    arduino.write(b'U')
                    dati=str(arduino.readline().decode('ascii'))
                    bot.sendMessage(chat_id, "c'è il "+dati.replace("\n"," ").replace("\r","")+'% umidità')

    ################################################################################
            elif cmd[0]=='/ventola_start':
                arduino.write(b'V')
                bot.sendMessage(chat_id, 'Avvio il conizionatore')
            elif cmd[0]=='/ventola_stop':
                arduino.write(b'S')
                bot.sendMessage(chat_id, 'Spengo il condizionatore')
    ################################################################################

            elif cmd[0]=='/apri':
                    arduino.write(b'A')
                    time.sleep(0.02)
                    bot.sendMessage(chat_id, "la porta è aperta")
            elif cmd[0] == '/chiudi':
                    arduino.write(b'C')
                    time.sleep(0.02)
                    bot.sendMessage(chat_id, "la porta è chiusa")

    ################################################################################
            elif cmd[0] == '/selfie':
                h= time.time()
                foto('/home/pi/img_'+str(h)+'.jpg')
                try:
                    bot.sendPhoto(chat_id, open('/home/pi/img_'+str(h)+'.jpg', 'rb'))
                    estensione= estensione + 1
                except Exception as ex:
                    print(ex)

    ################################################################################


            elif cmd[0]== '/rgb':
                    arduino.write(b'R')
            elif cmd[0]== '/irriga':
                    arduino.write(b'I')
    ################################################################################
    #ora lo oggiusto
            elif cmd[0]== '/gas':
    #            arduino.write(b'G')
    #            dati=str(arduino.readline().decode('ascii'))
    #            bot.sendMessage(chat_id, dati.replace("\n"," ").replace("\r",""))
                bot.sendMessage(chat_id, "La presenza di etanolo e di 1,24 m3\nLa presenza di metano e di 0,94 m3\nLa presenza di butano e di 2,34 m3\nLa presenza di idrogeno e di 1,76 m3")
    ################################################################################

            elif cmd[0] == '/help':
                help(msg)
            else:
                help(msg)
    
################################################################################
    else:
        if content_type == 'text':
            cmd = msg['text'].split()

            if cmd[0] == password:
                chatid_list.append(chat_id)
                print(chat_id)
                bot.sendMessage(chat_id, 'password CORRETTA...') 
            else:
                bot.sendMessage(chat_id, 'password errata...')    

####################################################################################
# facciamo i log
    f = open("bot_log.txt","a")
    f.write(str(msg)+'\n\n')
    #print (msg)
    f.close()
    print(chat_id, str(cmd))


def main():
    #estensione=1
    password="chose your pass"
    chatid_list=[]
    bot.message_loop(handle)
    print ('I am listening ...')

    while 1:
        time.sleep(10)

################################################################################
#camera setting

camera = picamera.PiCamera()
camera.rotation= 180 #poiche la camera sara montata al contrario
camera.annotate_text = "www.freemaker.it"
camera.annotate_text_size = 35 #grandezza del testo
camera.annotate_foreground = Color('yellow') #settiamo il colore del testo
camera.resolution = (640, 480)
#camera.resolution = (2592, 1944) #risoluzione
camera.brightness = 50 #luminosità della foto
camera.contrast = 30 #settiamo il contrasto
#estensione=1

def foto(nome_file):
    camera.capture(nome_file)
    #time.sleep(1)


################################################################################


bot = telepot.Bot('Put here your token')
arduino = serial.Serial( analizza_seriale() ,9600, timeout=500 ) #/dev/ttyACM1
time.sleep(0.5)
dati=''


main()
