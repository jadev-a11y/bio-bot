import os
import telebot
from telebot import types
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    """Простой HTTP обработчик для health check"""
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Level Up Developer Bot</title>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #1a1a1a; color: white; }
                    h1 { color: #00d4aa; }
                </style>
            </head>
            <body>
                <h1>🎮 Level Up Developer Bot is Running!</h1>
                <p>✅ Telegram Bot is active and responding</p>
                <p>🚀 Deployed on Render</p>
                <p>📡 Find me in Telegram: @rjr.biobot</p>
                <p>⚡ Status: Online 24/7</p>
                <p>🌐 Languages: English, Русский</p>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            logger.error(f"HTTP handler error: {e}")
    
    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
        except Exception as e:
            logger.error(f"HTTP HEAD error: {e}")
    
    def log_message(self, format, *args):
        return

def keep_alive():
    """HTTP сервер для Render health check"""
    try:
        port = int(os.environ.get('PORT', 8000))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        logger.info(f"🌐 HTTP server starting on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"HTTP server error: {e}")

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found!")
    exit(1)

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище для языков пользователей и попыток паролей
user_languages = {}
user_password_attempts = {}
SECRET_PASSWORD = "lchn18"

# Языковые настройки
LANGUAGES = {
    'en': '🇬🇧 English',
    'ru': '🇷🇺 Русский'
}

# Переводы
translations = {
    'welcome': {
        'en': """🌟 **Welcome {name} to my personal universe!** 🌟

👋 Hi there! I'm a **15-year-old tech enthusiast** from Central Asia who's passionate about creating digital experiences that matter.

🚀 **What I do:**
• Full-stack web development (Frontend + Backend)
• Custom websites tailored to any taste
• Telegram bots that actually work
• And pretty much anything tech-related!

💬 **Fun fact:** I can start a conversation about literally anything and keep it going - try me! 😄

**Choose what you'd like to know about me:**""",
        'ru': """🌟 **Добро пожаловать {name} в мою личную вселенную!** 🌟

👋 Привет! Я **15-летний энтузиаст технологий** из Центральной Азии, который увлечен созданием цифровых решений, которые действительно важны.

🚀 **Чем я занимаюсь:**
• Full-stack веб-разработка (Frontend + Backend)
• Кастомные сайты под любой вкус
• Telegram боты, которые реально работают
• И практически всё, что связано с технологиями!

💬 **Интересный факт:** Я могу начать разговор о чём угодно и поддержать его - попробуйте! 😄

**Выберите, что вы хотели бы узнать обо мне:**"""
    },
    
    'password_prompt': {
        'en': '🔐 **Access to Personal Information**\n\nThis section contains private details about my real personality, hobbies, and personal life beyond the professional side.\n\n🔑 **Please enter the access code to continue:**\n\n💡 *Hint: Special combination from my personal life*',
        'ru': '🔐 **Доступ к личной информации**\n\nЭтот раздел содержит личные детали о моей настоящей личности, хобби и личной жизни за пределами профессиональной стороны.\n\n🔑 **Пожалуйста, введите код доступа для продолжения:**\n\n💡 *Подсказка: Особая комбинация из моей личной жизни*'
    },
    
    'wrong_password': {
        'en': '❌ **Access Denied**\n\n🚫 Incorrect access code. Please try again.\n\n💡 *Hint: Think about something very personal to me*\n\n🔄 **Attempts remaining: {attempts}**',
        'ru': '❌ **Доступ запрещен**\n\n🚫 Неверный код доступа. Попробуйте еще раз.\n\n💡 *Подсказка: Подумайте о чем-то очень личном для меня*\n\n🔄 **Осталось попыток: {attempts}**'
    },
    
    'access_blocked': {
        'en': '🚨 **Access Temporarily Blocked**\n\n⏰ Too many incorrect attempts. Access to personal information is temporarily restricted.\n\n🔄 **Try again later or contact me directly.**',
        'ru': '🚨 **Доступ временно заблокирован**\n\n⏰ Слишком много неверных попыток. Доступ к личной информации временно ограничен.\n\n🔄 **Попробуйте позже или свяжитесь со мной напрямую.**'
    },
    
    'message_reply': {
        'en': """Thanks for the message! 😊

I'm a 15-year-old developer from Central Asia who loves creating amazing digital experiences!

Use /start to see the main menu with all my information, or just keep chatting - I love talking about tech, projects, or literally anything! 🚀

What would you like to know about me?""",
        'ru': """Спасибо за сообщение! 😊

Я 15-летний разработчик из Центральной Азии, который любит создавать удивительные цифровые решения!

Используйте /start чтобы увидеть главное меню со всей информацией обо мне, или просто продолжайте общаться - я люблю говорить о технологиях, проектах или буквально о чём угодно! 🚀

Что вы хотели бы узнать обо мне?"""
    },
    
    'back_to_menu': {
        'en': '🔙 Back to Menu',
        'ru': '🔙 Назад в меню'
    },
    
    'change_lang': {
        'en': '🌐 Change Language',
        'ru': '🌐 Изменить язык'
    }
}

# Кнопки меню
menu_buttons = {
    'about': {
        'en': '👤 About Me',
        'ru': '👤 Обо мне'
    },
    'skills': {
        'en': '💻 Skills',
        'ru': '💻 Навыки'
    },
    'projects': {
        'en': '🚀 Projects',
        'ru': '🚀 Проекты'
    },
    'contact': {
        'en': '📧 Contact',
        'ru': '📧 Контакты'
    },
    'languages': {
        'en': '🌍 Languages',
        'ru': '🌍 Языки'
    },
    'interests': {
        'en': '🎯 Interests',
        'ru': '🎯 Интересы'
    },
    'personal_info': {
        'en': '🔒 Personal Information',
        'ru': '🔒 Личная информация'
    }
}

def get_user_language(user_id):
    """Получить язык пользователя"""
    return user_languages.get(user_id, 'en')

def set_user_language(user_id, lang):
    """Установить язык пользователя"""
    user_languages[user_id] = lang

def t(key, user_id, **kwargs):
    """Получить перевод для пользователя"""
    lang = get_user_language(user_id)
    text = translations.get(key, {}).get(lang, translations.get(key, {}).get('en', key))
    return text.format(**kwargs)

def create_language_menu():
    """Создает меню выбора языка"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for lang_code, lang_name in LANGUAGES.items():
        btn = types.InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}")
        markup.add(btn)
    
    return markup

def create_main_menu(user_id):
    """Создает главное меню с кнопками на нужном языке"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    lang = get_user_language(user_id)
    
    btn1 = types.InlineKeyboardButton(menu_buttons['about'][lang], callback_data="about")
    btn2 = types.InlineKeyboardButton(menu_buttons['skills'][lang], callback_data="skills")
    btn3 = types.InlineKeyboardButton(menu_buttons['projects'][lang], callback_data="projects")
    btn4 = types.InlineKeyboardButton(menu_buttons['contact'][lang], callback_data="contact")
    btn5 = types.InlineKeyboardButton(menu_buttons['languages'][lang], callback_data="languages")
    btn6 = types.InlineKeyboardButton(menu_buttons['interests'][lang], callback_data="interests")
    btn7 = types.InlineKeyboardButton(menu_buttons['personal_info'][lang], callback_data="personal_info")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7)
    
    # Добавляем кнопку смены языка
    lang_btn = types.InlineKeyboardButton(t('change_lang', user_id), callback_data="change_lang")
    markup.add(lang_btn)
    
    return markup

def create_back_menu(user_id):
    """Создает кнопку Назад на нужном языке"""
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton(t('back_to_menu', user_id), callback_data="menu")
    markup.add(back_btn)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    """Команда /start"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Friend"
    
    # Если язык не установлен, показываем выбор языка
    if user_id not in user_languages:
        text = translations['language_select']['en']
        markup = create_language_menu()
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
    else:
        # Показываем главное меню на выбранном языке
        text = t('welcome', user_id, name=user_name)
        markup = create_main_menu(user_id)
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    """Команда /help"""
    user_id = message.from_user.id
    text = t('help_text', user_id)
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['lang'])
def lang_command(message):
    """Команда смены языка"""
    text = translations['language_select']['en']
    markup = create_language_menu()
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик нажатий на кнопки"""
    user_id = call.from_user.id
    
    # Обработка выбора языка
    if call.data.startswith('lang_'):
        lang_code = call.data.replace('lang_', '')
        if lang_code in LANGUAGES:
            set_user_language(user_id, lang_code)
            
            # Подтверждение смены языка
            confirmation_text = t('language_changed', user_id)
            bot.edit_message_text(confirmation_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            
            # Показываем главное меню
            user_name = call.from_user.first_name or "Friend"
            text = t('welcome', user_id, name=user_name)
            markup = create_main_menu(user_id)
            bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
    
    # Смена языка из главного меню
    elif call.data == "change_lang":
        text = translations['language_select']['en']
        markup = create_language_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown')
    
    # Возврат в главное меню
    elif call.data == "menu":
        user_name = call.from_user.first_name or "Friend"
        text = t('welcome', user_id, name=user_name)
        markup = create_main_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    # Обработка основных разделов
    elif call.data == "about":
        text = t('about_me', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "skills":
        text = t('skills', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "projects":
        text = t('projects', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "contact":
        text = t('contact', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "languages":
        text = t('languages', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "interests":
        text = t('interests', user_id)
        markup = create_back_menu(user_id)
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    # Секретный раздел
    elif call.data == "personal_info":
        # Инициализируем попытки пользователя
        if user_id not in user_password_attempts:
            user_password_attempts[user_id] = 3
        
        if user_password_attempts[user_id] <= 0:
            text = t('access_blocked', user_id)
            markup = create_back_menu(user_id)
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=markup, parse_mode='Markdown')
        else:
            text = t('password_prompt', user_id)
            markup = create_back_menu(user_id)
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                                 reply_markup=markup, parse_mode='Markdown')
            
            # Устанавливаем состояние ожидания пароля
            user_languages[user_id + 1000000] = 'waiting_password'

    # Подтверждение обработки callback
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех остальных сообщений"""
    user_id = message.from_user.id
    
    # Проверяем, ждем ли мы пароль от пользователя
    if user_languages.get(user_id + 1000000) == 'waiting_password':
        user_languages.pop(user_id + 1000000, None)  # Убираем состояние
        
        if message.text == SECRET_PASSWORD:
            # Правильный пароль!
            text = t('personal_info_content', user_id)
            markup = create_back_menu(user_id)
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
            
            # Сбрасываем попытки
            user_password_attempts[user_id] = 3
        else:
            # Неправильный пароль
            user_password_attempts[user_id] -= 1
            attempts_left = user_password_attempts[user_id]
            
            if attempts_left > 0:
                text = t('wrong_password', user_id, attempts=attempts_left)
                markup = create_back_menu(user_id)
                bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
            else:
                text = t('access_blocked', user_id)
                markup = create_back_menu(user_id)
                bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
        return
    
    # Обычная обработка сообщений
    text = t('message_reply', user_id)
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

if __name__ == "__main__":
    try:
        # Запускаем HTTP сервер в отдельном потоке
        http_thread = Thread(target=keep_alive)
        http_thread.daemon = True
        http_thread.start()
        
        # Запускаем Telegram бота
        logger.info("🤖 Multilingual Bot is starting...")
        logger.info("🌐 Supported languages: English, Русский")
        logger.info("🚀 Bot is now ready to receive users!")
        
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error: {e}")
    
    'language_select': {
        'en': '🌐 **Select your language / Выберите язык:**',
        'ru': '🌐 **Select your language / Выберите язык:**'
    },
    
    'language_changed': {
        'en': '✅ Language changed to English!',
        'ru': '✅ Язык изменен на русский!'
    },
    
    'help_text': {
        'en': """❓ **How to Navigate This Bot**

**Available Commands:**
• `/start` - Main menu and welcome
• `/help` - This help message
• `/lang` - Change language

**Interactive Menu:**
Use the buttons to explore different sections:
👤 **About Me** - My full story and background
💻 **Skills** - Technical abilities and tools
🚀 **Projects** - Portfolio and achievements
📧 **Contact** - How to reach me
🌍 **Languages** - Multilingual capabilities
🎯 **Interests** - My hobbies and passions
🔒 **Personal Information** - Private details (password protected)

**💡 Pro Tips:**
• Each section has detailed information
• Use "Back to Menu" to navigate easily
• Contact me directly for specific questions
• I respond to all messages personally!

**Questions? Just ask!** 
I love talking to people and discussing new ideas! 🚀""",
        'ru': """❓ **Как пользоваться этим ботом**

**Доступные команды:**
• `/start` - Главное меню и приветствие
• `/help` - Это сообщение помощи
• `/lang` - Изменить язык

**Интерактивное меню:**
Используйте кнопки для изучения разных разделов:
👤 **Обо мне** - Моя полная история и биография
💻 **Навыки** - Технические способности и инструменты
🚀 **Проекты** - Портфолио и достижения
📧 **Контакты** - Как со мной связаться
🌍 **Языки** - Многоязычные возможности
🎯 **Интересы** - Мои хобби и увлечения
🔒 **Личная информация** - Приватные детали (защищено паролем)

**💡 Полезные советы:**
• В каждом разделе есть подробная информация
• Используйте "Назад в меню" для удобной навигации
• Обращайтесь ко мне напрямую с конкретными вопросами
• Я отвечаю на все сообщения лично!

**Есть вопросы? Просто спрашивайте!** 
Я люблю общаться с людьми и обсуждать новые идеи! 🚀"""
    },
    
    'about_me': {
        'en': """👨‍💻 **About Me - The Full Story**

🎂 **Age:** 15 years old (yeah, I started early!)
🌍 **Location:** Central Asia 
🎯 **Mission:** Building the digital future, one project at a time

**My Journey:**
🚀 Started coding because I was curious about how websites work
💡 Quickly realized I love both frontend beauty AND backend logic
🌟 Now I create full-stack solutions that people actually enjoy using

**What makes me unique:**
✨ I'm genuinely passionate about EVERYTHING - tech, culture, science, you name it
🗣️ Master conversationalist - I can discuss quantum physics or favorite pizza toppings with equal enthusiasm
🔧 Problem solver by nature - if it exists, I can probably figure out how to improve it
🌈 Diverse perspective from Central Asia brings fresh ideas to every project

**Philosophy:**
"Age is just a number when you have passion and dedication. I might be 15, but my code speaks louder than my birth certificate!" 💪

Ready to see what I can do? Check out my skills and projects! 🚀""",
        'ru': """👨‍💻 **Обо мне - Полная история**

🎂 **Возраст:** 15 лет (да, я начал рано!)
🌍 **Местоположение:** Центральная Азия
🎯 **Миссия:** Строить цифровое будущее, проект за проектом

**Мой путь:**
🚀 Начал программировать из любопытства к тому, как работают сайты
💡 Быстро понял, что люблю и красоту frontend'а, И логику backend'а
🌟 Теперь создаю full-stack решения, которыми люди действительно наслаждаются

**Что делает меня уникальным:**
✨ Я искренне увлечен ВСЕМ - технологиями, культурой, наукой, чем угодно
🗣️ Мастер общения - могу обсуждать квантовую физику или любимую пиццу с одинаковым энтузиазмом
🔧 Решатель проблем по природе - если что-то существует, я вероятно смогу понять, как это улучшить
🌈 Разнообразная перспектива из Центральной Азии привносит свежие идеи в каждый проект

**Философия:**
"Возраст - это просто число, когда у тебя есть страсть и преданность. Мне может быть 15, но мой код говорит громче моего свидетельства о рождении!" 💪

Готовы увидеть, что я умею? Загляните в мои навыки и проекты! 🚀"""
    },
    
    'skills': {
        'en': """💻 **My Technical Arsenal**

**Frontend Development:**
🎨 HTML5, CSS3, JavaScript (ES6+)
⚡ React.js, Vue.js
🎯 Responsive Design & Mobile-First
✨ CSS Animations & Interactions
🖼️ UI/UX Design Principles

**Backend Development:**
🐍 Python (Django, Flask)
🟢 Node.js, Express.js
🗄️ Database Design (SQL, NoSQL)
🔐 API Development & Security
☁️ Cloud Services & Deployment

**Bot Development:**
🤖 Telegram Bot API Expert
⚙️ Complex Logic & Automation
💬 Natural Conversation Flow
📊 Data Processing & Analytics

**Tools & Technologies:**
🛠️ Git, GitHub, VS Code
🚀 Docker, Linux
📱 Figma, Adobe Creative Suite
🌐 Netlify, Heroku, Railway

**Soft Skills:**
🗣️ Excellent Communication (2 languages!)
🧠 Quick Learner & Problem Solver
🤝 Team Collaboration
💡 Creative Thinking

**Currently Learning:**
📚 Advanced React Patterns
🔮 Machine Learning Basics
🎮 Game Development with Unity

**Fun Fact:** I learn new technologies faster than most people learn new games! 🎯""",
        'ru': """💻 **Мой технический арсенал**

**Frontend разработка:**
🎨 HTML5, CSS3, JavaScript (ES6+)
⚡ React.js, Vue.js
🎯 Адаптивный дизайн и Mobile-First
✨ CSS анимации и взаимодействия
🖼️ Принципы UI/UX дизайна

**Backend разработка:**
🐍 Python (Django, Flask)
🟢 Node.js, Express.js
🗄️ Дизайн баз данных (SQL, NoSQL)
🔐 Разработка API и безопасность
☁️ Облачные сервисы и деплой

**Разработка ботов:**
🤖 Эксперт Telegram Bot API
⚙️ Сложная логика и автоматизация
💬 Естественный поток разговора
📊 Обработка данных и аналитика

**Инструменты и технологии:**
🛠️ Git, GitHub, VS Code
🚀 Docker, Linux
📱 Figma, Adobe Creative Suite
🌐 Netlify, Heroku, Railway

**Мягкие навыки:**
🗣️ Отличное общение (2 языка!)
🧠 Быстрое обучение и решение проблем
🤝 Командная работа
💡 Творческое мышление

**Сейчас изучаю:**
📚 Продвинутые паттерны React
🔮 Основы машинного обучения
🎮 Разработка игр с Unity

**Интересный факт:** Я изучаю новые технологии быстрее, чем большинство людей изучают новые игры! 🎯"""
    },
    
    'projects': {
        'en': """🚀 **My Project Showcase**

**🌟 Featured Projects:**

**1. 🌌 Cosmic Portfolio Website**
• Beautiful space-themed personal website
• Custom CSS animations & particle effects
• Fully responsive design
• Tech: HTML5, CSS3, JavaScript
• *Status: Featured on developer communities*

**2. 🤖 AI-Powered Telegram Bots**
• Multiple bots with advanced conversation logic
• User analytics & data processing
• Custom admin panels
• Tech: Python, PostgreSQL, Docker
• *Used by 1000+ active users*

**3. 💼 Business Landing Pages**
• Custom websites for local businesses
• SEO optimization & performance tuning
• Content management systems
• Tech: React.js, Node.js, MongoDB
• *100% client satisfaction rate*

**4. 🎮 Interactive Web Games**
• Browser-based games with real-time features
• Multiplayer functionality
• Progressive Web App capabilities
• Tech: JavaScript, WebSockets, Canvas API

**5. 📱 Mobile-First Web Apps**
• Responsive applications that feel native
• Offline functionality with service workers
• Push notifications integration
• Tech: Vue.js, PWA technologies

**🔥 What I Can Build for You:**
• E-commerce platforms
• Social media applications
• Educational platforms
• Gaming websites
• Business automation tools
• And literally anything you can imagine!

**Philosophy:** "Every project is a chance to create something amazing and learn something new!" ✨

Want to see live demos? Contact me! 📧""",
        'ru': """🚀 **Витрина моих проектов**

**🌟 Избранные проекты:**

**1. 🌌 Космический портфолио сайт**
• Красивый персональный сайт в космической тематике
• Кастомные CSS анимации и эффекты частиц
• Полностью адаптивный дизайн
• Технологии: HTML5, CSS3, JavaScript
• *Статус: Представлен в сообществах разработчиков*

**2. 🤖 Telegram боты с ИИ**
• Несколько ботов с продвинутой логикой разговора
• Аналитика пользователей и обработка данных
• Кастомные админ панели
• Технологии: Python, PostgreSQL, Docker
• *Используется 1000+ активными пользователями*

**3. 💼 Бизнес лендинги**
• Кастомные сайты для местного бизнеса
• SEO оптимизация и настройка производительности
• Системы управления контентом
• Технологии: React.js, Node.js, MongoDB
• *100% удовлетворенность клиентов*

**4. 🎮 Интерактивные веб-игры**
• Браузерные игры с функциями реального времени
• Многопользовательская функциональность
• Возможности Progressive Web App
• Технологии: JavaScript, WebSockets, Canvas API

**5. 📱 Mobile-First веб-приложения**
• Адаптивные приложения, которые ощущаются как нативные
• Оффлайн функциональность с service workers
• Интеграция push уведомлений
• Технологии: Vue.js, PWA технологии

**🔥 Что я могу создать для вас:**
• E-commerce платформы
• Приложения социальных сетей
• Образовательные платформы
• Игровые сайты
• Инструменты автоматизации бизнеса
• И буквально всё, что вы можете представить!

**Философия:** "Каждый проект - это шанс создать что-то удивительное и изучить что-то новое!" ✨

Хотите увидеть живые демо? Свяжитесь со мной! 📧"""
    },
    
    'contact': {
        'en': """📧 **Let's Connect & Build Something Amazing!**

**Direct Contact:**
📩 **Email:** orbitskill@gmail.com
💬 **Telegram:** @oxygw
🐙 **GitHub:** github.com/jadev-a11y

**💼 Available for:**
✅ Custom Website Development
✅ Telegram Bot Creation
✅ Full-Stack Web Applications
✅ UI/UX Design & Consultation
✅ Code Review & Mentoring
✅ Tech Discussions & Brainstorming

**🕒 Response Time:**
• Usually within 2-4 hours
• Emergency projects: Within 30 minutes
• Time Zone: UTC+5 (Central Asia)

**💰 Collaboration:**
• Student-friendly rates
• Portfolio projects (sometimes free for interesting ideas!)
• Long-term partnerships available
• Always up for innovative challenges

**🎯 Perfect Projects for Me:**
• Startups needing MVP development
• Students learning web development
• Small businesses going digital
• Creative projects with unique requirements

**📞 How to Reach Me:**
1. **Quick Questions:** Telegram (fastest response)
2. **Business Inquiries:** Email (detailed proposals)
3. **Code Collaboration:** GitHub (let's build together!)

**Fun Challenge:** Message me with your wildest project idea - I bet I can figure out how to make it happen! 🚀

*"Great ideas deserve great execution. Let's make it happen!"* ✨""",
        'ru': """📧 **Давайте свяжемся и создадим что-то удивительное!**

**Прямой контакт:**
📩 **Email:** orbitskill@gmail.com
💬 **Telegram:** @oxygw
🐙 **GitHub:** github.com/jadev-a11y

**💼 Доступен для:**
✅ Разработки кастомных сайтов
✅ Создания Telegram ботов
✅ Full-Stack веб-приложений
✅ UI/UX дизайна и консультаций
✅ Ревью кода и менторства
✅ Технических обсуждений и мозгового штурма

**🕒 Время ответа:**
• Обычно в течение 2-4 часов
• Срочные проекты: в течение 30 минут
• Часовой пояс: UTC+5 (Центральная Азия)

**💰 Сотрудничество:**
• Студенческие тарифы
• Портфолио проекты (иногда бесплатно для интересных идей!)
• Долгосрочные партнерства доступны
• Всегда готов к инновационным вызовам

**🎯 Идеальные проекты для меня:**
• Стартапы, нуждающиеся в разработке MVP
• Студенты, изучающие веб-разработку
• Малый бизнес, переходящий в цифру
• Творческие проекты с уникальными требованиями

**📞 Как со мной связаться:**
1. **Быстрые вопросы:** Telegram (самый быстрый ответ)
2. **Бизнес запросы:** Email (подробные предложения)
3. **Код сотрудничество:** GitHub (давайте строить вместе!)

**Веселый вызов:** Напишите мне свою самую дикую идею проекта - держу пари, я смогу понять, как это осуществить! 🚀

*"Отличные идеи заслуживают отличного исполнения. Давайте воплотим это в жизнь!"* ✨"""
    },
    
    'languages': {
        'en': """🌍 **Multilingual Communication**

**🗣️ Languages I Speak:**

**🇺🇸 English** - Fluent
• Professional communication
• Technical documentation
• International project collaboration
• *Can explain complex concepts simply*

**🇷🇺 Русский** - Native
• Comfortable with technical terms
• Business communication
• Cultural nuances understanding
• *Perfect for CIS market projects*

**💡 Communication Superpowers:**
✨ Can explain technical concepts in both languages
🌐 Perfect for international teams
🤝 Cultural sensitivity in global projects
📚 Translate technical documentation
🎯 Adapt communication style to audience

**🚀 What This Means for Your Project:**
• No language barriers in development
• Better understanding of diverse user needs
• Culturally appropriate solutions
• Effective team communication

**Fun Fact:** I dream in code, but I debug in two languages! 😄

**Bonus:** I'm also learning:
🇰🇷 Korean (K-pop influence! 🎵)
🇯🇵 Japanese (Anime and tech culture)""",
        'ru': """🌍 **Многоязычное общение**

**🗣️ Языки, на которых я говорю:**

**🇺🇸 English** - Свободно
• Профессиональное общение
• Техническая документация
• Международное сотрудничество по проектам
• *Могу объяснить сложные концепции просто*

**🇷🇺 Русский** - Родной
• Комфортно с техническими терминами
• Деловое общение
• Понимание культурных нюансов
• *Идеально для проектов рынка СНГ*

**💡 Суперспособности общения:**
✨ Могу объяснить технические концепции на обоих языках
🌐 Идеально для международных команд
🤝 Культурная чувствительность в глобальных проектах
📚 Перевожу техническую документацию
🎯 Адаптирую стиль общения к аудитории

**🚀 Что это означает для вашего проекта:**
• Никаких языковых барьеров в разработке
• Лучшее понимание потребностей разных пользователей
• Культурно подходящие решения
• Эффективное командное общение

**Интересный факт:** Я мечтаю в коде, но отлаживаю на двух языках! 😄

**Бонус:** Я также изучаю:
🇰🇷 Корейский (влияние K-pop! 🎵)
🇯🇵 Японский (Аниме и технологическая культура)"""
    },
    
    'interests': {
        'en': """🎯 **My Universe of Interests**

**🔧 Technology & Innovation:**
• Latest gadgets and tech trends
• AI and machine learning developments
• Blockchain and cryptocurrency
• IoT and smart home automation
• Space technology and exploration

**🎮 Digital Culture:**
• Video game development and design
• Streaming technology
• Digital art and NFTs
• Virtual and augmented reality
• Cybersecurity and ethical hacking

**🌟 Creative Pursuits:**
• UI/UX design trends
• Digital photography
• Video editing and motion graphics
• Music production (electronic beats!)
• 3D modeling and animation

**🧠 Learning & Growth:**
• Online courses and certifications
• Tech podcasts and YouTube channels
• Open source contributions
• Hackathons and coding competitions
• Teaching others what I know

**🌍 Global Perspective:**
• Different cultures and traditions
• International business practices
• Language learning techniques
• Travel and geography
• Global economic trends

**⚡ Random Facts About Me:**
• I can fix almost any tech problem (friends call me "Tech Support")
• Love discussing everything from quantum physics to pizza preferences
• Always excited about new challenges and learning opportunities
• Believe that age is just a number when you have passion
• Can turn any boring topic into an interesting conversation

**🚀 My Philosophy:**
"Life is too short to be bored. There's always something fascinating to discover, create, or improve!" ✨""",
        'ru': """🎯 **Моя вселенная интересов**

**🔧 Технологии и инновации:**
• Последние гаджеты и технологические тренды
• Разработки ИИ и машинного обучения
• Блокчейн и криптовалюты
• IoT и автоматизация умного дома
• Космические технологии и исследования

**🎮 Цифровая культура:**
• Разработка и дизайн видеоигр
• Стриминговые технологии
• Цифровое искусство и NFT
• Виртуальная и дополненная реальность
• Кибербезопасность и этичный хакинг

**🌟 Творческие занятия:**
• Тренды UI/UX дизайна
• Цифровая фотография
• Видеомонтаж и моушн-графика
• Музыкальное производство (электронные биты!)
• 3D моделирование и анимация

**🧠 Обучение и рост:**
• Онлайн курсы и сертификации
• Технические подкасты и YouTube каналы
• Вклад в open source
• Хакатоны и соревнования по программированию
• Обучение других тому что знаю 

**🌍 Глобальная перспектива:**
• Разные культуры и традиции
• Международные бизнес-практики
• Техники изучения языков
• Путешествия и география
• Глобальные экономические тренды

**⚡ Случайные факты обо мне:**
• Могу починить почти любую техническую проблему (друзья называют меня "Техподдержка")
• Люблю обсуждать всё от квантовой физики до предпочтений в пицце
• Всегда в восторге от новых вызовов и возможностей обучения
• Верю, что возраст - просто число, когда есть страсть
• Могу превратить любую скучную тему в интересный разговор

**🚀 Моя философия:**
"Жизнь слишком коротка, чтобы скучать. Всегда есть что-то увлекательное для открытия, создания или улучшения!" ✨"""
    },
    
    'personal_info_content': {
        'en': '''🔓 **Personal Information - Access Granted**

👋 **The Real Me:**
• Name: Jasur, 15 years old, Tashkent
• Location: Yangikhayat district (but I'm cool with people from anywhere!)
• Born: November 18, 2010 🎂

😊 **My Personality:**
• I'm a unique person - want to be sad? Let's go! Want to have fun? Let's go! Want to cringe? Let's go! Want to be serious? Let's go!
• I can talk about absolutely anything - just don't reply to my long texts with "okay" 😁
• I can adapt to your communication style, matching status or avatar - no problem! 🥹
• I'm a terrible socialphobe 🫣 but somehow still love meeting new people

🎵 **My Daily Life:**
• Music 24/7 - always in headphones 🎧
• Always online on Telegram, if not - I'll still see the notification and reply instantly
• I'm the person who responds in split seconds ⚡
• Love trying everything new, I'm into almost everything
• Love growing flames on TikTok 🥰

☕ **My Favorites:**
• Tea with lemon and coffee are my life! ☕🍋
• I love staying up all night - sleep is overrated 🌙
• Listening to music at night hits different 🎶
• Reading books late at night is my therapy 📚

💭 **My Vibe:**
• Generally comfortable and cheerful person
• But when needed, we can be sad together 🥲
• I can start a conversation on any topic
• Love deep night conversations over tea

---
*This is who I really am when I'm not being all professional! Thanks for getting to know the real Jasur! 🚀*''',

        'ru': '''🔓 **Личная информация - Доступ разрешен**

👋 **Настоящий я:**
• Имя: Жасур, 15 лет, Ташкент
• Район: Янгихайятский (но мне все равно откуда вы, главное чтобы было о чем поговорить!)
• Родился: 18 ноября 2010 года 🎂

😊 **Моя личность:**
• Я уникальный человек - погрустить? Го! Повеселиться? Го! Покринжовать? Го! Быть серьёзными? Го!
• Со мной можно поговорить о чём только можно - главное не отвечайте на большой текст «понятно» 😁
• Могу подстроиться под ваш стиль общения, парный статус или аватарка - без проблем! 🥹
• Я жуткий социофоб 🫣 но почему-то все равно люблю знакомиться

🎵 **Моя повседневность:**
• Музыка 24/7 - постоянно в наушниках 🎧
• Онлайн в телеграмме всегда, если нет то все равно увижу уведомление и сразу отвечу
• Я человек который отвечает за долю секунды ⚡
• Обожаю пробовать все новое, шарю почти за все
• Растить огонёк в тиктоке - обожаю 🥰

☕ **Мои любимые вещи:**
• Чай с лимоном и кофе - моя жизнь! ☕🍋
• Обожаю не спать по ночам - сон переоценен 🌙
• Слушать музыку по ночам - это особое настроение 🎶
• Читать книги поздно ночью - моя терапия 📚

💭 **Мой характер:**
• Вообще я комфортный и жизнерадостный
• Но когда надо можем и погрустить 🥲
• Умею заводить разговор на любые темы
• Люблю глубокие ночные разговоры за чаем

---
*Вот какой я на самом деле, когда не изображаю профессионала! Спасибо что познакомились с настоящим Жасуром! 🚀*'''
