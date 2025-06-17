import os
import telebot
from telebot import types
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found!")
    exit(1)

# Создаем бота
bot = telebot.TeleBot(BOT_TOKEN)

def create_main_menu():
    """Создает главное меню с кнопками"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn1 = types.InlineKeyboardButton("👤 About Me", callback_data="about")
    btn2 = types.InlineKeyboardButton("💻 Skills", callback_data="skills")
    btn3 = types.InlineKeyboardButton("🚀 Projects", callback_data="projects")
    btn4 = types.InlineKeyboardButton("📧 Contact", callback_data="contact")
    btn5 = types.InlineKeyboardButton("🌍 Languages", callback_data="languages")
    btn6 = types.InlineKeyboardButton("🎯 Interests", callback_data="interests")
    
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    
    return markup

def create_back_menu():
    """Создает кнопку Назад"""
    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")
    markup.add(back_btn)
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    """Команда /start"""
    user_name = message.from_user.first_name or "Friend"
    
    text = f"""
🌟 **Welcome {user_name} to my personal universe!** 🌟

👋 Hi there! I'm a **15-year-old tech enthusiast** from Central Asia who's passionate about creating digital experiences that matter.

🚀 **What I do:**
• Full-stack web development (Frontend + Backend)
• Custom websites tailored to any taste
• Telegram bots that actually work
• And pretty much anything tech-related!

💬 **Fun fact:** I can start a conversation about literally anything and keep it going - try me! 😄

**Choose what you'd like to know about me:**
    """
    
    markup = create_main_menu()
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    """Команда /help"""
    text = """
❓ **How to Navigate This Bot**

**Available Commands:**
• `/start` - Main menu and welcome
• `/help` - This help message

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

**🤖 Bot Features:**
✅ Always up-to-date information
✅ Mobile-friendly interface
✅ Quick navigation
✅ Personal touch in every response

**Questions? Just ask!** 
I love talking to people and discussing new ideas! 🚀
    """
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик нажатий на кнопки"""
    
    if call.data == "menu":
        text = """
🌟 **Welcome back to my personal universe!** 🌟

👋 I'm a **15-year-old tech enthusiast** from Central Asia who's passionate about creating digital experiences that matter.

**Choose what you'd like to know about me:**
        """
        markup = create_main_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "about":
        text = """
👨‍💻 **About Me - The Full Story**

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

Ready to see what I can do? Check out my skills and projects! 🚀
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "skills":
        text = """
💻 **My Technical Arsenal**

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

**Fun Fact:** I learn new technologies faster than most people learn new games! 🎯
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "projects":
        text = """
🚀 **My Project Showcase**

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

Want to see live demos? Contact me! 📧
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "contact":
        text = """
📧 **Let's Connect & Build Something Amazing!**

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

*"Great ideas deserve great execution. Let's make it happen!"* ✨
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "languages":
        text = """
🌍 **Multilingual Communication**

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
🇯🇵 Japanese (Anime and tech culture)
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "interests":
        text = """
🎯 **My Universe of Interests**

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
"Life is too short to be bored. There's always something fascinating to discover, create, or improve!"

**Challenge:** Try to name a topic I can't discuss - I dare you! 😄
        """
        markup = create_back_menu()
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, 
                             reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех остальных сообщений"""
    text = f"""
Thanks for the message! 😊

I'm a 15-year-old developer from Central Asia who loves creating amazing digital experiences!

Use /start to see the main menu with all my information, or just keep chatting - I love talking about tech, projects, or literally anything! 🚀

What would you like to know about me?
    """
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

if __name__ == "__main__":
    try:
        logger.info("🤖 Bot is starting...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error: {e}")
