import os
import telebot
from telebot import types
from random import shuffle
import django
django.setup()
from math_test.models import Question

API_TOKEN = '6556025703:AAELbyGavxR9JYf9y4PQY1ATHyYqv2cfAwI'

bot = telebot.TeleBot(API_TOKEN)





bot = telebot.TeleBot(API_TOKEN)
answers = []
questions = []
def data_cell():
    db = Question.objects.all()
    question: Question
    for question in db:
        questions.append(question.question)
        answers.append([question.a, question.b, question.c])

count = 0

def makekeyboard(question_id: int):
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for answer_id, answer in enumerate(answers[question_id]):
        buttons.append(types.InlineKeyboardButton(text=answer, callback_data=f"{question_id}_{answer_id}"))
    shuffle(buttons)
    for button in buttons:
        markup.add(button)
    return markup

@bot.message_handler(commands=['test'])
def handle_test(msg: types.Message):
    data_cell()
    bot.send_message(chat_id=msg.chat.id,
                    text=questions[0],
                    reply_markup=makekeyboard(0),
                    parse_mode='HTML')

@bot.callback_query_handler(func=lambda call:True)
def handle_answer(cb: types.CallbackQuery):
    global count
    global questions
    global answers
    question_id, answer_id = cb.data.split("_")
    if int(answer_id) == 0:
        count += 1
    if len(questions) > int(question_id) + 1:
        print(cb.data)
        bot.edit_message_text(chat_id=cb.message.chat.id, message_id=cb.message.message_id, text=questions[int(question_id) + 1], reply_markup=makekeyboard(int(question_id) + 1))
    else:
        count = 0
        questions = []
        answers = []
bot.infinity_polling()