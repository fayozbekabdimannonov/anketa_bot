from aiogram.fsm.state import State, StatesGroup

class AnketaState(StatesGroup):
    ism = State()
    familya = State() 
    tel_raqam = State()
    jinsi = State()
    t_yil = State()
    t_oy = State()
    t_kun =State()
    rasm = State()
    