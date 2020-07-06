#!/usr/bin/python3
# For making scheduled updates to a salesforce environment
# Accepts one command line argument of a directory string that os recognizes
# Iterates through directory and processes each json file found
# Intended to be run on an hourly cron

import os
import sys
import json
import datetime
import simple_salesforce
from simple_salesforce import Salesforce

os.chdir(sys.argv[1])
now = datetime.datetime.now()
now_string = now.isoformat()
now_string = now_string.replace(':','-')
now_string = now_string.replace('.','_')

#Prepare logging
try:
    log_name = 'log_' + now_string + '.txt'
    log_file = os.path.join(os.getcwd(), 'logs', log_name)
    if (not os.path.exists('logs')):
        os.makedirs('logs')
    if (not os.path.exists('done')):
        os.makedirs('done')
    with open(log_file, 'a') as log:
        log.write(f'Starting Update Engine: {now.isoformat()}\n\n')
except Exception as e:
    print(f'Unable to initialize logging: {e}')

#Get list of json files in directory
try:
    dir_list = [f for f in os.listdir() if f.endswith('.json')]
    if (not dir_list):
        with open(log_file,'a') as log:
            log.write(f'No JSON files in target directory {os.getcwd()}\n\n')
except Exception as e:
    with open(log_file, 'a') as log:
        log.write(f'Directory error: {e}')
        exit()

#Auth SFDC session
try:
    with open('sfdc_creds.json', 'r') as read_file:
        creds = json.load(read_file)
except Exception as e:
    with optn(log_file, 'a') as log:
        log.write(f' Failed to load credentials\n{e}')
        exit()

try:
    sf = Salesforce(username=creds['user'], password=creds['pass'], 
    security_token=creds['toke'])
except Exception as e:
    with open(log_file, 'a') as log:
        log.write(f'Failed to initialize salesforce session!\n{e}')
        #TODO email notification to person maintaining this script?
        exit()

#Main loop
for file_location in dir_list:
    try:
        with open(file_location) as read_file:
            input_data = json.load(read_file)
    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(f'{file_location}: Could not read file\n')
            log.write(str(e) + '\n\n')
            continue
    #One Time Updates
    try:
        if (input_data['main_type'] == 'once'):
            update_datetime = datetime.datetime.fromisoformat(
                input_data['datetime'])
            if (
                update_datetime.date() == now.date() and 
                update_datetime.hour == now.hour):
                results = sf.bulk.__getattr__(
                    input_data['object_type'])._bulk_operation(
                    object_name=input_data['object_type'], 
                    operation=input_data['operation'],
                    data=input_data['data'])
                if (not False in [x['success'] for x in results]):
                    os.rename(file_location, os.path.join(
                        'done',file_location))
                with open(log_file,'a') as log:
                    log.write(f'Processing file: {file_location}\n')
                    log.write(f'Frequency: {input_data["main_type"]} '
                    f'Operation: {input_data["operation"]} '
                    f'Object Type: {input_data["object_type"]}\nResults:\n')
                    log.write(str(results))
                    log.write('\n\n')
            else:
                with open(log_file, 'a') as log:
                    log.write(
                        f"{file_location}: Update day/time doesn't match, "
                        "skipped\n\n")
        #Rotations
        elif (input_data['main_type'] == 'rotation'):
            active = 0
            action = 0
            update_day = input_data['day']
            update_time = datetime.time.fromisoformat(input_data['time'])
            if (
                update_day == now.isoweekday() and
                update_time.hour == now.hour):
                #Determine active chunk
                for x in range(len(input_data['chunks'])):
                    if (input_data['chunks'][x]['active'] == 1):
                        if (x == len(input_data['chunks']) - 1):
                            action = 0
                            active = x
                        else:
                            action = x + 1
                            active = x
                #Do update
                results = sf.bulk.__getattr__(
                    input_data['object_type'])._bulk_operation(
                    object_name=input_data['object_type'], 
                    operation=input_data['operation'],
                    data=input_data['chunks'][action]['data'])
                #Change active chunk and write back to file
                if (not False in [x['success'] for x in results]):
                    input_data['chunks'][active]['active'] = 0
                    input_data['chunks'][action]['active'] = 1
                    with open(file_location, 'w') as writefile:
                        json.dump(input_data, writefile)
                with open(log_file,'a') as log:
                    log.write(f'Processing file: {file_location}\n')
                    log.write(f'Frequency: {input_data["main_type"]} '
                    f'Operation: {input_data["operation"]} '
                    f'Object Type: {input_data["object_type"]}\nResults:\n')
                    log.write(str(results))
                    log.write('\n\n')
            else:
                with open(log_file, 'a') as log:
                    log.write(
                        f"{file_location}: Update day/time doesn't match, "
                        "skipped\n\n")
        #TODO future main_type options
    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(
                f'{file_location}: Format of JSON data does not meet '
                f'expectations\n{e}\n\n')

with open(log_file, 'a') as log:
    log.write(f'Process Complete: {datetime.datetime.now().isoformat()}')


