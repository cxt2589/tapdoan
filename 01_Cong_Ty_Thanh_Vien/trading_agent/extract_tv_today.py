import re

with open(r'C:\Users\truon\.gemini\antigravity\brain\af65fd48-4737-4331-a907-9277b0c0da0b\.system_generated\steps\558\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'offers":\s*\{[^}]+\}', text):
    print("Offers:", m.group(0))

for m in re.finditer(r'What&#x27;s the gold price today.*?</div', text, re.DOTALL):
    print("FAQ:", m.group(0)[:300])

for m in re.finditer(r'"price":\s*"([0-9.]+)"', text):
    print("Price:", m.group(1))
