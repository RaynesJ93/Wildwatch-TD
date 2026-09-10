from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = 'Earn Coins by completing waves. Spend those permanent Coins on card packs to collect animal cards. Every pack contains 1 card from its matching rarity. Battle currency is separate and is only used for towers.'
new = old + ' <span style="display:inline-block;color:#38d96b;font-weight:800;white-space:nowrap">Scroll down for more packs ↓</span>'
if new in s:
    print('Scroll hint already present')
elif old in s:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')
    print('Added green scroll-down hint')
else:
    raise SystemExit('Pack description text not found')
