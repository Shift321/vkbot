text_for_admins = """Что бы вы хотели сделать?
                    записать новый препарат - запись
                    изменить дозировку препарата - изменить.
                    Удалить препарат из базы данных - удалить.
                    Поиск препарата по активному веществу - поиск по ав.
                    Поиск препарата по названия - поиск.
                    Если захотите вернуться в меню просто напишите отмена."""
text_for_users = """Что бы вы хотели сделать?
                 Поиск препарата по активному веществу - поиск по ав.
                 Поиск препарата по названия - поиск.
                 Если захотите вернуться в меню просто напишите отмена."""
format_of_write = """Введите название препарата и дозировку в формате:"
                     (Действующеее вещество):
                     (Коммерческое название):
                     (форма выпуска):
                     (Фарм группа):
                     (Цель использования):
                     (вид животного):
                     (Доза):
                     (Путь введения):
                     (кратность):
                     (Источник)"""
no_aids_with_this_name = """Препарата с таким активным веществом пока , что нет в моей базей данных.
                        Вы можете попробовать поискать другое название либо написать отмена и вернуться в меню."""
exist = "Не понимаю."


admins_id ={386837528, 422345800}
states = {}
aids_message = {}
words = ["поиск", "поиск по ав", "изменить", "удалить", "запись","меню","отмена"]
cancel = ["меню", "отмена"]