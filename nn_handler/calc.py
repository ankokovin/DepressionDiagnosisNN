#nn_handler/calc.py
from nn_handler.net import Net
from nn_handler.field import Field, FieldType, QField, QFieldChoice, QFieldNumeric, FieldCalc
import torch 
import json
import hashlib
import os
import csv
import datetime


"""Модуль управления моделями"""

state_filepath = os.getcwd()+'/models/state.json'
models_state = {}

main_model = None
main_model_fields = []
main_model_fields_data = []
main_model_out = {}

def set_main(model_uuid):
    """
    Установка модели как главной.
    Аргументы:

    model_uuid  --- str, id модели
    """
    if not isinstance(model_uuid, str):
        raise ValueError('На вход ожидалось str')
    
    if model_uuid not in models_state['models']:
        raise ValueError('Модель с таким идентификатором не была загружена')
    models_state['main_model'] = model_uuid
    save_state()
    load_main_model()


def load_model(model_uuid):
    """
    Загрузка модели из файловой системы.
    Аргументы:

    model_uuid  --- str, id модели
    """
    file_path = os.getcwd()+'/models/'+model_uuid
    md5_hash = hashlib.md5()
    with open(file_path+'/model_info.json', 'rb') as json_file:
        model_info_content = json_file.read()
    md5_hash.update(model_info_content)
    md5_hash_model_info = md5_hash.hexdigest()
    md5_hash = hashlib.md5()
    with open(file_path+'/model_data.pt', 'rb') as data_file:
        model_data_content = data_file.read()
    md5_hash.update(model_data_content)
    md5_hash_model_data = md5_hash.hexdigest()

    name = None
    with open(file_path+'/model_info.json') as json_file:
        obj = json.load(json_file)
        name = obj['name'] if 'name' in obj else model_uuid
            

    if 'models' in models_state:
        for val in models_state['models'].values():
            if val['model_data'] == md5_hash_model_data and val['model_info'] == md5_hash_model_info:
                delete_model(file_path)
                return False
    else:
        models_state['models'] = {}
    models_state['models'][model_uuid] = {
        'name': name,
        'model_data': md5_hash_model_data,
        'model_info': md5_hash_model_info
    }
    save_state()
    return True   
    
def save_state():
    """Сохранить текущее состояние моделей"""
    with open(state_filepath, 'w') as outp:
        json.dump(models_state, outp)
    
def delete_model(file_path):
    """
    Удалить модель из файловой системы.

    Аргументы:

    model_uuid  --- str, id модели
    """
    os.remove(file_path+'/model_info.json')
    os.remove(file_path+'/model_data.pt')
    os.removedirs(file_path)

def load_main_model():
    """Загрузить основную модель для вычислений"""
    global main_model
    global main_model_fields
    global main_model_fields_data
    global main_model_out 
    main_model = None
    main_model_fields = []
    main_model_fields_data = []
    main_model_out = {}
    if not 'main_model' in models_state:
        return
    path = os.getcwd()+'/models/'+models_state['main_model']
    with open(path+'/model_info.json','r') as inp:
        model_info = json.load(inp)
    Field.clear_field_list()
    input_cnt = 0
    if 'out' in model_info:
        main_model_out = model_info['out']
    else:
        main_model_out = {
            'mean': 0,
            'std': 1
        }
    for column in model_info['columns']:
        t = FieldType[column['type']]
        field = None
        ignore = 'ignore' in column and column['ignore'] == True
        if t == FieldType.choice:
            if 'separate' in column:
                separate = column['separate']
            else:
                separate = isinstance(column['answers'], list)
            if 'question' in column:
                question = column['question']
            else:
                question = column['name']
            
            if not ignore:
                if separate:
                    input_cnt += len(column['answers'])
                else:
                    input_cnt += 1
            field = QFieldChoice(column['name'],ignore,question,separate,column['answers'])
            main_model_fields_data.append({
                    'field_type':int(t),
                    'name':column['name'],
                    'question':question,
                    'answers':column['answers'] if separate else list(column['answers'].keys())
                    })
        elif t == FieldType.numeric:
            field = QFieldNumeric(column['name'],ignore,column['question'],column['mean'],column['std'])
            main_model_fields_data.append({
                    'field_type':int(t),
                    'name':column['name'],
                    'question':column['question']
                    })
            if not ignore:
                input_cnt += 1
        elif t == FieldType.calc:
            field = FieldCalc(column['name'],ignore,column['code'],column['mean'],column['std'])
            if not ignore:
                input_cnt += 1
        main_model_fields.append(field)

    main_model = Net(model_info['model']['hidden_cnt'],input_cnt,1, model_info['model']['act_function']).to(Net.torch_device)
    state_dict = torch.load(path+'/model_data.pt', Net.torch_device)
    main_model.load_state_dict(state_dict)
    main_model.eval()
    


