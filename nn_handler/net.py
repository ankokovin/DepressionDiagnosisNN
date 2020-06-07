#nn_handler/net.py
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
"""
Данный модуль содержит реализацию нейронной сети.
"""


verbouse = os.getenv('VERBOUSE','True') == 'True' 

class Net(nn.Module):
    """
    Реализация нейронной сети
    """
    torch_device = None
    if torch.cuda.is_available():
        torch_device = torch.device("cuda:0")  
        if verbouse:
            print("Running on the GPU")
    else:
        torch_device = torch.device("cpu")
        if verbouse:
            print("Running on the CPU")

    @staticmethod
    def get_torch_act_function(name):
        """Функция преобразования строки названия функции активации к объекту функции активации из PyTorch.
        """
        if not isinstance(name, str):
            raise ValueError('Expected string for a name of activation function')
        elif name == 'tanh':
            return nn.Tanh()
        elif name == 'sigmoid':
            return nn.Sigmoid()
        else:
            raise ValueError('Activation function "'+name+'" is not defined')

    def __init__(self, hidden_cnt,input_count,output_count,act_function='sigmoid'):
        """
        Инициализация нейронной сети.
        Не следует менять для синхронизации с генерацией.

        
        Аргументы:

        - hidden_cnt - количество нейронов на скрытом слое
        - input_cnt - количество входных нейронов
        - output_cnt - количество выходных нейронов
        - act_function='Sigmoid' - функция активации нейронов 
        """
        super(Net, self).__init__()
        if not isinstance(hidden_cnt, int) or hidden_cnt<1:
            raise ValueError('hidden_cnt must be a natrual number')
        if not isinstance(input_count, int) or input_count<1:
            raise ValueError('input_count must be a natrual number')
        if not isinstance(output_count, int) or output_count<1:
            raise ValueError('output_count must be a natrual number')

        self.act_function_name = act_function
        self.act_function = Net.get_torch_act_function(act_function)
        self.input_layer = nn.Linear(input_count,hidden_cnt)
        self.output_layer = nn.Linear(hidden_cnt, output_count) 
        self.hidden_cnt = hidden_cnt
    def forward(self, x):
        """
        Прямое распространение.
        Не следует менять для синхронизации с генерацией.
        """
        x = self.act_function(self.input_layer(x))
        x = self.act_function(self.output_layer(x))
        return x