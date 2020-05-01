from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vkapi import vk_session
import re
from sql import cursor, conn
from constants import texts, states, admins_id, medicines_message

def send_message(user_id,message):                                                                            #функция , которая отвечает за отправление сообщения
    keyboard = create_keyboard(user_id)
    if message == "handle_admin":
        if user_id in admins_id:
            message = texts["text_for_admins"]
        else:
            message = texts["text_for_users"]    
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0, 'keyboard': keyboard})

def create_keyboard(user_id):                                                                                  # функция создания клавиатуры
    keyboard = VkKeyboard(one_time=False)
    if states[user_id] == "menu":
        keyboard.add_button('Поиск', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Поиск по ав', color=VkKeyboardColor.PRIMARY)
        if user_id in admins_id:
                keyboard.add_button('Запись', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()
                keyboard.add_button('Изменить', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('удалить', color=VkKeyboardColor.PRIMARY)
    else:
        keyboard.add_button('Отмена', color=VkKeyboardColor.PRIMARY)
    keyboard = keyboard.get_keyboard()
    return keyboard

def handle_write(event):                                                                                            # функция для записи нового препарата
    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text) 
    if len(list(regular)) == 0:                                                                                # проверка правильности ввода.
        send_message(event.user_id, "Не правильный формат.")
        return
    sql_write = "SELECT * FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_write, [(regular[0][1])])
    cursor_fetchall = cursor.fetchall()
    if cursor_fetchall == []:
        for i in range(len(list(regular))):
            cursor.execute(f"""INSERT INTO medicines VALUES ("{regular[i][0]}",
                                                        "{regular[i][1]}",
                                                        "{regular[i][2]}",
                                                        "{regular[i][3]}",
                                                        "{regular[i][4]}",
                                                        "{regular[i][5]}",
                                                        "{regular[i][6]}",
                                                        "{regular[i][7]}",
                                                        "{regular[i][8]}",
                                                        "{regular[i][9]}")""")
            conn.commit()
            states[event.user_id] = "menu"
            send_message(event.user_id, "Записано.")
            
            
    else:
        
        send_message(event.user_id, "Такое лекарство уже есть.")   

def handle_edit(event):                                                                                             # функция для изменения параметров припарата
    cursor.execute(f"SELECT * FROM medicines WHERE medicines_name LIKE '%{event.text}%'")
    cursor_fetchall_edit = cursor.fetchall()
    if cursor_fetchall_edit == []:                                                   # Проверка есть ли такой препарат в базе
        send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
        return
    medicines_message[event.user_id] = cursor_fetchall_edit[0][1]
    states[event.user_id] = "edition"
    send_message(event.user_id, texts["format_of_write"])

def handle_edittion(event):                                                                                         # изменение
    regular = re.findall(r"(.+?)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)\:(.+)",event.text)
    for i in range(len(list(regular))):
        cursor.execute(f"""UPDATE medicines SET
                        active_substance = "{regular[i][0]}",
                        medicines_name = "{regular[i][1]}",
                        farm_group = "{regular[i][2]}",
                        release_form = "{regular[i][3]}",
                        target = "{regular[i][4]}",
                        animal = "{regular[i][5]}",
                        dosage = "{regular[i][6]}",
                        ways_to_use = "{regular[i][7]}",
                        how_often = "{regular[i][8]}",
                        source = "{regular[i][9]}",
                        WHERE medicines_name ="{medicines_message[event.user_id]}" """
                        )
    conn.commit()
    states[event.user_id] = "menu"
    send_message(event.user_id, "Изменено")
    
def handle_search_as(event):                                                                                        # функция для поиска по активному веществу
    cursor.execute(f"SELECT * FROM medicines WHERE active_substance LIKE '%{event.text}%'")
    text = cursor.fetchall()
    if event.text == '':
        send_message(event.user_id, texts["exist"])
        return
    else:
        if text == []:                                                                       # проверка есть ли препарат с таким активным веществом в базе
            send_message(event.user_id, texts["no_medicines_with_this_name"])
            states[event.user_id] = "search_as"
            return
        for x in range(len(list(text))):
            message_of_search_as = f"""Действущее вещество: {text[x][0]}
                                        Название препарата: {text[x][1]}
                                        Форма выпуска: {text[x][2]}
                                        Фарм группа: {text[x][3]}
                                        Цель использования: {text[x][4]}
                                        Вид животного: {text[x][5]}
                                        Доза: {text[x][6]}
                                        Путь введения: {text[x][7]}
                                        Кратность: {text[x][8]}
                                        Источник: {text[x][9]}"""
    states[event.user_id] = "menu"
    send_message(event.user_id, message_of_search_as)
    
def handle_search(event):                                                                                           # функция для поиска по названию
    search_as_sql = f"SELECT * FROM medicines WHERE medicines_name LIKE '{event.text}%'COLLATE NOCASE"
    cursor.execute(search_as_sql)
    text = cursor.fetchall()
    if event.text == '':
        send_message(event.user_id, text["exist"])
        return
    else:
        if text == []:
            send_message(event.user_id, texts["no_medicines_with_this_name"])                        # проверка есть ли такой препарат в базе
            states[event.user_id] = "search"
            return
        for x in range(len(list(text))):
            message_of_search_as = f"""Действущее вещество: {text[x][0]}
                                        Название препарата: {text[x][1]}
                                        Форма выпуска: {text[x][2]}
                                        Фарм группа: {text[x][3]}
                                        Цель использования: {text[x][4]}
                                        Вид животного: {text[x][5]}
                                        Доза: {text[x][6]}
                                        Путь введения: {text[x][7]}
                                        Кратность: {text[x][8]}
                                        Источник: {text[x][9]}"""
    states[event.user_id] = "menu"
    send_message(event.user_id, message_of_search_as)

def handle_delete(event):                                                                                           # функция для удаления 
    sql_delete = "SELECT * FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_delete, [(event.text)])
    cursor_fetchall_delte = cursor.fetchall()
    if cursor_fetchall_delte == []:                                                        # проверка есть ли такой препарат в базе
        send_message(event.user_id, "Нет такого препарата попробуйте еще раз.")
        states[event.user_id] = "menu"
        return
    sql_delete = "DELETE FROM medicines WHERE medicines_name =?"
    cursor.execute(sql_delete, ([event.text]))
    conn.commit()
    states[event.user_id] = "menu"
    send_message(event.user_id, "Удалено")

def handle_menu(response,event):                                                                                     # меню
    if response == "меню":
        states[event.user_id] = "menu"
        send_message(event.user_id, "handle_admin")
    elif response == "запись" and event.user_id in admins_id:
        states[event.user_id] = "write"
        send_message(event.user_id, texts["format_of_write"])
    elif response == "изменить" and event.user_id in admins_id:
        states[event.user_id] = "edit"
        send_message(event.user_id, "Введите название препарата, который хотите изменить.")
    elif response == "поиск по ав":
        states[event.user_id] = "search_as"
        send_message(event.user_id, "Введите название действующего вещества,которое хотите посмотреть.")
    elif response == "поиск":
        states[event.user_id] = "search"
        send_message(event.user_id, "Введите название препарата ,которое хотите посмотреть.")
    elif response == "удалить"and event.user_id in admins_id:
        states[event.user_id] = "delete"
        send_message(event.user_id, "Введите название препарата ,которое хотите удалить.")    
    else:
        send_message(event.user_id,texts["exist"]) 