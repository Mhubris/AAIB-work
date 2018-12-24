import matplotlib
matplotlib.use('Agg')
import socket
from struct import *
import struct
import sys
import MySQLdb
from PIL import Image
import re
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import pearsonr
from scipy.interpolate import spline
from scipy import signal
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import classify_example_randomforest_orange as classify_sample
import smooth
import process_data_AAIB2018 as my_pd
import os
from joblib import dump, load


print(" _________________________________________\n")
print("|___________________AAIB__________________|\n")
print("|_____________Bernardo Teixeira___________|\n")
print("|____________Miguel Neto Andrade__________|\n")
print("|_____________Sara Beatriz Lobo___________|\n")
print("|_________________________________________|\n")

print("A treinar o classificador...")
# classify example


#clf = classify_sample.get_fit()
#This function load our joblib file
clf = load('//home//pi//Desktop//AAIB_Project//training.joblib')
#classify_sample.get_confusion_matrix(clf)


# Open database connection
db = MySQLdb.connect("localhost","myuser","mypassword","mydb" )
# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Base de Dados mariaDB esta pronta")

#This is the TCP IP of our rpi
TCP_IP = '192.168.0.74'
TCP_PORT = 5005
BUFFER_SIZE = 8  # Normally 1024, but we want fast response

#Fields of connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(5)

#This fields are usefull to the execution of our server
matrix_with_uint8=[]
histogrms=""
signal=""
spect=""
spect=""
t, x, y, z=0,0,0,0
uniformTime, newX, newY, newZ=0,0,0,0



#Signal Fields
matrix_with_values=[]
result=[]

# This function return the last entry of our data-base
# It is important to store the pictures on apache directory
def get_last_id_db():
    sql = "SELECT id FROM Utilizadores ORDER BY id DESC LIMIT 1"
    try:
        # Execute the SQL command
        cursor.execute(sql)
        myresult = cursor.fetchone()
        if myresult == None:
            return 0
        else:
            return myresult[0]
    except:
        # Rollback in case there is any error
        db.rollback()

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

#Where we have the core of our server. It is a infinite loop
#that receive orders and execute tasks
while True:
    conn, addr = s.accept()

    #When cordova app makes a connection with server, address is displayed on
    #console
    print('Ip ', addr," conectou-se ao seu RPI")
    data = conn.recv(1).decode()
    firstbyte = unpack('b', data)

    #If the application send a byte with value of 0 it means that our server
    #will receive data from accelarometer
    if firstbyte[0] == 0:
        while 1:
            data = conn.recv(BUFFER_SIZE).decode()
            try:
                received = unpack('BBBBBBBB', data)
            except struct.error as err:
                break
            matrix_with_uint8.append(received)
            if received == (0, 0, 0, 0, 0, 0, 0, 0):
                matrix_with_uint8.pop() # Remove the last element of list becouse its the terminal byte

                # matrix_with_values are use
                matrix_with_values = [(line[0] * 100 + line[1],
                                       int((line[2] * 255 + line[3]) - 7800),
                                       int((line[4] * 255 + line[5]) - 7800),
                                       int((line[6] * 255 + line[7]) - 7800)) for line in matrix_with_uint8]

                tt, xx, yy, zz = my_pd.get_values_from_phone(matrix_with_values)
                t, x, y, z = my_pd.remove_duplicates(tt, xx, yy, zz)
                uniformTime, newX, newY, newZ = my_pd.uniform_time(t, x, y, z)

                t = uniformTime
                # Apply a smooth filter to remove peaks
                x, y, z = my_pd.smooth_signal(newX, newY, newZ, window_len=4)

                # extract features
                str_features = my_pd.get_tab_separated_features(t, x, y, z)
                # classify example -------------------------------------------------------------------------------------
                est_y = classify_sample.classify_ex_phone(clf, str_features)
                class_number = my_pd.get_class_number_from_letter(est_y)

                # The classifier returns our target, that its a value beteween 0 and 6
                if class_number == 0:
                    result=["Ficou Parado","0"]
                elif class_number == 1:
                    result=["Teste Invalido","1"]
                elif class_number == 2:
                    result=["Cadeira Eletrica","2"]
                elif class_number == 3:
                    result = ["Cadeira Manual","3"]
                elif class_number == 4:
                    result = ["Empurrado","4"]
                elif class_number == 6:
                    result = ["Use o nosso suporte","6"]
                else:
                    result=""

                matrix_with_uint8 = []
                break
    elif firstbyte[0] == 1:
        while 1:
            conn.send(result[0].encode())
            break
    elif firstbyte[0] == 2:
        while 1:
            data = conn.recv(30).decode('utf-8')
            dataSplited= data.split(";")

            sql = "INSERT INTO Utilizadores(name, \
                   age, weight, result) \
                   VALUES ('%s', '%d', '%d', '%d')" % \
                  (dataSplited[0], int(dataSplited[1]), int(dataSplited[2]), int(result[1]))
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Commit your changes in the database
                db.commit()
                id=get_last_id_db()
                # plot signal (x, y, z) and smooth signal (newX, newY, newZ) in uniform time
                my_pd.get_signal_figure(t, x, y, z, newX, newY, newZ, save_fig=True,
                                        file_name="//var//www//html//images//plot_signals" + str(id) + ".jpg",
                                        length_inches=9.2, width_inches=2.0)

                # x, y and z spectrogram -------------------------------------------------------------------------------
                my_pd.get_spectrograms_figure(t, x, y, z, save_fig=True,
                                              file_name="//var//www//html//images//spectrograms" + str(id) + ".jpg",
                                              length_inches=9.2, width_inches=4.0)

                # histograms -------------------------------------------------------------------------------------------
                my_pd.get_histograms_figure(t, x, y, z, save_fig=True,
                                            file_name="//var//www//html//images//histograms" + str(id) + ".jpg",
                                            length_inches=9.2, width_inches=4.0)
            except:
                # Rollback in case there is any error
                db.rollback()
            break

