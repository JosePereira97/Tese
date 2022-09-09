#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
from flask import Flask, request
from werkzeug.datastructures import FileStorage, ImmutableMultiDict
from flask_cors import CORS
import os
import json
import glob
import requests
import snakemake
import argparse
import sys
import json
import yaml
from time import gmtime, strftime, time
import shutil
import zipfile

__version__ = '1.6.0'

app = Flask(__name__)
CORS(app)

class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name, method):
        f = open(file_name, method)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))

@app.route('/run_MOSCA full workflow', methods = ['POST'])
def run_MOSCA ():
    the_file = request.form.to_dict(flat=False)
    conf = the_file['config']
    Great_List = json.loads(the_file['Workflow'][0])
    if os.path.isdir('./input') == False: 
        os.makedirs('./input')
    for i in request.files:
        teste = request.files[i]
        with open(f"./input/{teste.filename}","wb") as binary_file:
            binary_file.write(teste.read())
        binary_file.close()
    with open("./input/config.json",'w') as config:
        config.write(str(conf).replace("['", "").replace("']",""))
    config.close()
    parser = argparse.ArgumentParser(description="MOSCA's main script")
    parser.add_argument("-s", "--snakefile", default=f'{sys.path[0]}/Snakefile', help="Snakefile file")
    parser.add_argument(
        "-c", "--configfile", default='./input/config.json',
        help="Configuration file for MOSCA (JSON or YAML). Obtain one at https://iquasere.github.io/MOSGUITO")
    parser.add_argument(
        '--unlock', action='store_true', default=False,
        help='If user forced termination of workflow, this might be required')
    parser.add_argument('-v', '--version', action='version', version=f'MOSCA {__version__}')
    args = parser.parse_args()


    def read_config(filename):
        if filename.split('.')[-1] == 'yaml':
            with open(filename) as stream:
                try:
                    return yaml.safe_load(stream), 'yaml'
                except yaml.YAMLError as exc:
                    print(exc)
        elif filename.split('.')[-1] == 'json':
            with open(filename) as f:
                return json.load(f), 'json'
        else:
            exit('Config file must end in either ".json" or ".yaml"')


    def save_config(config_data, filename, output_format):
        with open(filename, 'w', encoding='utf-8') as f:
            if output_format == 'json':
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            elif output_format == 'yaml':
                yaml.dump(config_data, f, ensure_ascii=False, indent=2)
            else:
                return NotImplementedError


    def human_time(seconds):
        days = seconds // 86400
        if days > 0:
            return strftime(f"{days}d%Hh%Mm%Ss", gmtime(seconds))
        return strftime("%Hh%Mm%Ss", gmtime(seconds))
    start_time = time()

    config, config_format = read_config(args.configfile)
    pathlib.Path(config["output"]).mkdir(parents=True, exist_ok=True)
    save_config(config, f'{config["output"]}/config.json', output_format=config_format)
    print(Great_List)
    for analyses in Great_List: #it works
        print(analyses)
        Result = snakemake.main(
            f"-s {args.snakefile} --until {analyses} --printshellcmds --cores {config['threads']} --configfile {args.configfile} -p"
            f"{' --unlock' if args.unlock else ''}")
        

    print(f'MOSCA analysis finished in {human_time(time() - start_time)}')

    shutil.make_archive('output_results', 'zip', 'output')
    shutil.rmtree('input')
    shutil.rmtree('output')
    
    my_class = OpenFiles()
    el_file = FileStorage(my_class.open('output_results.zip', 'rb'))
    output = {'output_results': el_file}
    data = {'Analyses_name': f'{config["name"]}', 'parent_User_id':'Great_user@tester.com'}
    response = requests.post('http://192.168.1.99:5000/Save_Output_Files', verify=False,data=data, files=output)
    
    my_class.close()
    os.remove('output_results.zip')
    return('Funcionou wow')
            
if __name__ == '__main__':
    app.run(port=5003)