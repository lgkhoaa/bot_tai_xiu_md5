import telebot
import time
import re
import hashlib
import random
import math
from datetime import datetime

TOKEN = '8004410977:AAHTaUVXEI8xg9AVfEtHjqq22Q1gMlWQYXc'
bot = telebot.TeleBot(TOKEN)

history_data = []

def dynamic_seed(md5):
    now = datetime.utcnow()
    seed_value = int(now.strftime("%Y%m%d%H%M%S")) + sum(ord(c) for c in md5[:8])
    random.seed(seed_value)
    return random.random()

def calculate_entropy(md5):
    prob = [md5.count(c)/len(md5) for c in set(md5)]
    entropy = -sum(p * math.log2(p) for p in prob)
    return entropy

def enhanced_basic_rule(md5):
    last5 = md5[-5:]
    digits = sum(1 for c in last5 if c.isdigit())
    entropy = calculate_entropy(md5)
    if entropy > 3.5 and digits >= 3:
        return 'XỈU'
    elif entropy <= 3.5 and digits < 3:
        return 'TÀI'
    return 'TÀI' if digits < 3 else 'XỈU'

def enhanced_parity_rule(md5):
    last_char = md5[-1]
    seed = dynamic_seed(md5)
    if last_char.isdigit():
        val = int(last_char) + int(seed * 10) % 10
        return 'XỈU' if val % 2 == 0 else 'TÀI'
    else:
        return 'TÀI' if seed > 0.5 else 'XỈU'

def enhanced_checksum_rule(md5):
    total = sum(int(c) if c.isdigit() else ord(c) for c in md5)
    adjust = int(dynamic_seed(md5) * 100) % 10
    result = total + adjust
    return 'XỈU' if result % 2 == 0 else 'TÀI'

def enhanced_md5_hash_rule(md5):
    segment = md5[-8:]
    hashed = hashlib.md5(segment.encode()).hexdigest()
    digit_sum = sum(int(c, 16) for c in hashed if c.isalnum())
    return 'TÀI' if digit_sum % 3 == 0 else 'XỈU'

def analyze_md5(md5):
    b = enhanced_basic_rule(md5)
    p = enhanced_parity_rule(md5)
    c = enhanced_checksum_rule(md5)
    h = enhanced_md5_hash_rule(md5)

    result_count = {'TÀI': 0, 'XỈU': 0}
    for r in [b, p, c, h]:
        result_count[r] += 1

    final_result = 'TÀI' if result_count['TÀI'] >= 3 else 'XỈU'

    history_data.append((md5, final_result))

    return f"""[PHÂN TÍCH MD5]
Entropy: {round(calculate_entropy(md5), 3)}
Seed: {round(dynamic_seed(md5), 5)}

- Thuật toán Basic + Entropy: {b}
- Thuật toán Parity + Seed: {p}
- Thuật toán Checksum + Seed: {c}
- Thuật toán MD5 Hash Cải Tiến: {h}

=> KẾT LUẬN: {final_result}
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào, tôi là BOT TÀI XỈU MD5 - ADMIN : LG Khoaa.\nGỬI MÃ MD5 ĐỂ PHÂN TÍCH!")

@bot.message_handler(func=lambda m: True)
def handle_md5(message):
    md5 = message.text.strip().lower()
    if re.fullmatch(r'[a-f0-9]{32}', md5):
        bot.reply_to(message, "⏳ Đang phân tích mã MD5, vui lòng chờ...")
        time.sleep(random.randint(3, 5))
        result = analyze_md5(md5)
        bot.send_message(message.chat.id, f"{result}\n📩 Gửi Mã MD5 Tiếp Theo📩")
    else:
        bot.reply_to(message, "⚠️ Mã MD5 không hợp lệ. Vui lòng gửi đúng 32 ký tự hex.")

bot.polling()
