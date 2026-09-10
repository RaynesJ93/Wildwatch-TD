from pathlib import Path
p=Path('index.html'); s=p.read_text()
repls={
'Earn Coins by completing waves. Spend those permanent Coins on chests to hunt for rare animal cards. Battle currency is separate and is only used for towers.':'Earn Coins by completing waves. Spend those permanent Coins on card packs to collect animal cards. Every pack contains 1 card from its matching rarity. Battle currency is separate and is only used for towers.',
'🪵 Common Chest • 🟡 250 Coins':'⚪ Common Pack • 🟡 250 Coins',
'🟩 Uncommon Chest • 🟡 500 Coins':'🟢 Uncommon Pack • 🟡 500 Coins',
'💜 Rare Chest • 🟡 750 Coins':'🔵 Rare Pack • 🟡 750 Coins',
'🌟 Legendary Chest • 🟡 1500 Coins':'🟡 Legendary Pack • 🟡 1500 Coins',
'name:"Common Chest"':'name:"Common Pack"',
'name:"Uncommon Chest"':'name:"Uncommon Pack"',
'name:"Rare Chest"':'name:"Rare Pack"',
'name:"Legendary Chest"':'name:"Legendary Pack"',
'for this chest.':'for this pack.',
'in this chest yet.':'in this pack yet.'
}
for old,new in repls.items():
    if old in s:s=s.replace(old,new)
# Add foil-pack styling while preserving existing click handlers/data attributes and costs.
marker='</style>'
css=r'''
/* Card pack shop */
#chestScreen .chestBtn{min-height:92px;border-radius:14px;border:2px solid rgba(255,255,255,.32);font-size:18px;font-weight:900;letter-spacing:.25px;box-shadow:inset 0 0 18px rgba(255,255,255,.18),0 6px 14px rgba(0,0,0,.24);position:relative;overflow:hidden;text-shadow:0 1px 2px rgba(0,0,0,.55)}
#chestScreen .chestBtn:before,#chestScreen .chestBtn:after{content:"";position:absolute;left:0;right:0;height:8px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.5) 0 5px,rgba(0,0,0,.12) 5px 9px)}
#chestScreen .chestBtn:before{top:0}#chestScreen .chestBtn:after{bottom:0}
#chestScreen .chestBtn[data-chest="common"]{background:linear-gradient(135deg,#fff,#d7d7d7 55%,#fff);color:#242424;text-shadow:none}
#chestScreen .chestBtn[data-chest="uncommon"]{background:linear-gradient(135deg,#28b94c,#08752b 55%,#42df68);color:#fff}
#chestScreen .chestBtn[data-chest="epic"]{background:linear-gradient(135deg,#2d8fff,#064ba5 55%,#42a7ff);color:#fff}
#chestScreen .chestBtn[data-chest="legendary"]{background:linear-gradient(135deg,#ffd84d,#a86d00 55%,#ffe881);color:#241500;border-color:#ffe78a;text-shadow:none}
'''
if marker not in s: raise SystemExit('style marker not found')
s=s.replace(marker,css+'\n'+marker,1)
p.write_text(s)
