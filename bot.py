import os
import telegram
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found!")
    exit(1)

def start(update, context):
    """Команда /start"""
    user = update.effective_user
    
    message = f"""
🌟 **Welcome {user.first_name}!** 🌟

👋 Hi! I'm a **15-year-old tech enthusiast** from Central Asia passionate about creating digital experiences!

🚀 **What I do:**
• Full-stack web development (Frontend + Backend)
• Custom websites for any taste
• Telegram bots that actually work
• Anything tech-related!

**Available commands:**
/about - Learn more about me
/skills - My technical skills
/projects - Check out my work
/contact - Get in touch
/languages - Languages I speak
/interests - My hobbies

💬 **Fun fact:** I can talk about literally anything - try me! 😄

Type any command or just chat with me! 🚀
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def about(update, context):
    """Команда /about"""
    message = """
👨‍💻 **About Me - The Full Story**

🎂 **Age:** 15 years old (started early!)
🌍 **Location:** Central Asia 
🎯 **Mission:** Building the digital future, one project at a time

**My Journey:**
🚀 Started coding out of curiosity about how websites work
💡 Love both frontend beauty AND backend logic
🌟 Create full-stack solutions people actually enjoy using

**What makes me unique:**
✨ Passionate about EVERYTHING - tech, culture, science
🗣️ Master conversationalist - can discuss anything with enthusiasm  
🔧 Natural problem solver - can improve almost anything
🌈 Central Asian perspective brings fresh ideas

**Philosophy:**
"Age is just a number when you have passion and dedication. My code speaks louder than my birth certificate!" 💪

Ready to see what I can do? Use /skills and /projects! 🚀
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def skills(update, context):
    """Команда /skills"""
    message = """
💻 **My Technical Arsenal**

**Frontend Development:**
🎨 HTML5, CSS3, JavaScript (ES6+)
⚡ React.js, Vue.js
🎯 Responsive Design & Mobile-First
✨ CSS Animations & Interactions

**Backend Development:**
🐍 Python (Django, Flask)
🟢 Node.js, Express.js
🗄️ Database Design (SQL, NoSQL)
🔐 API Development & Security

**Bot Development:**
🤖 Telegram Bot API Expert
⚙️ Complex Logic & Automation
💬 Natural Conversation Flow

**Tools & Technologies:**
🛠️ Git, GitHub, VS Code
🚀 Docker, Linux
📱 Figma, Design Tools
🌐 Netlify, Heroku, Railway

**Soft Skills:**
🗣️ Excellent Communication (3 languages!)
🧠 Quick Learner & Problem Solver
🤝 Team Collaboration
💡 Creative Thinking

**Currently Learning:**
📚 Advanced React Patterns
🔮 Machine Learning Basics
🎮 Game Development

**Fun Fact:** I learn new technologies faster than most people learn new games! 🎯
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def projects(update, context):
    """Команда /projects"""
    message = """
🚀 **My Project Showcase**

**🌟 Featured Projects:**

**1. 🌌 Cosmic Portfolio Website**
• Space-themed personal website
• Custom CSS animations & particle effects
• Fully responsive design
• Tech: HTML5, CSS3, JavaScript

**2. 🤖 AI-Powered Telegram Bots**
• Advanced conversation logic
• User analytics & data processing
• Tech: Python, PostgreSQL, Docker
• *Used by 1000+ active users*

**3. 💼 Business Landing Pages**
• Custom websites for local businesses
• SEO optimization & performance tuning
• Tech: React.js, Node.js, MongoDB
• *100% client satisfaction rate*

**4. 🎮 Interactive Web Games**
• Browser-based games with real-time features
• Multiplayer functionality
• Tech: JavaScript, WebSockets, Canvas API

**5. 📱 Mobile-First Web Apps**
• Responsive applications that feel native
• Offline functionality with service workers
• Tech: Vue.js, PWA technologies

