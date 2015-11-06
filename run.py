from flask import Flask, request, render_template, url_for, redirect
import time
import threading
import csv
import pandas as pd

app = Flask(__name__)

global now
sensors  = {1: "28-04146f9f0eff", 2: "28-04146f98b6ff", 3:"28-04146f99b1ff", 4:"28-04146f91d2ff", 5:"28-04146f9898ff"}    
temperatures = {1:0, 2:0, 3:0, 4:0, 5:0 }
desviations = {1:0.4, 2:0.5, 3:0.35, 4:0.2, 5:0.3 }

def read_temperature(sensorID):
    
    tempfile = open("/sys/bus/w1/devices/"+sensors[sensorID]+"/w1_slave")
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    return temperature

@app.route("/")
def getTemperatures():
    return render_template('temps.html', t=temperatures)

@app.route("/logs")
def getLogs():
    return redirect(url_for('static', filename=now+".txt"))

@app.route("/csvlogs")
def getCSVLogs():
    return redirect(url_for('static', filename=now+".csv"))

@app.route("/graphs")
def getGraphs():
    df = pd.read_csv("static/"+now+".csv", sep=';')
    sensor1 = df["Sensor 1"].tolist()
    sensor2 = df["Sensor 2"].tolist()
    sensor3 = df["Sensor 3"].tolist()
    sensor4 = df["Sensor 4"].tolist()
    sensor5 = df["Sensor 5"].tolist()
    print (sensor1)
    return render_template('graphs.html', s1=sensor1, s2=sensor2, s3=sensor3, s4=sensor4, s5=sensor5 )

class main(threading.Thread):
    def run(self):
        while True:
            for id in sensors.keys():
                temperatures[id]=read_temperature(id)+desviations[id]
            time.sleep(5)

class datalogger(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        global now
        now = time.strftime("%c")

    def run(self):
        global now
        while True:
            file = open("static/"+now+".txt",'a')
            file.write("_________________________________________\n")
            file.write("\n ")
            file.write(time.strftime("%c")+"\n")
            file.write("_________________________________________\n")
            file.write("Temperatura sensor 1 : "+str(temperatures[1])+"\n")
            file.write("Temperatura sensor 2 : "+str(temperatures[2])+"\n")
            file.write("Temperatura sensor 3 : "+str(temperatures[3])+"\n")
            file.write("Temperatura sensor 4 : "+str(temperatures[4])+"\n")
            file.write("Temperatura sensor 5 : "+str(temperatures[5])+"\n")
            file.write("_________________________________________\n")
            file.close()
            time.sleep(60)

class CSVdatalogger(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        global now
        file = open("static/"+now+".csv",'ab')
        csvwriter = csv.writer(file,dialect='excel', delimiter=';',quoting=csv.QUOTE_NONE)
        csvwriter.writerow(["Data"]+["Sensor 1"]+["Sensor 2"]+["Sensor 3"]+["Sensor 4"]+["Sensor 5"])
        file.close()

    def run(self):
        global now
        while True:
            file = open("static/"+now+".csv",'ab')
            csvwriter = csv.writer(file,dialect='excel', delimiter=';',quoting=csv.QUOTE_NONE)
            csvwriter.writerow([time.strftime("%c")]+[str(temperatures[1])]+[str(temperatures[2])]+[str(temperatures[3])]+[str(temperatures[4])]+[str(temperatures[5])])
#            csvwriter.writerow(["Sensor 1"])
 #           csvwriter.writerow(["Sensor 2"]+ [str(temperatures[2])])
  #          csvwriter.writerow(["Sensor 3"]+ [str(temperatures[3])])
   #         csvwriter.writerow(["Sensor 4"]+ [str(temperatures[4])])
    #        csvwriter.writerow(["Sensor 5"]+ [str(temperatures[5])])
            file.close()
            time.sleep(60)


if __name__ == "__main__":
    myMain = main()
    myMain.daemon=True
    myMain.start()
    time.sleep(5)
    myDatalogger = datalogger()
    myDatalogger.daemon=True
    myDatalogger.start()
    myCSVDatalogger = CSVdatalogger()
    myCSVDatalogger.daemon=True
    myCSVDatalogger.start()
    app.run(host='0.0.0.0', port=1234,threaded=True, debug=True)   

