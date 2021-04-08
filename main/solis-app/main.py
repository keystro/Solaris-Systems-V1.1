#!/usr/bin/env python3
#!flask/bin/python3
from flask import Flask, request, jsonify
#from flask_login import LoginManager
import secrets, time




app = Flask(__name__)



@app.route('/')
@app.route('/login')
def login():
    return "Login User"

@app.route('/logout')
def logout():
    return "logout User"

@app.route('/home', methods=['POST'])
def home():
    json_data = request.get_json()
    print(json_data)
    return jsonify(json_data)


@app.route('/esp_mount')
def esp_mount():
    return jsonify({'Mode':'Primary/Secondary/Auxillary',
                    'Watts produced/Hr': '1000kW/0KW',
                    'Watts consumed/Hr': '600KW',
                    'Rate of battery charging/discharing':'200KW/hr',
                    'Battery %': '60%',
                    'Battery Temperature':'23.7',
                    'Internal Device Temperature': '36.8',
                    'Cooling Fan': 'On/Off'})

@app.route('/generate_key')
def generate_key():
    Api_Key = secrets.token_hex(16)
    return jsonify({'API_Key': Api_Key })

@app.route('/generate_device_ID')
def generate_device_ID():
    Device_ID = secrets.token_hex(8)
    return jsonify({'IoT_Device_ID': Device_ID})

@app.route('/local_time')
def local_time():
    timestamp = time.asctime(time.localtime(time.time()))
    return jsonify({'local_time': timestamp})

@app.route('/switch_power_states')
def switch_power_states():
    return jsonify({'Power_Mode': 'Primary/ Secondary/ Auxillary'})

@app.route('/switch_fan')
def switch_fan():
    return jsonify({'State': 'On/ Off'})

@app.route('/reset_device')
def reset_device():
    return "Initiate Reboot Sequence ******* "

@app.route('/self_diagnosis')
def self_diagnosis():
    return "Initiate Self Diagnostic Sequence ******* "

@app.route('/download_remote_data')
def download_remote_data():
    return jsonify({'1':'Enter user_admin password .....',
                    '2':'User validation successful',
                    '3':'Compressing remote data',
                    '4':'Download in ....5/',
                    '5':'....4/',
                    '6':'....3/',
                    '7':'....2/',
                    '8':'....1'})

@app.route('/wipe_remote_drive')
def wipe_remote_drive():
    return jsonify({'1':'User_admin password required .....',
                    '2':'User validation successful',
                    '3':'Please confirm that User wishes to wipe remote drive',
                    '4':'Wiping remote drive in ....5/',
                    '5':'....4/',
                    '6':'....3/',
                    '7':'....2/',
                    '8':'....1'})

@app.route('/print_stats')
def print_stats():
    return "Printing Data Stats, Preiod(14/01/2021- 14/03/2021) ...... /"



if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.104', port = 8090)