def load_module():
    """Загрузить данный модуль."""
    global models_state
    global state_filepath
    
    try:
        with open(state_filepath) as inp:
            models_state = json.load(inp) 
        load_main_model()
    except:
        pass

if __name__ == '__main__':
    load_module()


def calc(input_dict):
    """
    Вычислить оценку.
    Аргументы:

    input_dict  --- dict[str]
    Выход:
    float - значение оценки
    или при ошибке
    {
        'missing_input' - список названий отсутствующих полей.
        'unknown_input' - список неизвестных названий полей.
    }
    """
    if not isinstance(input_dict, dict):
        raise ValueError("Ожидался ввод типа dict")
    missing_input = []
    unknown_input = []
    for field in main_model_fields:
        if not isinstance(field, QField):
            continue
        if not field.name in input_dict:
            missing_input.append(field.name)
    for inp_field in input_dict:
        if inp_field not in Field.df:
            unknown_input.append(inp_field) 
    if len(missing_input)>0 or len(unknown_input)>0:
        return {
            'missing_input': missing_input,
            'unknown_input': unknown_input
        }
    load_main_model()
    # Initial parsing
    for field in main_model_fields:
        if isinstance(field, QFieldChoice):
            if field.separate:
                for i in field.answers:
                    input_dict[field.name+":"+i] = 1.0 if input_dict[field.name] == i else 0
            else:
                input_dict[field.name] = field.answers[input_dict[field.name]]
        elif isinstance(field, QFieldNumeric):
            input_dict[field.name] = float(input_dict[field.name])
        elif isinstance(field, FieldCalc):
            continue
        else:
            raise NotImplementedError('Unknown field class')
    # Calc fields
    for field in main_model_fields:
        if isinstance(field, FieldCalc):
            exec(field.code, {'df':input_dict})
    # Z-Score Normalization
    for field in main_model_fields:
        if isinstance(field, (QFieldNumeric, FieldCalc)):
            input_dict[field.name] = (input_dict[field.name] - field.mean)/field.std

    input_list = []
    for field in main_model_fields:
        if field.ignore:
            continue
        if isinstance(field, QFieldChoice) and field.separate:
            for ans in field.answers:
                input_list.append(input_dict[field.name+':'+ans])
        else:
            input_list.append(input_dict[field.name])
    input_tensor = torch.FloatTensor([input_list])
    output_tensor = main_model(input_tensor).tolist()
    return output_tensor[0][0]*main_model_out['std']+main_model_out['mean']

 
def save_answer(input_dict, score):
    path = 'logs/'+models_state['main_model']+'.csv'
    if not os.path.isfile(path):
        with open(path, 'w') as outp:
            writer = csv.writer(outp, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(list(input_dict.keys())+['Score','DateTime'])
            writer.writerow(list(input_dict.values())+[score, datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S") ])
    else:
        with open(path, 'a') as outp:
            writer = csv.writer(outp, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(list(input_dict.values())+[score, datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S") ])
    