**🔥 What I Can Build:**
• E-commerce platforms
• Social media applications
• Educational platforms
• Gaming websites
• Business automation tools
• Literally anything you can imagine!

**Philosophy:** "Every project is a chance to create something amazing!" ✨

Want to see live demos? Use /contact! 📧
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def contact(update, context):
    """Команда /contact"""
    message = """
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
• Portfolio projects (sometimes free for cool ideas!)
• Long-term partnerships available
• Always up for innovative challenges

**🎯 Perfect Projects for Me:**
• Startups needing MVP development
• Students learning web development
• Small businesses going digital
• Creative projects with unique requirements

**📞 How to Reach Me:**
1. **Quick Questions:** Telegram (fastest)
2. **Business Inquiries:** Email (detailed proposals)
3. **Code Collaboration:** GitHub (let's build together!)

**Fun Challenge:** Message me your wildest project idea - I bet I can make it happen! 🚀

*"Great ideas deserve great execution. Let's make it happen!"* ✨
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def languages(update, context):
    """Команда /languages"""
    message = """
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
✨ Explain technical concepts in any language
🌐 Perfect for international teams
🤝 Cultural sensitivity in global projects
📚 Translate technical documentation
🎯 Adapt communication style to audience

**🚀 What This Means for Projects:**
• No language barriers in development
• Better understanding of diverse user needs
• Culturally appropriate solutions
• Effective team communication

**Fun Fact:** I dream in code, but debug in three languages! 😄

**Bonus Learning:**
🇰🇷 Korean (K-pop influence! 🎵)
🇯🇵 Japanese (Anime and tech culture)
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def interests(update, context):
    """Команда /interests"""
    message = """
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
• Friends call me "Tech Support" - I fix everything!
• Love discussing quantum physics to pizza preferences
• Always excited about new challenges
• Believe age is just a number with passion
• Can make any topic interesting

**🚀 Philosophy:**
"Life's too short to be bored. There's always something fascinating to discover, create, or improve!"

**Challenge:** Try to name a topic I can't discuss - I dare you! 😄
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def help_command(update, context):
    """Команда /help"""
    message = """
❓ **Bot Commands & Features**

**Available Commands:**
• `/start` - Welcome message & introduction
• `/about` - My full story and background
• `/skills` - Technical abilities and tools
• `/projects` - Portfolio and achievements
• `/contact` - How to reach me
• `/languages` - Multilingual capabilities
• `/interests` - My hobbies and passions
• `/help` - This help message

**💡 Pro Tips:**
• Each command gives detailed information
• You can also just chat with me normally!
• Contact me directly for specific questions
• I respond to all messages personally

**🤖 Bot Features:**
✅ Always up-to-date information
✅ Mobile-friendly interface
✅ Personal touch in every response
✅ Works 24/7

**Questions? Just ask!** 
I love talking to people and discussing new ideas! 🚀

Type any command or just start chatting! 💬
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def echo(update, context):
    """Отвечает на любые сообщения"""
    message = f"""
Thanks for the message! 😊

I'm a 15-year-old developer from Central Asia who loves creating amazing digital experiences!

**Try these commands to learn more:**
• /about - My story
• /skills - What I can do
• /projects - My work
• /contact - Get in touch

Or just keep chatting - I love talking about tech, projects, or literally anything! 🚀

What would you like to know about me?
    """
    
    update.message.reply_text(message, parse_mode='Markdown')

def main():
    """Запуск бота"""
    try:
        # Создаем updater
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        # Добавляем обработчики команд
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("about", about))
        dp.add_handler(CommandHandler("skills", skills))
        dp.add_handler(CommandHandler("projects", projects))
        dp.add_handler(CommandHandler("contact", contact))
        dp.add_handler(CommandHandler("languages", languages))
        dp.add_handler(CommandHandler("interests", interests))
        dp.add_handler(CommandHandler("help", help_command))
        
        # Обработчик всех остальных сообщений
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        
        # Запускаем бота
        logger.info("🤖 Bot is starting...")
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == '__main__':
    main()
