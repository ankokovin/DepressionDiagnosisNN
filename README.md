# Платформа для прохождения тестов

## Описание процесса прохождения диагностики

![](https://github.com/ankokovin/DepressionDiagnosisNN/blob/master/docimgs/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0.PNG)

***Главная страница***

При нажатии кнопки "Начать" откроется анкета с вопросами.

![](https://github.com/ankokovin/DepressionDiagnosisNN/blob/master/docimgs/%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.PNG)

***Страница тестирования***

После ввода ответов на все вопросы следует нажать "Отправить". После нажатия откроется страница с результатами диагностики.

![](https://github.com/ankokovin/DepressionDiagnosisNN/blob/master/docimgs/%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20%D1%80%D0%B5%D0%B7%D1%83%D0%BB%D1%8C%D1%82%D0%B0%D1%82%D0%B0.PNG)

***Страница результата***

## Руководство администратора

### Запуск системы

Для локального запуска системы запустите файл !run.bat через Проводник или через консоль:

```shell 
.\!run.bat
```
***
Для запуска системы через Docker:
1) Выполните сборку image системы, если она ещё не была совершена:
```shell
docker build --pull --rm -f "Dockerfile" -t finals:latest "." 
```
2) Запустите файл !rundocker.bat через Проводник или через консоль
```shell
.\!rundocker.bat
```
***
Для запуска тестов системы запустите файл !rundoctest.bat через Проводник или через консоль:

```shell 
.\!rundoctest.bat
```



### Управление моделями

![](https://github.com/ankokovin/DepressionDiagnosisNN/blob/master/docimgs/%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F%20%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0.PNG)

***Главная страница***

Для открытия меню администрирования нажмите ссылку Admin. После ввода логина и пароля откроется страница администрирования.

![](https://github.com/ankokovin/DepressionDiagnosisNN/blob/master/docimgs/%D0%A1%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0%20%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F.PNG)

***Страница администрирования***

Сверху страницы расположен ввод новой модели в систему. Для ввода модели выполните выбор файла конфигурации модели и файла нейронной сети и нажмите Отправить.

Снизу страницы расположен список моделей. Для каждой модели указывается её название и уникальный идентификатор.

Кнопка основной модели страницы выделена синим цветом. Для изменения основной модели нажмите на блок модели.

Напротив кнопок моделей находятся кнопки для удаления моделей.

## Описание кода

### Модуль nn_handler

#### nn_handler.field
Модуль представления полей.

##### Класс FieldType
Перечисление типов полей.
Используется для упрощения соответствия строк типов полей и классов полей. 

Значения:
- choice  = 1
- numeric = 2
- calc    = 3     

Имеет преобразование к числу, используется для передачи в шаблон фронтенда

[Тесты](#test-fieldtype)

##### Класс Field

Абстрактный класс поля.
Ожидается, что он не будет использоваться сам по себе, нобудет наследоваться.

Поля:
- name        --- имя поля, str
- field_type  --- тип поля класса [FieldType](#класс-fieldtype)
- ignore      --- игнорирование поля как входа в нейронную сеть

[Тесты](#test-field)

##### Класс QField

Класс поля с вопросом.  Наследует Field.
Используется в случае, если значение поля зависит от ввода пользователя.

Поля:
- name          --- имя поля, str
- field_type    --- тип поля класса [FieldType](#класс-fieldtype)
- ignore        --- игнорирование поля как входа в нейронную сеть
- question      --- отображаемый вопрос, str

[Тесты](#test-qfield)

##### Класс QFieldChoice 
Класс поля с множественным выбором ответа. Наследует [QField](#класс-qfield).

Поля:
- name        --- имя поля, str
- field_type  --- тип поля класса FieldType- 
- ignore      --- игнорирование поля как входа в нейронну- сеть
- question    --- отображаемый вопрос, str- 
- separate    --- отображать ли через "one hot encoding"- bool
- answers     --- варианты ответа: list[str] если separate == True иначе dict[str, number]
        
[Тесты](#test-qfieldchoice)

##### Класс QFieldNumeric
Класс поля с числовым ответом. Наследует [QField](#класс-qfield).

Поля:
- name        --- имя поля, str
- ignore      --- игнорирование поля как входа в нейронную сеть
- question    --- отображаемый вопрос, str
- mean        --- среднее значение для Z-scoring
- std         --- стандартное квадратичное отклонение для Z-scoring

[Тесты](#test-qfieldnumeric)

##### Класс FieldCalc
Класс вычислимого поля. Наследует [Field](#класс-field).

Поля:
- name        --- имя поля, str
- ignore      --- игнорирование поля как входа в нейронную сеть
- code        --- исполняемый код для расчёта значения поля
- mean        --- среднее значение для Z-scoring
- std         --- стандартное квадратичное отклонение для Z-scoring, неотрицательное

Требования к исполняемому коду:
1. Должно иметь строковое представление.
2. Должно обращаться к объекту df. Он имеет тип dict. Ключами являются имена полей.
3. Должно быть упоминание df[\<name\>]. Желательно с присваиванием. 
4. Нельзя обращаться к полям, объявления которых лежат ниже в описании конфигурации системы.

Пример - вычисление коэффициента массы тела по росту и весу с последующим игнорированием веса и роста:
```python
>>> from nn_handler.field import QFieldNumeric, FieldCalc
>>> f1 = QFieldNumeric('вес', True, 'Ваш вес', 0.0, 1.0)
>>> f2 = QFieldNumeric('рост', True, 'Ваш рост',0.0, 1.0)
>>> f3 = FieldCalc('BMI',False,"df['BMI']=df['вес']/df['рост']**2", 0.0 , 1.0)

```

[Тесты](#test-fieldcalc)

##### Класс FieldInputError
Базовый класс ошибки ввода в систему экземпляра [Field](#класс-field).

##### Класс FieldNameExists
Класс ошибки: поле с именем уже существует. Проверка на имя происходит при инициализации объекта на уровне [Field](#класс-field).

[Тесты](#test-fieldnameexists)

##### Класс CalcCodeParseError
Класс ошибки: код вычисляемого поля некорректен. Варианты содержания сообщения:
1. Syntax error - общая синтаксическая ошибка.
2. В коде отсутствует ссылка на df["<имя данного поля>"].
3. В коде сущесвует ссылка на df["<имя невведённого поля>"].

#### Net

Данный модуль содержит реализацию нейронной сети.

##### Класс Net

Реализация нейронной сети.

###### __init__

Инициализация нейронной сети.

Аргументы:

- hidden_cnt - количество нейронов на скрытом слое
- input_cnt - количество входных нейронов
- output_cnt - количество выходных нейронов
- act_function='Sigmoid' - функция активации нейронов 

###### get_torch_act_function

Функция преобразования строки названия функции активации к объекту функции активации из PyTorch.

###### forward

Прямое распространение сигнала по нейронной сети.

#### Calc

Модуль управления моделями

##### set_main
Установка модели как главной.

Аргументы:

model_uuid  --- str, id модели

##### load_model
Загрузка модели из файловой системы.

Аргументы:

model_uuid  --- str, id модели

##### save_state

Сохранить текущее состояние моделей

##### delete_model

Удалить модель из файловой системы.

Аргументы:

model_uuid  --- str, id модели

##### load_main_model

Загрузить основную модель для вычислений

##### load_module

Загрузить данный модуль

##### calc

Вычислить оценку.

Аргументы:    input_dict  --- dict[str]
    
Выход:
- float - значение оценки
- или при ошибке 
    ```
    {
        'missing_input' - список названий отсутствующих полей.
        'unknown_input' - список неизвестных названий полей.
    }
    ```

##### save_answer

Сохранить полученный результат. Создаёт или продолжает файл */logs/\<main_model_uuid\>.csv*.

Аргументы:
- input_dict - словарь полученных входных данных
- score - полученная оценка

### Main

Описание доступно по пути /doc.

## Юнит-тесты

Запуск тестов - !rundoctest.bat.

Тесты реализованы при помощи doctest.

Содержание тестов - ниже.



```python
# Очистка перед выполнением тестов
>>> from nn_handler.field import Field; Field.clear_field_list(); import os
>>> try: os.rename(os.getcwd()+'/models', 'models-saved'); os.mkdir(os.getcwd()+'/models')
... except: pass

# 
```
### Модуль nn_handler.field
<a id="test-fieldtype"></a>

#### [FieldType](#класс-fieldtype)
##### import
```python
>>> from nn_handler.field import FieldType

```

##### int
```python
>>> int(FieldType.choice)
1
>>> int(FieldType.numeric)
2
>>> int(FieldType.calc)
3

```
<a id="test-field"></a>

#### [Field](#класс-field)
##### import
```python
>>> from nn_handler.field import Field

```
##### __init__
###### Количество аргументов - 3
```python
>>> Field()
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'name', 'field_type', and 'ignore'

>>> Field(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'field_type' and 'ignore'

>>> Field(1,2)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'ignore'

```
###### Типы аргументов
- name - str
```python
>>> Field(1, 1, 1)
Traceback (most recent call last):
...
ValueError: field name must be string

```
- field_type - [FieldType](#classFieldType)
```python
>>> Field('test',1,1)
Traceback (most recent call last):
...
ValueError: field type must be from enum

```
- ignore - bool
```python
>>> Field('test',FieldType.choice,1)
Traceback (most recent call last):
...
ValueError: ignore must be bool

```
###### Доступность полей
```python     
>>> f = Field('test',FieldType.choice,True)
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == True
>>> assert 'test' in Field.df
>>> Field.clear_field_list()
        
>>> f = Field('test',FieldType.numeric,True)
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.numeric
>>> assert f.ignore == True
>>> assert 'test' in Field.df
>>> Field.clear_field_list()
        
>>> f = Field('test',FieldType.calc,False)
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.calc
>>> assert f.ignore == False
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

```

<a id='test-fieldnameexists'></a>

#### [FieldNameExists](#класс-fieldnameexists) 
```python     
>>> Field('test', FieldType.calc, False); assert len(Field.df) == 1; Field('test', FieldType.calc, False)
Traceback (most recent call last):
...
nn_handler.field.FieldNameExists: (<class 'nn_handler.field.FieldNameExists'>, FieldNameExists(...), "Поле с именем 'test' уже существует.")
>>> assert len(Field.df) == 1; Field.clear_field_list()

```
<a id="test-qfield"></a>

#### [QField](#класс-qfield)
##### import
```python
>>> from nn_handler.field import QField

```
##### __init__
###### Количество аргументов - 4
```python
>>> QField()
Traceback (most recent call last):
...
TypeError: __init__() missing 4 required positional arguments: 'name', 'field_type', 'ignore', and 'question'

>>> QField(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'field_type', 'ignore', and 'question'

>>> QField(1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'ignore' and 'question'

>>> QField(1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'question'

```
###### Типы аргументов:
- name - str
```python
>>> QField(1,1,1,1)
Traceback (most recent call last):
...
ValueError: field name must be string

```
- field_type - FieldType
```python
>>> QField('test',1,1,1)
Traceback (most recent call last):
...
ValueError: field type must be from enum

```
- ignore - bool
```python
>>> QField('test',FieldType.choice,1,1)
Traceback (most recent call last):
...
ValueError: ignore must be bool

```

- question - str
```python
>>> QField('test',FieldType.choice,False,1)
Traceback (most recent call last):
...
ValueError: field question must be string

```
 
###### Доступность полей
```python
>>> f = QField('test',FieldType.choice,True,'test_question')
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == True
>>> assert f.question == 'test_question'
>>> assert 'test' in Field.df
>>> Field.clear_field_list()
        
>>> f = QField('test',FieldType.numeric,True,'test_question')
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.numeric
>>> assert f.ignore == True
>>> assert f.question == 'test_question'
>>> assert 'test' in Field.df
>>> Field.clear_field_list()
        
>>> f = QField('test',FieldType.calc,False,'test_question')
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.calc
>>> assert f.ignore == False
>>> assert f.question == 'test_question'
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

```

<a id="test-qfieldchoice"></a>

#### [QFieldChoice](#класс-qfieldchoice)
##### import
```python
>>> from nn_handler.field import QFieldChoice

```
##### __init__ 
###### Количество аргументов: 5
```python
>>> QFieldChoice()
Traceback (most recent call last):
...
TypeError: __init__() missing 5 required positional arguments: 'name', 'ignore', 'question', 'separate', and 'answers'

>>> QFieldChoice(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 4 required positional arguments: 'ignore', 'question', 'separate', and 'answers'

>>> QFieldChoice(1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'question', 'separate', and 'answers'

>>> QFieldChoice(1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'separate' and 'answers'

>>> QFieldChoice(1,1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'answers'

```
###### Типы аргументов: 
- name - str
```python
>>> QFieldChoice(1,1,1,1,1)
Traceback (most recent call last):
...
ValueError: field name must be string

```
- ignore - bool
```python
>>> QFieldChoice('test',1,1,1,1)
Traceback (most recent call last):
...
ValueError: ignore must be bool

```
- question - str
```python
>>> QFieldChoice('test',False,1,1,1)
Traceback (most recent call last):
...
ValueError: field question must be string

```
- separate - bool
```python
>>> QFieldChoice('test',False,'test_qestion',1,1)
Traceback (most recent call last):
...
ValueError: separate must be bool

```
- answers - list[str] если separate == True или dict[str, number] если separate == False
```python
>>> QFieldChoice('test',False,'test_question',False,1)
Traceback (most recent call last):
...
ValueError: choice field answers on non-separate field must be dict

>>> QFieldChoice('test',False,'test_qauestion',False,['one','two'])
Traceback (most recent call last):
...
ValueError: choice field answers on non-separate field must be dict

>>> QFieldChoice('test',False,'test_question',False,{1:2,'test':2})
Traceback (most recent call last): 
...
ValueError: all answer keys must be str

>>> QFieldChoice('test',False,'test_question',False,{'test':1,'test2':'qq'})
Traceback (most recent call last):
...
ValueError: all answer values must be int of float

>>> QFieldChoice('test',False,'test_question',True,1)
Traceback (most recent call last):
...
ValueError: choice filed answers on separate field must be list

>>> QFieldChoice('test',False,'test_question',True,{'test':1})
Traceback (most recent call last):
...
ValueError: choice filed answers on separate field must be list

>>> QFieldChoice('test',False,'test_question',True,['hi',1])
Traceback (most recent call last):
...
ValueError: all answer items must be str

```
###### Доступность полей
```python
>>> f=QFieldChoice('test',False,'test_question',True,['hi','all'])
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == False
>>> assert f.question == 'test_question'
>>> assert f.separate == True
>>> assert len(f.answers) == 2
>>> assert f.answers[0] == 'hi'
>>> assert f.answers[1] == 'all'
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

>>> f=QFieldChoice('test',True,'test_question',True,['hi'])
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == True
>>> assert f.question == 'test_question'
>>> assert f.separate == True
>>> assert len(f.answers) == 1
>>> assert f.answers[0] == 'hi'
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

>>> f=QFieldChoice('test',False,'test_question',False,{'hi':1})
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == False
>>> assert f.question == 'test_question'
>>> assert f.separate == False
>>> assert len(f.answers) == 1
>>> assert f.answers['hi'] == 1
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

>>> f=QFieldChoice('test',True,'test_question',False,{'hi':1, 'all':0.5})
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.choice
>>> assert f.ignore == True
>>> assert f.question == 'test_question'
>>> assert f.separate == False
>>> assert len(f.answers) == 2
>>> assert f.answers['hi'] == 1
>>> assert f.answers['all'] == 0.5
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

```

<a id='test-qfieldnumeric'></a>

#### [QFieldNumeric](#класс-qfieldnumeric)
##### import
```python
>>> from nn_handler.field import QFieldNumeric

```
##### __init__
###### Количество аргументов: 5
```python
>>> QFieldNumeric()
Traceback (most recent call last):
...
TypeError: __init__() missing 5 required positional arguments: 'name', 'ignore', 'question', 'mean', and 'std'

>>> QFieldNumeric(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 4 required positional arguments: 'ignore', 'question', 'mean', and 'std'

>>> QFieldNumeric(1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'question', 'mean', and 'std'

>>> QFieldNumeric(1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'mean' and 'std'

>>> QFieldNumeric(1,1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'std'

```
###### Типы аргументов: 
- name - str
```python
>>> QFieldNumeric(1,1,1,1,1)
Traceback (most recent call last):
...
ValueError: field name must be string

```
- ignore - bool
```python
>>> QFieldNumeric('test',1,1,1,1)
Traceback (most recent call last):
...
ValueError: ignore must be bool

```
- question - str
```python
>>> QFieldNumeric('test',False,1,1,1)
Traceback (most recent call last):
...
ValueError: field question must be string

```
- mean - float
```python
>>> QFieldNumeric('test',False,'test_question',1,1)
Traceback (most recent call last):
...
ValueError: numeric field mean must be float

```
- std - float, non-negative
```python
>>> QFieldNumeric('test',False,'test_question',1.0,1)
Traceback (most recent call last):
...
ValueError: numeric field std must be float

>>> QFieldNumeric('test',False,'test_question',1.0,-1.0)
Traceback (most recent call last):
...
ValueError: deviation cannot be negative

```

###### Доступность полей
```python
>>> f=QFieldNumeric('test',False,'test_question',1.0,2.0)
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.numeric
>>> assert f.ignore == False
>>> assert f.question == 'test_question'
>>> assert f.mean == 1.0
>>> assert f.std == 2.0
>>> assert 'test' in Field.df
>>> Field.clear_field_list()


>>> f=QFieldNumeric('test',True,'test_question',1.0,2.0)
>>> assert f.name == 'test'
>>> assert f.field_type == FieldType.numeric
>>> assert f.ignore == True
>>> assert f.question == 'test_question'
>>> assert f.mean == 1.0
>>> assert f.std == 2.0
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

```

<a id='test-fieldcalc'></a>

#### [FieldCalc](#класс-fieldcalc)
##### import
```python
>>> from nn_handler.field import FieldCalc

```
##### __init__
###### Количество аргументов: 
```python
>>> FieldCalc()
Traceback (most recent call last):
...
TypeError: __init__() missing 5 required positional arguments: 'name', 'ignore', 'code', 'mean', and 'std'

>>> FieldCalc(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 4 required positional arguments: 'ignore', 'code', 'mean', and 'std'

>>> FieldCalc(1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'code', 'mean', and 'std'

>>> FieldCalc(1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'mean' and 'std'

>>> FieldCalc(1,1,1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'std'

```
###### Типы аргументов:

- name - str
```python
>>> FieldCalc(1,1,1,1,1)
Traceback (most recent call last):
...
ValueError: field name must be string

```
- ignore - bool
```python
>>> FieldCalc('test',1,1,1,1)
Traceback (most recent call last):
...
ValueError: ignore must be bool

```
- code - str
```python
>>> FieldCalc('test',False,1,1,1)
Traceback (most recent call last):
...
ValueError: code in calc field is expected to be str

```

- mean - float
```python
>>> FieldCalc('test',False,'df["test"]',1,1)
Traceback (most recent call last):
...
ValueError: numeric field mean must be float

```
- std - float, non-negative
```python
>>> FieldCalc('test',False,'df["test"]',1.0,1)
Traceback (most recent call last):
...
ValueError: numeric field std must be float

>>> FieldCalc('test',False,'df["test"]',1.0,-1.0)
Traceback (most recent call last):
...
ValueError: deviation cannot be negative

```
###### Доступность полей
```python
>>> f = FieldCalc('test',False,'df["test"]',1.0,2.0)
>>> assert f.name == 'test'
>>> assert f.ignore == False
>>> assert f.code == 'df["test"]'
>>> assert f.mean == 1.0
>>> assert f.std == 2.0
>>> assert 'test' in Field.df
>>> Field.clear_field_list()

```

<a id='test-calccodeparseerror'></a>

#### [CalcCodeParseError](#класс-calccodeparseerror)
1. Syntax error
```python
>>> FieldCalc('test',False,'def t',1.0,1.0)
Traceback (most recent call last):
...
nn_handler.field.CalcCodeParseError: invalid syntax

```
2. Отсутсвие в коде ссылки на поле
```python
>>> FieldCalc('test',False,'2+2',1.0,1.0)
Traceback (most recent call last):
...
nn_handler.field.CalcCodeParseError: В коде отсутствует ссылка на df["test"]

```
3. Наличие ссылки на ещё не добавленное поле
```python
>>> FieldCalc('test',False,'df["test"]=df["illegal_field"]',1.0,1.0)
Traceback (most recent call last):
...
nn_handler.field.CalcCodeParseError: В коде используется ссылка на неизвестное поле с именем illegal_field

```

### nn_handler.net
#### import
```python
>>> import os; os.environ['VERBOUSE'] = 'False'; from nn_handler.net import Net

```
#### get_torch_act_function
```python
>>> Net.get_torch_act_function()
Traceback (most recent call last):
...
TypeError: get_torch_act_function() missing 1 required positional argument: 'name'

>>> Net.get_torch_act_function(1)
Traceback (most recent call last):
...
ValueError: Expected string for a name of activation function

>>> Net.get_torch_act_function('test')
Traceback (most recent call last):
...
ValueError: Activation function "test" is not defined

>>> Net.get_torch_act_function('test', 1)
Traceback (most recent call last):
...
TypeError: get_torch_act_function() takes 1 positional argument but 2 were given

>>> Net.get_torch_act_function('tanh')
Tanh()

>>> Net.get_torch_act_function('sigmoid')
Sigmoid()

```
#### __init__
##### Количество аргументов: 3
```python
>>> Net()
Traceback (most recent call last):
...
TypeError: __init__() missing 3 required positional arguments: 'hidden_cnt', 'input_count', and 'output_count'
>>> Net(1)
Traceback (most recent call last):
...
TypeError: __init__() missing 2 required positional arguments: 'input_count' and 'output_count'
>>> Net(1,1)
Traceback (most recent call last):
...
TypeError: __init__() missing 1 required positional argument: 'output_count'

```
##### Аргументы:
3 натуральных числа + (опционально) название функции активации
```python
>>> Net('hello, world',1,1)
Traceback (most recent call last):
...
ValueError: hidden_cnt must be a natrual number
>>> Net(1,'hello, world',1)
Traceback (most recent call last):
...
ValueError: input_count must be a natrual number

>>> Net(1,1,'hello, world' )
Traceback (most recent call last):
...
ValueError: output_count must be a natrual number
>>> Net(-1,1,1)
Traceback (most recent call last):
...
ValueError: hidden_cnt must be a natrual number

>>> Net(1,-1,1)
Traceback (most recent call last):
...
ValueError: input_count must be a natrual number

>>> Net(1,1,-1)
Traceback (most recent call last):
...
ValueError: output_count must be a natrual number
>>> Net(1,1,1,'test')
Traceback (most recent call last):
...
ValueError: Activation function "test" is not defined

```
### nn_handler.calc
#### import
```python
>>> from nn_handler import calc

```
#### load

Загрузка первой модели

```python
>>> calc.load_module()
>>> assert len(calc.models_state) == 0

# Скопируем модель test из папки models-test в models с случайным uuid и попробуем загрузить
>>> import shutil; test_path = os.getcwd()+'/models-test/test/';model_path = os.getcwd()+'/models/'; import uuid; test_uuid = str(uuid.uuid4()); os.mkdir(model_path+test_uuid); r1 = shutil.copyfile(test_path+'model_data.pt',model_path+test_uuid+'/model_data.pt'); r2 = shutil.copyfile(test_path+'model_info.json',model_path+test_uuid+'/model_info.json'); calc.load_model(test_uuid);
True
>>> assert len(calc.models_state['models']) == 1
>>> assert calc.models_state['models'][test_uuid]['name'] == 'test'
>>> assert calc.models_state['models'][test_uuid]['model_data'] == '7c06541fa48e77b5e2a49fd25041619e'
>>> assert calc.models_state['models'][test_uuid]['model_info'] == 'eca818e482b6aa06bf6d19b5c411a87e'

```

Попытка повторной загрузки
```python
# Загрузка той же модели
>>> test_uuid2 = str(uuid.uuid4()); assert test_uuid2 != test_uuid; os.mkdir(model_path+test_uuid2); r1 = shutil.copyfile(test_path+'model_data.pt',model_path+test_uuid2+'/model_data.pt'); r2 = shutil.copyfile(test_path+'model_info.json',model_path+test_uuid2+'/model_info.json'); calc.load_model(test_uuid2)
False

# Загрузка иной модели
>>> test_uuid2 = str(uuid.uuid4()); assert test_uuid2 != test_uuid; test_path = os.getcwd()+'/models-test/test2/'; os.mkdir(model_path+test_uuid2); r1 = shutil.copyfile(test_path+'model_data.pt',model_path+test_uuid2+'/model_data.pt'); r2 = shutil.copyfile(test_path+'model_info.json',model_path+test_uuid2+'/model_info.json'); calc.load_model(test_uuid2)
True

```

#### set_main
```python
>>> calc.set_main(1)
Traceback (most recent call last):
...
ValueError: На вход ожидалось str

>>> calc.set_main('Unknown')
Traceback (most recent call last):
...
ValueError: Модель с таким идентификатором не была загружена

>>> calc.set_main(test_uuid)

>>> calc.set_main(test_uuid)

>>> calc.set_main(test_uuid2)

>>> calc.set_main(test_uuid)

```

#### calc
```python

>>> calc.calc(1)
Traceback (most recent call last):
...
ValueError: Ожидался ввод типа dict
>>> calc.calc({})
{'missing_input': ['Пол', 'Возраст', 'Образование', 'Доход', 'Семейное положение', 'Рост (см)', 'Вес (кг)', 'Детство', 'Потеря родителей', 'Родственники', 'Творчество', 'Умственный труд', 'Близкие', 'Заболевание'], 'unknown_input': []}
>>> calc.calc({'Unknown':'input'})
{'missing_input': ['Пол', 'Возраст', 'Образование', 'Доход', 'Семейное положение', 'Рост (см)', 'Вес (кг)', 'Детство', 'Потеря родителей', 'Родственники', 'Творчество', 'Умственный труд', 'Близкие', 'Заболевание'], 'unknown_input': ['Unknown']}
>>> calc.calc({'Unknown':'input','Потеря родителей':'Нет', 'Семейное положение':'Не женат/замужем', 'Вес (кг)':105, 'Доход':'Менее 20 тыс.', 'Образование':'Среднее', 'Родственники':'Нет', 'Умственный труд':'Нет', 'Близкие':'Нет', 'Рост (см)':180, 'Возраст':21, 'Пол':'Мужской', 'Детство':'Нет', 'Заболевание':'Нет', 'Творчество':'Нет'})
{'missing_input': [], 'unknown_input': ['Unknown']}
>>> calc.calc({'Потеря родителей':'Нет', 'Семейное положение':'Не женат/замужем', 'Вес (кг)':105, 'Доход':'Менее 20 тыс.', 'Образование':'Среднее', 'Родственники':'Нет', 'Умственный труд':'Нет', 'Близкие':'Нет', 'Рост (см)':180, 'Возраст':21, 'Пол':'Мужской', 'Детство':'Нет', 'Заболевание':'Нет', 'Творчество':'Нет'})
1.0

```

#### load(продолжение)

Загрузка системы по сохранённому состоянию

```python
>>> import json
>>> with open(model_path+'state.json', 'w') as outfile: 
...     json.dump({"models": {test_uuid: {"name":"test3","model_data": "7c06541fa48e77b5e2a49fd25041619e", "model_info": "eca818e482b6aa06bf6d19b5c411a87e"}}, "main_model":test_uuid},outfile)
>>> calc.load_module()
>>> assert len(calc.models_state['models']) == 1
>>> assert calc.models_state['models'][test_uuid]['name'] == 'test3'
>>> assert calc.models_state['models'][test_uuid]['model_data'] == '7c06541fa48e77b5e2a49fd25041619e'
>>> assert calc.models_state['models'][test_uuid]['model_info'] == 'eca818e482b6aa06bf6d19b5c411a87e'

```
TODO: загрузка моделей с некорретными описаниями полей


### main
```python
>>> from fastapi.testclient import TestClient
>>> import main
>>> client = TestClient(main.app)

```
Главная страница
```python
>>> client.get('/').status_code
200

```
Страница тестирования
```python
>>> client.get('/test').status_code
200

```
Страница с результатом
```python
>>> resp = client.get('/result/1.234'); assert resp.status_code == 200; '1.234' in str(resp.content)
True

```
Список моделей
```python
>>> resp = client.get('/models'); resp.status_code; resp.json()['detail'] 
401
'Not authenticated'

>>> import base64; auth_header = {"WWW-Authenticate": "Basic", "Authorization":"Basic "+ str(base64.b64encode(("admin"+":"+"12345").encode("utf-8")), "utf-8")}; auth_fake_header = {"WWW-Authenticate": "Basic", "Authorization":"Basic "+ str(base64.b64encode(("unknownuser"+":"+"123441245").encode("utf-8")))}
>>> resp = client.get('/models',headers=auth_fake_header); resp.status_code; resp.json()['detail']
401
'Invalid authentication credentials'

>>> resp = client.get('/models',headers=auth_header); resp.status_code;  resp.json() == [{'name': 'test3', 'uuid': test_uuid, 'main': True}]
200
True


```
Прохождение диагностики
```python
>>> resp = client.post('/diagnose/', json={}); resp.status_code; resp.json()
422
{'detail': [{'loc': ['body', 'json_q', 'items'], 'msg': 'field required', 'type': 'value_error.missing'}]}

>>> resp = client.post('/diagnose/', json={'json_q':{}}); resp.status_code; resp.json() 
422
{'detail': [{'loc': ['body', 'json_q', 'items'], 'msg': 'field required', 'type': 'value_error.missing'}]}

>>> resp = client.post('/diagnose/', json={'items':[]});  resp.status_code; resp.json()
400
{'detail': {'missing_input': ['Пол', 'Возраст', 'Образование', 'Доход', 'Семейное положение', 'Рост (см)', 'Вес (кг)', 'Детство', 'Потеря родителей', 'Родственники', 'Творчество', 'Умственный труд', 'Близкие', 'Заболевание'], 'unknown_input': []}}

>>> resp = client.post('/diagnose/', json={'items':[{'name':'Unknown','value':'input'}]});  resp.status_code; resp.json()
400
{'detail': {'missing_input': ['Пол', 'Возраст', 'Образование', 'Доход', 'Семейное положение', 'Рост (см)', 'Вес (кг)', 'Детство', 'Потеря родителей', 'Родственники', 'Творчество', 'Умственный труд', 'Близкие', 'Заболевание'], 'unknown_input': ['Unknown']}}

>>> resp = client.post('/diagnose/', json={'items':[{'name':'Потеря родителей','value':'Нет'},{ 'name':'Семейное положение','value':'Не женат/замужем'},{ 'name':'Вес (кг)','value':105},{ 'name':'Доход','value':'Менее 20 тыс.'},{ 'name':'Образование','value':'Среднее'},{ 'name':'Родственники','value':'Нет'},{ 'name':'Умственный труд','value':'Нет'},{ 'name':'Близкие','value':'Нет'},{ 'name':'Рост (см)','value':180},{ 'name':'Возраст','value':21},{ 'name':'Пол','value':'Мужской'},{ 'name':'Детство','value':'Нет'},{ 'name':'Заболевание','value':'Нет'},{ 'name':'Творчество','value':'Нет'}]}); resp.status_code; resp.json()
200
1.0

>>> resp = client.post('/diagnose/', json={'items':[{'name':'Потеря родителей','value':'Нет'},{ 'name':'Семейное положение','value':'Не женат/замужем'},{ 'name':'Вес (кг)','value':105},{ 'name':'Доход','value':'Менее 20 тыс.'},{ 'name':'Образование','value':'Среднее'},{ 'name':'Родственники','value':'Нет'},{ 'name':'Умственный труд','value':'Нет'},{ 'name':'Близкие','value':'Нет'},{ 'name':'Рост (см)','value':180},{ 'name':'Возраст','value':21},{ 'name':'Пол','value':'Мужской'},{ 'name':'Детство','value':'Нет'},{ 'name':'Заболевание','value':'Нет'},{ 'name':'Творчество','value':'Нет'}]}); resp.status_code; resp.json()
200
1.0

```
Загрузка моделей
```python
>>> resp = client.post('/upload_model/',{}); resp.status_code; resp.json()['detail']
401
'Not authenticated'

>>> resp = client.post('/upload_model/',{}, headers=auth_fake_header); resp.status_code; resp.json()['detail']
401
'Invalid authentication credentials'

>>> resp = client.post('/upload_model/',{},headers=auth_header); resp.status_code; resp.json()['detail']
422
[{'loc': ['body', 'model_info'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'model_data'], 'msg': 'field required', 'type': 'value_error.missing'}]

>>> m_info_f = open(test_path+"model_info.json", 'r'); m_data_f = open(test_path+"model_data.pt", 'rb'); resp = client.post('/upload_model/', files={"model_info": ("model_info.json", m_info_f, ".json"),"model_data":("model_data.pt",m_data_f, ".pt")}, headers=auth_header); m_info_f.close(); m_data_f.close(); resp.status_code; resp.json()['Success']; r_uuid = uuid.UUID(resp.json()['UUID']); r_uuid = resp.json()['UUID']; resp = client.get('/models',headers=auth_header); resp.status_code; resp =  resp.json();  len(resp) == 2; resp[0]['name'] == 'test3'; resp[0]['uuid'] == test_uuid; resp[0]['main'] == True; resp[1]['name'] == r_uuid; resp[1]['uuid'] == r_uuid; resp[1]['main'] == False
200
True
200
True
True
True
True
True
True
True

>>> m_info_f = open(test_path+"model_info.json", 'r'); m_data_f = open(test_path+"model_data.pt", 'rb'); resp = client.post('/upload_model/', files={"model_info": ("model_info.json", m_info_f, ".json"),"model_data":("model_data.pt",m_data_f, ".pt")}, headers=auth_header); m_info_f.close(); m_data_f.close(); resp.status_code; resp.json()['Success']
200
False
>>> 
```
Смена главной модели
```python
>>> client.post('/set_main').status_code
404

>>> client.post('/set_main/').status_code
404

>>> client.post('/set_main/123').status_code
401

>>> client.post('/set_main/123',headers=auth_header).status_code
404

>>> client.post('/set_main/'+r_uuid,headers=auth_header).status_code; resp = client.get('/models',headers=auth_header); resp.status_code; resp =  resp.json();  len(resp) == 2; resp[0]['name'] == 'test3'; resp[0]['uuid'] == test_uuid; resp[0]['main'] == False; resp[1]['name'] == r_uuid; resp[1]['uuid'] == r_uuid; resp[1]['main'] == True
200
200
True
True
True
True
True
True
True

>>> client.post('/set_main/'+test_uuid,headers=auth_header).status_code; resp = client.get('/models',headers=auth_header); resp.status_code; resp =  resp.json();  len(resp) == 2; resp[0]['name'] == 'test3'; resp[0]['uuid'] == test_uuid; resp[0]['main'] == True; resp[1]['name'] == r_uuid; resp[1]['uuid'] == r_uuid; resp[1]['main'] == False
200
200
True
True
True
True
True
True
True

```

Удаление модели
```python
>>> client.delete('/delete_model').status_code
404

>>> client.delete('/delete_model/123').status_code
401

>>> client.delete('/delete_model/123', headers=auth_header).status_code
404

>>> client.delete('/delete_model/'+r_uuid, headers=auth_header).status_code; resp = client.get('/models',headers=auth_header); resp.status_code; resp =  resp.json();  len(resp) == 1; resp[0]['name'] == 'test3'; resp[0]['uuid'] == test_uuid; resp[0]['main'] == True
200
200
True
True
True
True


```


### Очистка после выполнения тестов
```python
>>> import os; import shutil; shutil.rmtree(os.getcwd()+'/models', ignore_errors=True)
>>> try:os.rename(os.getcwd()+'/models-saved', 'models') 
... except: pass

```
