import telebot
from config import token
from logic import globalhelper, fact, progressfact
from telebot import types
bot = telebot.TeleBot(token)

questions = [
    {
        "question": "Что является основной причиной глобального потепления?",
        "options": ["Вулканическая активность", "Парниковый эффект", "Изменение орбиты Земли"],
        "correct": 1
    },
    {
        "question": "Какой газ вносит наибольший вклад в парниковый эффект?",
        "options": ["Углекислый газ (CO2)", "Метан (CH4)", "Водяной пар (H2O)"],
        "correct": 2
    },
    {
        "question": "К каким последствиям приводит повышение средней температуры?",
        "options": ["Понижению уровня океана", "Таянию ледников", "Увеличению площади лесов"],
        "correct": 1
    },
    {
        "question": "Какой год считается самым теплым за всю историю наблюдений?",
        "options": ["2016", "2020", "2023"],
        "correct": 2
    }
]

user_scores = {}


@bot.message_handler(commands=["start"])
def bot_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в GlobalBot!")

@bot.message_handler(commands=["help"])
def bot_help(message):
    bot.send_message(message.chat.id, "/start — приветствие от бота\n/help — помощь\n/globalhelper — случайное решение проблемы глобального потепления\n/fact — случайный факт о глобальном потеплении\n/progressfact — случайное достижение в решении этой проблемы\n/test - мини тест-игра")

@bot.message_handler(commands=["globalhelper"])
def bot_globalhelper(message):
    bot.send_message(message.chat.id, globalhelper())

@bot.message_handler(commands=["fact"])
def bot_fact(message):
    bot.send_message(message.chat.id, fact())

@bot.message_handler(commands=["progressfact"])
def bot_progressfact(message):
    bot.send_message(message.chat.id, progressfact())

@bot.message_handler(commands=["test"])
def start_test(message):
    user_id = message.from_user.id
    user_scores[user_id] = {'current_question': 0, 'score': 0}
    send_question(message, 0)

def send_question(message, question_index):
    question_data = questions[question_index]
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for option in question_data['options']:
        markup.add(types.KeyboardButton(option))
    bot.send_message(message.chat.id, 
                     f"❓ Вопрос {question_index+1}/{len(questions)}:\n\n{question_data['question']}",
                     reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    if user_id not in user_scores:
        bot.reply_to(message, "Нажмите 'Начать тест', чтобы начать викторину.")
        return
    user_data = user_scores[user_id]
    current_q = user_data['current_question']
    if current_q >= len(questions):
        bot.reply_to(message, "Тест уже завершен. Нажмите 'Начать тест', чтобы пройти снова.")
        return
    question_data = questions[current_q]
    if message.text in question_data['options']:
        selected_index = question_data['options'].index(message.text)
        if selected_index == question_data['correct']:
            user_data['score'] += 1
            bot.reply_to(message, "Правильно! Молодец!")
        else:
            correct_text = question_data['options'][question_data['correct']]
            bot.reply_to(message, f"Неправильно. Правильный ответ: {correct_text}")
        user_data['current_question'] += 1
        
        if user_data['current_question'] < len(questions):
            send_question(message, user_data['current_question'])
        else:
            score = user_data['score']
            total = len(questions)
            bot.send_message(message.chat.id, 
                             f"🏁 Тест завершен!\n\nВаш результат: {score} из {total} правильных ответов.\n\n"
                             f"{'Отлично!' if score == total else 'Хорошо!' if score >= total/2 else 'Попробуйте еще раз!'}\n\n"
                             "Нажмите 'Начать тест', чтобы пройти заново.")
            # del user_scores[user_id]
    else:
        bot.reply_to(message, "Пожалуйста, выберите вариант ответа из предложенных кнопок.")

if __name__ == '__main__':
    bot.polling(none_stop=True)












