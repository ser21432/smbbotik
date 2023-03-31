import telebot
import re
from telebot import types

bot = telebot.TeleBot('5977391979:AAH6CDRxAUrV-yY8w7A_vB-mmft4GqeukHw')

#m_List = {}

IsBotWorking = False
    
startFirstChecker = False
startSecondChecker = False
startThirdChecker = False
userForm = False
phoneNum = False
choiceTrain = False
FinishTrainChoice = False
order = ""

@bot.message_handler(commands=['start','restart'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Запустить")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "👋 Привет! Я помогу тебе настроить твой будущий поезд!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message): 

    global IsBotWorking
    global startFirstChecker
    global startSecondChecker
    global startThirdChecker
    global choiceTrain
    global order
    global userForm
    global FinishTrainChoice
    global phoneNum

    def FirstPoint(message):
        global startFirstChecker
        global startSecondChecker
        global order
        global IsBotWorking
        IsBotWorking = True
        if message.text.isdigit() and int(message.text) >= 10 and int(message.text) <= 150:
            if message.text != 'Запустить':
                bot.send_message(message.from_user.id, 'Введите длинну')
                order +=  "Высота: " + message.text + "мм\n"
                startSecondChecker = True
                startFirstChecker = False
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз высоту!")

    def SecondPoint(message):
        global order
        global startSecondChecker
        global startThirdChecker
        
        if message.text.isdigit() and int(message.text) >= 10 and int(message.text) <= 150:
            if order != order + message.text:
                bot.send_message(message.from_user.id, 'Введите ширину')
                order += "Длинна: " + message.text + "мм\n"
                startSecondChecker = False
                startThirdChecker = True
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз длинну!")

    def ThirdPoint(message):
        global order
        global startFirstChecker
        global startThirdChecker
        global phoneNum
        if message.text.isdigit() and int(message.text) >= 10 and int(message.text) <= 150:
            if order != order + message.text:
                order += "Ширина: " + message.text + "мм\n"
                startFirstChecker = False
                startThirdChecker = False
                bot.send_message(message.from_user.id, "Для завершения заказа введите свой номер телефона через 7 без +")
                phoneNum = True
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз ширину!")

    def StopBot(message,order):
        global IsBotWorking
        if IsBotWorking == True:
            IsBotWorking = False
            bot.send_message(1204314824, order)
            bot.send_message(message.from_user.id, 'Настройка окончена!\nЗаказ принят, в течении 1 рабочего дня наш менеджер свяжется с вами по указанному телефону для подтверждения заказа.\nИнформацию по заказу вы можете уточнить по номеру:\n+7 (800) 555 35-35')

    def TrainChoice(message):
        woodTrain = open("C:\photos\wood.jpg",'rb')
        bot.send_photo(message.from_user.id,woodTrain,caption="Деревянный")
        plaTrain = open("C:\photos\pla.jpg",'rb')
        bot.send_photo(message.from_user.id,plaTrain,caption="Пластиковый")

        bot.send_message(message.from_user.id, 'Введите "Деревянный"/"Пластиковый" чтобы настроить материал поезда')

    if message.text == 'Запустить':
        bot.send_message(message.from_user.id, "Подсказка: чтобы ввести данные заново, вам нужно перезапустить бота командой /start или /restart")
        bot.send_message(message.from_user.id, 'Для начала создадим вашу анкету!')
        userForm = True
        bot.send_message(message.from_user.id, "Как к вам обращаться?")
    elif userForm == True:
        if message.text.isdigit() == False:
            if order != order + message.text:
                order += "ФИО: " + message.text + "\n"
                choiceTrain = True
                userForm = False
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз без цифр!")
    if choiceTrain == True:
        FinishTrainChoice = True
        choiceTrain = False
        TrainChoice(message)
    elif FinishTrainChoice == True:
        if message.text == "Деревянный" or message.text == "деревянный" or message.text == "Пластиковый" or message.text == "пластиковый":
            if order != order + message.text:
                order += "Поезд: " + message.text + "\n"
                FinishTrainChoice = False
                bot.send_message(message.from_user.id,"Размерности от 10мм до 150мм!")
                bot.send_message(message.from_user.id, "Введите высоту")
                startFirstChecker = True
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз материал поезда!")
    elif startFirstChecker == True:
        FirstPoint(message)
    elif startSecondChecker == True:
        SecondPoint(message)
    elif startThirdChecker == True:
        ThirdPoint(message)
    elif phoneNum == True:
        if message.text.isdigit() == True and len(message.text) == 11:
            #bot.send_message(message.from_user.id, "")
            if order != order + message.text:
                order += "Номер телефона: " + message.text + "\n"
                phoneNum = False
                StopBot(message,order)
        else:
            bot.send_message(message.from_user.id, "Неверный ввод, введите ещё раз номер телефона!")

    

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть