#nn_handler/field.py
from enum import Enum
from ast import parse as ast_parse
import re
"""
Модуль представления полей.
"""

class FieldInputError(Exception):
    """Базовый класс ошибок модуля"""
    pass

class FieldNameExists(FieldInputError):
    """Ошибка: поле с именем уже существует"""
    def __init__(self, name):
        self.name = name
        msg = "Поле с именем '"+name+"' уже существует."
        super().__init__(FieldNameExists, self,msg)

class CalcCodeParseError(FieldInputError):
    """Ошибка парсинга кода вычисляемого поля"""
    pass



class FieldType(Enum):
    """
    Перечисление типов полей.
    Используется для упрощения соответствия строк типов полей и классов полей. 
    """
    choice  = 1
    numeric = 2
    calc    = 3
    def __int__(self):
        """
        Перевод значения перечисления в числовой вид.
        Используется для передачи в шаблон фронтенда.
        """
        return self.value


class Field():
    """
    Абстрактный класс поля.
    Ожидается, что он не будет использоваться сам по себе, но будет наследоваться.
    """


    df = {}
    @staticmethod
    def clear_field_list():
        Field.df.clear()

    @staticmethod
    def add_name(name):
        if name in Field.df:
            raise FieldNameExists(name)
        Field.df[name]=1.0
    
    @staticmethod
    def register(name, from_child):
        if not from_child:
            Field.add_name(name)

    def __init__(self, name, field_type, ignore, from_child=False):
        """
        Инициализация поля.

        Аргументы:
        name        --- имя поля, str
        field_type  --- тип поля класса FieldType
        ignore      --- игнорирование поля как входа в нейронную сеть
        """
        if not isinstance(name, str):
            raise ValueError('field name must be string')
        self.name = name
        if not isinstance(field_type, FieldType):
            raise ValueError('field type must be from enum')
        self.field_type = field_type
        if not isinstance(ignore, bool):
            raise ValueError('ignore must be bool')
        self.ignore = ignore
        Field.register(name, from_child)

class QField(Field):
    """
    Класс поля с вопросом. Наследует Field.
    Используется в случае, если значение поля зависит от ввода пользователя.
    """
    def __init__(self, name, field_type, ignore, question, from_child=False):
        """
        Инициализация поля с вопросом.

        Аргументы:
        name        --- имя поля, str
        field_type  --- тип поля класса FieldType
        ignore      --- игнорирование поля как входа в нейронную сеть
        question    --- отображаемый вопрос, str
        """
        super().__init__(name, field_type, ignore, True)
        if not isinstance(question, str):
            raise ValueError('field question must be string')
        self.question = question
        Field.register(name, from_child)
        
        
class QFieldChoice(QField):
    """
    Класс поля с множественным выбором ответа. Наследует QField.
    """
    def __init__(self, name, ignore, question, separate, answers, from_child=False):
        """
        Инициализация поля с вопросом.

        Аргументы:
        name        --- имя поля, str
        ignore      --- игнорирование поля как входа в нейронную сеть
        question    --- отображаемый вопрос, str
        separate    --- отображать ли через "one hot encoding", bool
        answers     --- варианты ответа: list[str] если separate == True иначе dict[str, number]
        """
        super().__init__(name,  FieldType.choice, ignore, question,True)
        if not isinstance(separate, bool):
            raise ValueError('separate must be bool')
        self.separate = separate
        if not separate:
            if not isinstance(answers,  dict):
                raise ValueError('choice field answers on non-separate field must be dict')
            for key, val in answers.items():
                if not isinstance(key, str):
                    raise ValueError('all answer keys must be str')
                if not isinstance(val, (int, float)):
                    raise ValueError('all answer values must be int of float')
        elif separate:
            if not isinstance(answers, list):
                raise ValueError('choice filed answers on separate field must be list')
            for item in answers:
                if not isinstance(item, str):
                    raise ValueError('all answer items must be str')
        self.answers = answers
        Field.register(name, from_child)

class QFieldNumeric(QField):
    """
    Класс поля с числовым ответом. Наследует QField.
    """
    def __init__(self, name, ignore, question, mean, std, from_child=False):
        """
        Инициализация поля с числовым ответом.

        Аргументы:
        name        --- имя поля, str
        ignore      --- игнорирование поля как входа в нейронную сеть
        question    --- отображаемый вопрос, str
        mean        --- среднее значение для Z-scoring
        std         --- стандартное квадратичное отклонение для Z-scoring, неотрицательное
        """
        super().__init__(name, FieldType.numeric, ignore, question, True)
        if not isinstance(mean, float):
            raise ValueError('numeric field mean must be float')
        if not isinstance(std, float):
            raise ValueError('numeric field std must be float')
        if std<0:
            raise ValueError('deviation cannot be negative')
        self.mean = mean
        self.std = std
        Field.register(name, from_child)

class FieldCalc(Field):
    """
    Класс вычислимого поля. Наследует Field.
    """
    def __init__(self, name, ignore, code, mean, std, from_child=False):
        """
        Инициализация вычислимого поля.

        Аргументы:
        name        --- имя поля, str
        ignore      --- игнорирование поля как входа в нейронную сеть
        code        --- исполняемый код для расчёта значения поля
        mean        --- среднее значение для Z-scoring
        std         --- стандартное квадратичное отклонение для Z-scoring, неотрицательное
        
        Пример значения code:
        df['name'] = df['name1'] + df['name2']
        """
        super().__init__(name, FieldType.calc, ignore, True)
        if not isinstance(code, str):
            raise ValueError('code in calc field is expected to be str')
        if not isinstance(mean, float):
            raise ValueError('numeric field mean must be float')
        if not isinstance(std, float):
            raise ValueError('numeric field std must be float')
        if std<0:
            raise ValueError('deviation cannot be negative')
        try:
            ast_parse(code)
        except SyntaxError as e:
            raise CalcCodeParseError(e.msg)
        if not "df[\'"+name+"\']" in code and not 'df[\"'+name+'\"]' in code:
            raise CalcCodeParseError('В коде отсутствует ссылка на df[\"'+name+'\"]')  
        regex = r"(?<=df\[)[ ]*('|\")[a-zA-Z0-9_ ]+('|\")[ ]*(?=])"
        matches = re.finditer(regex, code, re.MULTILINE)
        for match in matches:
            fragment = code[match.start():match.end()]
            tname = fragment.strip()[1:-1]
            if tname != name and tname not in Field.df:
                raise CalcCodeParseError('В коде используется ссылка на неизвестное поле с именем '+tname)
        self.mean = mean
        self.std = std
        self.code = code
        Field.register(name, from_child)

