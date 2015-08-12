from flask import Flask, request, render_template, url_for, redirect
import time
import threading

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
def hello():
    #logs=" "
    #with open("/static"+now+'.txt','r') as file:
    #    for line in file:
    #        logs = logs + line +"\n"
    #return logs
    return redirect(url_for('static', filename=now+".txt"))

class main(threading.Thread):
    def run(self):
        while True:
            for id in sensors.keys():
                temperatures[id]=read_temperature(id)+desviations[id]

            #print("_________________________________________")
            #print(" ")
            #print("Temperatura sensor 1 : "+str(temperatures[1]))
            #print("Temperatura sensor 2 : "+str(temperatures[2]))
            #print("Temperatura sensor 3 : "+str(temperatures[3]))
            #print("Temperatura sensor 4 : "+str(temperatures[4]))
            #print("Temperatura sensor 5 : "+str(temperatures[5]))
            #print("_________________________________________")
            time.sleep(5)

class datalogger(threading.Thread):
    
    def __init__(self):
        global now
        threading.Thread.__init__(self)
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


if __name__ == "__main__":
    myMain = main()
    myMain.start()
    myDatalogger = datalogger()
    myDatalogger.start()
    app.run(host='0.0.0.0', port=1234,threaded=True, debug=True)   

