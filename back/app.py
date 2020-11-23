#!/usr/bin/python
# -*- coding: utf-8 -*-

# Imports
from flask import Flask, jsonify, request, url_for, json
from flask_cors import CORS
from flask_socketio import SocketIO
from subprocess import check_output
from ADC import ADCSPI
import threading
import time
from RPi import GPIO
import requests
import serial

# Custom imports
from database.Database import Database
from LCD import lcd
from Tempclass import tempSensor

# Start app
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
light =ADCSPI(10**5)
sensor_address = "28-00000aee6af2"
sensor = tempSensor()
GPIO.setmode(GPIO.BCM)
buzzer = 27
GPIO.setup(buzzer, GPIO.OUT)
conn = Database(app=app, user='root', password='Berend2802', db='smartfridge')
api_key = "AC939DFDCBCA58BD57DF47EF508DE3B8" #https://upcdatabase.org/



# Custom endpoint
endpoint = '/api/v1'


def get_ip():
    ips = check_output(['hostname', '--all-ip-addresses'])
    ip = str(ips).split(' ', 1)[-1].split(' ', 1)[0]
    return ip

def data_to_lcd():
    lcd1 = lcd()
    sensor = tempSensor()
    sensor_address = "28-00000aee6af2"

    time.sleep(20)
    lcd1.init_LCD()
    lcd1.write_message(str(get_ip()))

    while True:
        lcd1.second_row()
        temp = round(sensor.read_temprature(sensor_address),1)
        lcd1.write_message(str(temp))
        lcd1.send_character(223)
        lcd1.write_message("C ")

def temp_to_db(unit="C", sound=1):
    while True:
        conn.set_data("INSERT INTO temperatureHistory values (NULL,%s,NULL,(SELECT idfridge FROM fridge where idfridge LIKE %s), %s, %s)",
                      [str(sensor.read_temprature(sensor_address)), 1, unit, sound])
        time.sleep(10)


def barcode():
    with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as port:
        while True:
            line = port.readline()
            strp_line = line.decode('utf-8')
            url = "https://api.upcdatabase.org/product/%s?apikey=%s" % (strp_line, api_key)

            headers = {
                'cache-control': "no-cache",
            }

            response = requests.request("GET", url, headers=headers)
            json_data = response.json()
            if "title" in json_data:
                print(json_data["title"])
                product = json_data["title"]
                if json_data["title"] == "":
                    product = json_data["description"]
                    if product == "":
                        product = "Naam niet gevonden"

                code = int(json_data["barcode"])
                product_in_db = conn.get_data("SELECT barcode FROM products where barcode = %s",[code])
                try:
                    if product_in_db[0] is not None:
                        conn.set_data("UPDATE fridge_has_products SET amount = amount+1 WHERE products_barcode = %s",[code])
                except IndexError:
                    conn.set_data("INSERT INTO products values(%s,%s)", [code, product])
                    conn.set_data(
                        "INSERT INTO fridge_has_products values((select idfridge from fridge where idFridge LIKE %s),%s,NULL,NULL,%s)",
                        [1, code, 1])



def open_detection():
    global fridge_open
    light_over_20_time = 0
    while True:
        light_level = light.return_light()
        if light_level >= 20:
            light_over_20_time += 1
        else:
            light_over_20_time = 0 # reset counter, too dark
            fridge_open = False

        if light_over_20_time >= 30:
            fridge_open = True
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(buzzer, GPIO.LOW)
            time.sleep(2)
            #light_over_20_time = 0  # reset counter
        time.sleep(1)

db = threading.Thread(target=temp_to_db)
db.start()
x = threading.Thread(target=data_to_lcd)
x.start()
bar = threading.Thread(target=barcode)
bar.start()
noise = threading.Thread(target=open_detection)
noise.start()

@app.route(endpoint + "/temperature_history" ,methods=["GET"])
def get_temp_history():
    if request.method == "GET":
        return jsonify(conn.get_data("SELECT temperature, time FROM temperatureHistory WHERE DATE(`time`) = CURDATE()"))

@app.route(endpoint + "/unit" ,methods=["GET","POST"])
def get_temp_unit():
    if request.method == "POST":
        data = request.get_json()["unit"]
        print(data)
    elif request.method == "GET":
        return jsonify(conn.get_data("SELECT tempUnit FROM temperatureHistory ORDER BY idtemperature DESC LIMIT 1"))

