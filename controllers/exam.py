from aiogram import Dispatcher, types
from main import test, bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup



class QState(StatesGroup):
    Answered = State() 
    Finished = State()
    answers = []
    questionNumber = 0
    result = 0

async def startTest(message: Message, state: FSMContext):
    buttonOk = KeyboardButton('OK')
    buttonNo = KeyboardButton('No')
    startOptions = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
         ).row(buttonOk, buttonNo)
    QState.result = 0
    QState.answers = []
    await state.set_state(QState.Answered)
    await bot.send_message(message.from_user.id, "Let's get started! Press 'OK'.", reply_markup=startOptions)
    # questions = test.find()
    # for el in questions:
    #     testQuestion = (
    #         el['question'] 
    #         + '\n 1) ' + el['variants'][0] 
    #         + '\n 2) ' + el['variants'][1] 
    #         + '\n 3) ' + el['variants'][2]
    #         )
    #     await bot.send_message(message.from_user.id, testQuestion)
async def Test(message: Message, state: FSMContext):
    questions = test.find()
    if QState.questionNumber < len(list(test.find())):
        question = questions[QState.questionNumber]
        testQuestion = (
                question['question'] 
                # + '\n 1) ' + question['variants'][0] 
                # + '\n 2) ' + question['variants'][0] 
                # + '\n 3) ' + question['variants'][2]
                )
        button1 = KeyboardButton(question['variants'][0])
        button2 = KeyboardButton(question['variants'][1])
        button3 = KeyboardButton(question['variants'][2])
        options = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
             ).row(button1, button2, button3)
        QState.questionNumber += 1
        QState.answers.append(message.text)
        await state.set_state(QState.Answered)
        await bot.send_message(message.from_user.id, testQuestion, reply_markup=options)
    else:
        await bot.send_message(message.from_user.id, "No more questions. Tap to /showresults")
        QState.answers.append(message.text)
        QState.questionNumber = 0
        await state.set_state(QState.Finished)
        # await state.finish()

async def showResults(message: Message, state: FSMContext):
    for i in range(len(QState.answers)-1):
        if QState.answers[i+1] == test.find()[i]['answer']:
            QState.result += 1
    await state.finish()
    await bot.send_message(message.from_user.id, "⬇️ This dude got " + str(QState.result) + " right answers out of " + str(len(QState.answers)-1))
    profilePictures = await dp.bot.get_user_profile_photos(message.from_user.id)
    await bot.send_photo(message.from_user.id, dict((profilePictures.photos[0][0])).get("file_id"))

def initTest(dp: Dispatcher):
    dp.register_message_handler(startTest, content_types=['text'], state='*', commands=['testme'])
    dp.register_message_handler(Test, content_types=['text'], state = QState.Answered)
    dp.register_message_handler(showResults, content_types=['text'], state= QState.Finished, commands=['showresults'])