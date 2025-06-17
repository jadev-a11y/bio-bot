import os
import telebot
from telebot import types
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище для языков пользователей (в реальном боте используйте базу данных)
user_languages = {}

# Языковые настройки
LANGUAGES = {
    'en': '🇬🇧 English',
    'ru': '🇷🇺 Русский', 
    'uz': '🇺🇿 O\'zbek'
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

**Choose what you'd like to know about me:**""",
        'ru': """🌟 **Добро пожаловать {name} в мою личную вселенную!** 🌟

👋 Привет! Я **15-летний энтузиаст технологий** из Центральной Азии, который увлечен созданием цифровых решений, которые действительно важны.

🚀 **Чем я занимаюсь:**
• Full-stack веб-разработка (Frontend + Backend)
• Кастомные сайты под любой вкус
• Telegram боты, которые реально работают
• И практически всё, что связано с технологиями!

**Выберите, что вы хотели бы узнать обо мне:**""",
        'uz': """🌟 **Xush kelibsiz {name} mening shaxsiy olamimga!** 🌟

👋 Salom! Men **Markaziy Osiyodan 15 yoshli texnologiya ishqibozi**man va haqiqatan ham muhim bo'lgan raqamli tajribalarni yaratishdan zavqlanaman.

🚀 **Men nima qilaman:**
• To'liq web-ishlab chiqish (Frontend + Backend)
• Har qanday didga mos maxsus veb-saytlar
• Haqiqatan ishlaydigantelegram botlar
• Va texnologiya bilan bog'liq deyarli hamma narsa!

**Men haqimda nimani bilishni xohlaysiz, tanlang:**"""
    },
    
    'language_select': {
        'en': '🌐 **Select your language / Выберите язык / Tilni tanlang:**',
        'ru': '🌐 **Select your language / Выберите язык / Tilni tanlang:**',
        'uz': '🌐 **Select your language / Выберите язык / Tilni tanlang:**'
    },
    
    'language_changed': {
        'en': '✅ Language changed to English!',
        'ru': '✅ Язык изменен на русский!',
        'uz': '✅ Til o\'zbek tiliga o\'zgartirildi!'
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

**💡 Полезные советы:**
• В каждом разделе есть подробная информация
• Используйте "Назад в меню" для удобной навигации
• Обращайтесь ко мне напрямую с конкретными вопросами
• Я отвечаю на все сообщения лично!

**Есть вопросы? Просто спрашивайте!** 
Я люблю общаться с людьми и обсуждать новые идеи! 🚀""",
        'uz': """❓ **Ushbu botdan qanday foydalanish**

**Mavjud buyruqlar:**
• `/start` - Asosiy menyu va salomlashish
• `/help` - Ushbu yordam xabari
• `/lang` - Tilni o'zgartirish

**Interaktiv menyu:**
Turli bo'limlarni o'rganish uchun tugmalardan foydalaning:
👤 **Men haqimda** - Mening to'liq hikoyam va biografiyam
💻 **Ko'nikmalar** - Texnik qobiliyatlar va vositalar
🚀 **Loyihalar** - Portfolio va yutuqlar
📧 **Aloqa** - Men bilan qanday bog'lanish
🌍 **Tillar** - Ko'p tilli imkoniyatlar
🎯 **Qiziqishlar** - Mening sevimli mashg'ulotlarim

**💡 Foydali maslahatlar:**
• Har bir bo'limda batafsil ma'lumot bor
• Qulay navigatsiya uchun "Menyuga qaytish" tugmasini ishlating
• Aniq savollar bilan to'g'ridan-to'g'ri murojaat qiling
• Men barcha xabarlarga shaxsan javob beraman!

**Savollar bormi? Shunchaki so'rang!** 
Men odamlar bilan suhbatlashishni va yangi g'oyalarni muhokama qilishni yaxshi ko'raman! 🚀"""
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

Готовы увидеть, что я умею? Загляните в мои навыки и проекты! 🚀""",
        'uz': """👨‍💻 **Men haqimda - To'liq hikoya**

🎂 **Yosh:** 15 yosh (ha, men ertaroq boshladim!)
🌍 **Joylashuv:** Markaziy Osiyo
🎯 **Missiya:** Raqamli kelajakni qurish, har bir loyiha bilan

**Mening yo'lim:**
🚀 Veb-saytlar qanday ishlashiga qiziqib dasturlashni boshladim
💡 Tezda frontend go'zalligi VA backend mantiqini ham yaxshi ko'rishimni angladim
🌟 Endi odamlar haqiqattan ham foydalanishni yoqtiradigan full-stack yechimlar yarataman

**Meni noyob qiladigan narsa:**
✨ Men chinakam HAMMA NARSAGA ishtiyoqliman - texnologiya, madaniyat, fan, nima bo'lmasin
🗣️ Suhbat ustasi - kvant fizikasi yoki sevimli pizza haqida bir xil ishtiyoq bilan gaplasha olaman
🔧 Tabiatim bo'yicha muammo yechuvchi - agar biror narsa mavjud bo'lsa, uni qanday yaxshilashni tushunib olishim mumkin
🌈 Markaziy Osiyodan turlicha nuqtai nazar har bir loyihaga yangi g'oyalar olib keladi

**Falsafa:**
"Ishtiyoq va fidoiylik bor joyda yosh shunchaki raqam. Men 15 yoshda bo'lishim mumkin, lekin mening kodim tug'ilganlik guvohnomamdan balandroq gapiradi!" 💪

Men nima qila olishimni ko'rishga tayyormisiz? Ko'nikmalarim va loyihalarimni ko'ring! 🚀"""
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
🗣️ Excellent Communication (3 languages!)
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
🗣️ Отличное общение (3 языка!)
🧠 Быстрое обучение и решение проблем
🤝 Командная работа
💡 Творческое мышление

**Сейчас изучаю:**
📚 Продвинутые паттерны React
🔮 Основы машинного обучения
🎮 Разработка игр с Unity

**Интересный факт:** Я изучаю новые технологии быстрее, чем большинство людей изучают новые игры! 🎯""",
        'uz': """💻 **Mening texnik arsenalim**

**Frontend ishlab chiqish:**
🎨 HTML5, CSS3, JavaScript (ES6+)
⚡ React.js, Vue.js
🎯 Moslashuvchan dizayn va Mobile-First
✨ CSS animatsiyalari va o'zaro ta'sirlar
🖼️ UI/UX dizayn tamoyillari

**Backend ishlab chiqish:**
🐍 Python (Django, Flask)
🟢 Node.js, Express.js
🗄️ Ma'lumotlar bazasi dizayni (SQL, NoSQL)
🔐 API ishlab chiqish va xavfsizlik
☁️ Bulut xizmatlari va joylashtirish

**Bot ishlab chiqish:**
🤖 Telegram Bot API mutaxassisi
⚙️ Murakkab mantiq va avtomatlashtirish
💬 Tabiiy suhbat oqimi
📊 Ma'lumotlarni qayta ishlash va tahlil

**Vositalar va texnologiyalar:**
🛠️ Git, GitHub, VS Code
🚀 Docker, Linux
📱 Figma, Adobe Creative Suite
🌐 Netlify, Heroku, Railway

**Yumshoq ko'nikmalar:**
🗣️ Ajoyib muloqot (3 til!)
🧠 Tez o'rganish va muammo yechish
🤝 Jamoa hamkorligi
💡 Ijodiy fikrlash

**Hozir o'rganyapman:**
📚 React'ning ilg'or namunalari
🔮 Mashinali o'rganishning asoslari
🎮 Unity bilan o'yin ishlab chiqish

**Qiziq fakt:** Men yangi texnologiyalarni ko'pchilik yangi o'yinlarni o'rganishidan tezroq o'rganaman! 🎯"""
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

Хотите увидеть живые демо? Свяжитесь со мной! 📧""",
        'uz': """🚀 **Mening loyihalar ko'rgazmasi**

**🌟 Tanlangan loyihalar:**

**1. 🌌 Kosmik portfolio veb-sayt**
• Kosmik mavzudagi chiroyli shaxsiy veb-sayt
• Maxsus CSS animatsiyalari va zarracha effektlari
• To'liq moslashuvchan dizayn
• Texnologiya: HTML5, CSS3, JavaScript
• *Status: Dasturchilar hamjamiyatlarida taqdim etilgan*

**2. 🤖 AI bilan ishlaydigan Telegram botlar**
• Ilg'or suhbat mantiqiga ega bir nechta botlar
• Foydalanuvchi tahlili va ma'lumotlarni qayta ishlash
• Maxsus admin panellari
• Texnologiya: Python, PostgreSQL, Docker
• *1000+ faol foydalanuvchi tomonidan ishlatilmoqda*

**3. 💼 Biznes landing sahifalari**
• Mahalliy biznes uchun maxsus veb-saytlar
• SEO optimallashtirish va ishlash sozlamalari
• Kontent boshqaruv tizimlari
• Texnologiya: React.js, Node.js, MongoDB
• *100% mijozlar mamnuniyat darajasi*

**4. 🎮 Interaktiv veb-o'yinlar**
• Real vaqt funksiyalari bilan brauzer asosidagi o'yinlar
• Ko'p foydalanuvchili funksiyalar
• Progressive Web App imkoniyatlari
• Texnologiya: JavaScript, WebSockets, Canvas API

**5. 📱 Mobile-First veb-ilovalar**
• Mahalliy his qiladigan moslashuvchan ilovalar
• Service workers bilan oflayn funksiyalar
• Push bildirishnomalar integratsiyasi
• Texnologiya: Vue.js, PWA texnologiyalari

**🔥 Siz uchun nima qura olaman:**
• E-commerce platformalar
• Ijtimoiy tarmoq ilovalari
• Ta'lim platformalari
• O'yin veb-saytlari
• Biznes avtomatlashtirish vositalari
• Va siz tasavvur qila oladigan har qanday narsa!

**Falsafa:** "Har bir loyiha - ajoyib narsa yaratish va yangi narsalarni o'rganish imkoniyati!" ✨

Jonli demo ko'rishni xohlaysizmi? Men bilan bog'laning! 📧"""
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

*"Отличные идеи заслуживают отличного исполнения. Давайте воплотим это в жизнь!"* ✨""",
        'uz': """📧 **Keling bog'lanaliq va ajoyib narsa yarataylik!**

**To'g'ridan-to'g'ri aloqa:**
📩 **Email:** orbitskill@gmail.com
💬 **Telegram:** @oxygw
🐙 **GitHub:** github.com/jadev-a11y

**💼 Quyidagilar uchun mavjudman:**
✅ Maxsus veb-sayt ishlab chiqish
✅ Telegram bot yaratish
✅ Full-Stack veb-ilovalar
✅ UI/UX dizayn va maslahat
✅ Kod ko'rib chiqish va mentorlik
✅ Texnik muhokamalar va aqliy hujum

**🕒 Javob berish vaqti:**
• Odatda 2-4 soat ichida
• Shoshilinch loyihalar: 30 daqiqa ichida
• Vaqt zonasi: UTC+5 (Markaziy Osiyo)

**💰 Hamkorlik:**
• Talabalar uchun qulay narxlar
• Portfolio loyihalari (ba'zan qiziqarli g'oyalar uchun bepul!)
• Uzoq muddatli hamkorlik mavjud
• Har doim innovatsion qiyinchiliklarga tayyor

**🎯 Men uchun mukammal loyihalar:**
• MVP ishlab chiqishga muhtoj startaplar
• Veb-ishlab chiqishni o'rganayotgan talabalar
• Raqamli texnologiyaga o'tayotgan kichik biznes
• Noyob talablarga ega ijodiy loyihalar

**📞 Men bilan qanday bog'lanish:**
1. **Tezkor savollar:** Telegram (eng tez javob)
2. **Biznes so'rovlari:** Email (batafsil takliflar)
3. **Kod hamkorligi:** GitHub (birga quraylik!)

**Qiziqarli qiyinchilik:** Menga eng aqldan ozgan loyiha g'oyangizni yozing - ishonchim komilki, uni qanday amalga oshirishni tushunib olaman! 🚀

*"Ajoyib g'oyalar ajoyib bajarilishni loyiq ko'radi. Keling, buni amalga oshiraylik!"* ✨"""
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

**🇺🇿 O'zbek** - Native
• Deep cultural understanding
• Local market insights
• Regional business knowledge
• *Bridge between Central Asian cultures*

**💡 Communication Superpowers:**
✨ Can explain technical concepts in any of these languages
🌐 Perfect for international teams
🤝 Cultural sensitivity in global projects
📚 Translate technical documentation
🎯 Adapt communication style to audience

**🚀 What This Means for Your Project:**
• No language barriers in development
• Better understanding of diverse user needs
• Culturally appropriate solutions
• Effective team communication

**Fun Fact:** I dream in code, but I debug in three languages! 😄

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

**🇺🇿 O'zbek** - Родной
• Глубокое понимание культуры
• Понимание местного рынка
• Региональные бизнес-знания
• *Мост между центральноазиатскими культурами*

**💡 Суперспособности общения:**
✨ Могу объяснить технические концепции на любом из этих языков
🌐 Идеально для международных команд
🤝 Культурная чувствительность в глобальных проектах
📚 Перевожу техническую документацию
🎯 Адаптирую стиль общения к аудитории

**🚀 Что это означает для вашего проекта:**
• Никаких языковых барьеров в разработке
• Лучшее понимание потребностей разных пользователей
• Культурно подходящие решения
• Эффективное командное общение

**Интересный факт:** Я мечтаю в коде, но отлаживаю на трех языках! 😄

**Бонус:** Я также изучаю:
🇰🇷 Корейский (влияние K-pop! 🎵)
🇯🇵 Японский (Аниме и технологическая культура)""",
        'uz': """🌍 **Ko'p tilli muloqot**

**🗣️ Men gapira oladigan tillar:**

**🇺🇸 English** - Erkin
• Professional muloqot
• Texnik hujjatlar
• Xalqaro loyiha hamkorligi
• *Murakkab tushunchalarni oddiy tarzda tushuntira olaman*

**🇷🇺 Русский** - Ona tili
• Texnik atamalar bilan qulay
• Biznes muloqoti
• Madaniy nozikliklarni tushunish
• *MDH bozori loyihalari uchun mukammal*

**🇺🇿 O'zbek** - Ona tili
• Madaniyatni chuqur tushunish
• Mahalliy bozor tushunchalari
• Mintaqaviy biznes bilimlari
• *Markaziy Osiyo madaniyatlari o'rtasidagi ko'prik*

**💡 Muloqot super kuchlari:**
✨ Ushbu tillarning har qandayida texnik tushunchalarni tushuntira olaman
🌐 Xalqaro jamoalar uchun mukammal
🤝 Global loyihalarda madaniy sezgirlik
📚 Texnik hujjatlarni tarjima qilaman
🎯 Muloqot uslubini auditoriyaga moslashtiraman

**🚀 Bu sizning loyihangiz uchun nimani anglatadi:**
• Ishlab chiqishda til to'siqlari yo'q
• Turli foydalanuvchilar ehtiyojlarini yaxshiroq tushunish
• Madaniy jihatdan mos yechimlar
• Samarali jamoa muloqoti

**Qiziq fakt:** Men kod bilan tush ko'raman, lekin uch tilda debug qilaman! 😄

**Bonus:** Men shuningdek o'rganyapman:
🇰🇷 Koreys tili (K-pop ta'siri! 🎵)
🇯🇵 Yapon tili (Anime va texnologiya madaniyati)"""
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
"Life is too short to be bored. There's always something fascinating to discover, create, or improve!\"""",

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
• Обучение других тому, что знаю

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
"Жизнь слишком коротка, чтобы скучать. Всегда есть что-то увлекательное для открытия, создания или улучшения!"\"""",

        'uz': """🎯 **Mening qiziqishlar olami**

**🔧 Texnologiya va innovatsiya:**
• Eng so'nggi gadjetlar va texnologik trendlar
• AI va mashinali o'rganish ishlanmalari
• Blokcheyn va kriptovalyuta
• IoT va aqlli uy avtomatizatsiyasi
• Kosmik texnologiya va tadqiqotlar

**🎮 Raqamli madaniyat:**
• Video o'yin ishlab chiqish va dizayn
• Streaming texnologiyalari
• Raqamli san'at va NFT
• Virtual va qo'shimcha haqiqat
• Kiberxavfsizlik va axloqiy hacking

**🌟 Ijodiy mashg'ulotlar:**
• UI/UX dizayn tendentsiyalari
• Raqamli fotografiya
• Video montaj va harakat grafikalari
• Musiqa ishlab chiqarish (elektron bitlar!)
• 3D modellashtirish va animatsiya

**🧠 O'rganish va o'sish:**
• Onlayn kurslar va sertifikatlar
• Texnik podkastlar va YouTube kanallari
• Open source hissalar
• Xakatonlar va dasturlash musobaqalari
• Boshqalarga bilganimni o'rgatish

**🌍 Global nuqtai nazar:**
• Turli madaniyatlar va an'analar
• Xalqaro biznes amaliyotlari
• Til o'rganish usullari
• Sayohat va geografiya
• Global iqtisodiy tendentsiyalar

**⚡ Men haqimda tasodifiy faktlar:**
• Deyarli har qanday texnik muammoni yecha olaman (do'stlar meni "Texnik yordam" deb atashadi)
• Kvant fizikasidan tortib pitsa afzalliklarigacha hamma narsani muhokama qilishni yaxshi ko'raman
• Har doim yangi qiyinchiliklar va o'rganish imkoniyatlaridan hayajonlanaman
• Ishtiyoq bor joyda yoshning shunchaki raqam ekanligiga ishonaman
• Har qanday zerikarli mavzuni qiziqarli suhbatga aylantira olaman

**🚀 Mening falsafam:**
"Hayot zerikish uchun juda qisqa. Har doim kashf qilish, yaratish yoki yaxshilash uchun qiziqarli narsa bor!"\"""",

    },
    
    'message_reply': {
        'en': """Thanks for the message! 😊

I'm a 15-year-old developer from Central Asia who loves creating amazing digital experiences!

Use /start to see the main menu with all my information, or just keep chatting - I love talking about tech, projects, or literally anything! 🚀

What would you like to know about me?""",
        'ru': """Спасибо за сообщение! 😊

Я 15-летний разработчик из Центральной Азии, который любит создавать удивительные цифровые решения!

Используйте /start чтобы увидеть главное меню со всей информацией обо мне, или просто продолжайте общаться - я люблю говорить о технологиях, проектах или буквально о чём угодно! 🚀

Что вы хотели бы узнать обо мне?""",
        'uz': """Xabar uchun rahmat! 😊

Men Markaziy Osiyodan 15 yoshli dasturchiman va ajoyib raqamli tajribalar yaratishni yaxshi ko'raman!

Barcha ma'lumotlarim bilan asosiy menyuni ko'rish uchun /start dan foydalaning yoki shunchaki suhbatni davom ettiring - men texnologiya, loyihalar yoki deyarli har qanday narsa haqida gaplashishni yaxshi ko'raman! 🚀

Men haqimda nimani bilishni xohlaysiz?"""
    },
    
    'back_to_menu': {
        'en': '🔙 Back to Menu',
        'ru': '🔙 Назад в меню',
        'uz': '🔙 Menyuga qaytish'
    },
    
    'change_lang': {
        'en': '🌐 Change Language',
        'ru': '🌐 Изменить язык', 
        'uz': '🌐 Tilni o\'zgartirish'
    }
}

# Кнопки меню
menu_buttons = {
    'about': {
        'en': '👤 About Me',
        'ru': '👤 Обо мне',
        'uz': '👤 Men haqimda'
    },
    'skills': {
        'en': '💻 Skills',
        'ru': '💻 Навыки',
        'uz': '💻 Ko\'nikmalar'
    },
    'projects': {
        'en': '🚀 Projects',
        'ru': '🚀 Проекты',
        'uz': '🚀 Loyihalar'
    },
    'contact': {
        'en': '📧 Contact',
        'ru': '📧 Контакты',
        'uz': '📧 Aloqa'
    },
    'languages': {
        'en': '🌍 Languages',
        'ru': '🌍 Языки',
        'uz': '🌍 Tillar'
    },
    'interests': {
        'en': '🎯 Interests',
        'ru': '🎯 Интересы',
        'uz': '🎯 Qiziqishlar'
    }
}

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
                <p>🌐 Languages: English, Русский, O'zbek</p>
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
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
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

# Исправленный обработчик callback'ов
# Замените эту часть в вашем коде:

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
    
    # ИСПРАВЛЕННАЯ ЧАСТЬ - обработка основных разделов
    elif call.data == "about":
        text = t('about_me', user_id)  # Изменено с 'about' на 'about_me'
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
    
    # Подтверждение обработки callback
    bot.answer_callback_query(call.id)
    # Подтверждение обработки callback
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех остальных сообщений"""
    user_id = message.from_user.id
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
        logger.info("🌐 Supported languages: English, Русский, O'zbek")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error: {e}")