@app.route(endpoint + "/table", methods=["GET", "POST"])
def db_to_table():
    if request.method == "GET":
        antw_db = conn.get_data("SELECT f.products_barcode, f.date, f.expirationDate, f.amount, p.name FROM fridge_has_products AS f left join products AS p ON f.products_barcode = p.barcode ORDER BY f.date DESC")
        json_db = jsonify(antw_db)
        return json_db
    elif request.method == "POST":
        title = request.get_json()["htmlvalue"]
        amount_list = conn.get_data("SELECT f.amount FROM fridge_has_products AS f LEFT JOIN products AS p ON f.products_barcode = p.barcode WHERE name = %s", [title])
        code_list = conn.get_data("SELECT p.barcode FROM fridge_has_products AS f LEFT JOIN products AS p ON f.products_barcode = p.barcode WHERE name = %s", [title])
        amount_dict = amount_list[0]
        code_dict = code_list[0]
        amount = amount_dict.get("amount")
        code = code_dict.get("barcode")
        print(amount)
        print(code)
        if amount == 1:
            conn.set_data("DELETE FROM fridge_has_products WHERE products_barcode = %s",[code])
            conn.set_data("DELETE FROM products WHERE barcode = %s",[code])
        else:
            conn.set_data("UPDATE fridge_has_products SET amount = amount-1 WHERE products_barcode = %s",[code])
        return (jsonify(title))

@app.route(endpoint + "/app", methods={"GET", "POST"})
def barcode_from_app():
    if request.method == "GET":
        antw_db = conn.get_data("SELECT temperature from temperatureHistory order by idtemperature DESC LIMIT 1")
        return(jsonify(antw_db))
    if request.method == "POST":
        barcode = request.get_json()
        print(barcode)
        url = "https://api.upcdatabase.org/product/%s?apikey=%s" % (barcode, api_key)

        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers)
        json_data = response.json()
        print(json_data)
        if json_data['success'] == True:
            if "title" in json_data:
                print(json_data["title"])
                product = json_data["title"]
                if json_data["title"] == "":
                    product = json_data["description"]
                    if product == "":
                        product = "Naam niet gevonden"

            code = int(json_data["barcode"])
            product_in_db = conn.get_data("SELECT barcode FROM products where barcode = %s", [code])
            try:
                if product_in_db[0] is not None:
                    conn.set_data("UPDATE fridge_has_products SET amount = amount+1 WHERE products_barcode = %s",
                                  [code])
            except IndexError:
                conn.set_data("INSERT INTO products values(%s,%s)", [code, product])
                conn.set_data(
                    "INSERT INTO fridge_has_products values((select idfridge from fridge where idFridge LIKE %s),%s,NULL,NULL,%s)",
                    [1, code, 1])
            return (jsonify(json_data))
        else:
            return (jsonify(""))

@app.route(endpoint + "/app/amount", methods={"POST"})
def update_amount():
    if request.method == "POST":
        barcode = request.get_json()["barcode"]
        amount = str(request.get_json()["amount"])

        if int(amount) == 1:
            print("Already added a product! Nothing to be done...")
        elif int(amount) < 1:
            conn.set_data("DELETE FROM fridge_has_products WHERE products_barcode = %s", [barcode])
            conn.set_data("DELETE FROM products WHERE barcode = %s", [barcode])

        else:
            add_amount = int(amount) - 1
            conn.set_data("UPDATE fridge_has_products SET amount = amount + %s WHERE products_barcode = %s", [add_amount, int(barcode)])
        print(amount, barcode)
        return amount

@app.route(endpoint + "/app/fridge", methods={"GET"})
def open_or_closed():
    if request.method == "GET":
        return jsonify(fridge_open)

@app.route(endpoint + "/app/manual", methods={"GET","POST"})
def add_products_manually():
    if request.method == "POST":
        barcode = request.get_json()["barcode"]
        product = request.get_json()["title"]
        amount = request.get_json()["amount"]
        conn.set_data("INSERT INTO products values(%s,%s)", [barcode, product])
        conn.set_data(
            "INSERT INTO fridge_has_products values((select idfridge from fridge where idFridge LIKE %s),%s,NULL,NULL,%s)",
            [1, barcode, 1])
        conn.set_data("UPDATE fridge_has_products SET amount = amount + %s WHERE products_barcode = %s",
                      [amount, int(barcode)])
        return jsonify(barcode)




# @socketio.on("naarfrontend")
# def realtime_temp(unit):
#         if unit == "C":
#             temp_C = round(sensor.read_temprature(sensor_address),1)
#             socketio.emit("temp_terug", str(temp_C) + "°C")
#         elif unit == "F":
#             temp_F = round(sensor.read_temprature(sensor_address) * 1.8 + 32),1
#             socketio.emit("temp_terug", str(temp_F) + "°F")

@socketio.on("naarfrontend")
def realtime_temp():
    while True:
        socketio.emit("temp_terug", round(sensor.read_temprature(sensor_address),1))


# Start app
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
