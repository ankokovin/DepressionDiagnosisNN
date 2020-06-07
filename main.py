#main.py
import secrets
from fastapi import Depends, FastAPI, Form, Response, status, File, UploadFile, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, HTMLResponse
import nn_handler.calc as handler
import uuid
import os
from jinja2 import Template
from pydantic import BaseModel
from typing import List, Union

class query_item(BaseModel):
    name: str
    value: Union[str, float]

class query(BaseModel):
    items: List[query_item]


app = FastAPI(
    title="Система диагностики депрессии",
    description="""Данная система разработана в рамках ВКР "Разработка информационной системы для нейросетевого исследования феномена депрессии" 
    \nстудента ВШЭ-Пермь группы ПИ-16-2 Коковина Алексея Николаевича
    """
)

templates = {}

for filename in os.listdir("templates"):
    if filename.endswith('.html'):
        item = ""
        with open('templates/'+filename, 'r',encoding='UTF-8') as inp:
            item = inp.read()
        templates[filename] = item

app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "12345")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/test")
def test():
    """Страница прохождения диагностики
    """
    result = Template(templates['test.html']).render(fields=handler.main_model_fields_data)
    return HTMLResponse(result)

@app.get("/")
def read_root():
    """Начальная страница
    """
    return RedirectResponse("/static/index.html")

@app.post("/diagnose/")
def diagnose(json_q: query):
    """Запрос для прохождения диагностики
    """
    input_dict = {}
    for item in json_q.items:
        input_dict[item.name] = item.value
    res = handler.calc(input_dict)
    if isinstance(res, float):
        handler.save_answer(input_dict, res)
        return res
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res,
        )

@app.get("/result/{score}")
def result(score:float):
    """Страница результата диагностики
    """
    result = Template(templates['result.html']).render(score = str(score))
    return HTMLResponse(result)

@app.get("/admin/")
def admin(username: str = Depends(get_current_username)):
    """Страница управления моделями
    """
    with open("admin.html","r",encoding='UTF-8') as inp:
        result = ''.join(inp.readlines())
    return HTMLResponse(result)

@app.post("/upload_model/")
def add_model(model_info: UploadFile = File(...), model_data: UploadFile = File(...), username: str = Depends(get_current_username)):
    """Запрос на загрузку модели на сервер
    """
    model_uuid = str(uuid.uuid4())
    path = os.getcwd()+'/models/'+str(model_uuid)
    os.mkdir(path)
    with open(path+'/model_data.pt', 'wb') as out:
        out.write(model_data.file.read())
    with open(path+'/model_info.json','wb') as out:
        out.write(model_info.file.read())
    result = handler.load_model(model_uuid)
    return {
        "Success": result,
        "UUID": model_uuid
    }

@app.get('/models')
def models_list(username: str = Depends(get_current_username)):
    """Запрос списка моделей
    """
    result = []
    if 'models' in handler.models_state:
        for key, val in handler.models_state['models'].items():
            item = {
                "name": val['name'] if 'name' in val else key,
                "uuid": key,
                "main": 'main_model' in handler.models_state and key == handler.models_state['main_model']
            }
            result.append(item)
    return result

@app.post('/set_main/{model_uuid}')
def change_main_model(model_uuid, username: str = Depends(get_current_username)):
    """Запрос на изменение главной модели системы
    """
    try:
        handler.set_main(model_uuid)
    except ValueError as er:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(er),
            headers={"WWW-Authenticate": "Basic"},
        )
    
@app.delete('/delete_model/{model_uuid}')
def delete_model_call(model_uuid,response:Response,  username: str = Depends(get_current_username)):
    """Запрос на удаление модели
    """
    if model_uuid in handler.models_state['models']:
        handler.models_state['models'].pop(model_uuid, None)
        handler.save_state()
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    
