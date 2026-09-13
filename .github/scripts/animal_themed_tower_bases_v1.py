from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Make the themed habitat base large and visible.
s=s.replace('const k=t.key,x=t.x,y=t.y+11;','const k=t.key,x=t.x,y=t.y+13;')
s=s.replace('ctx.globalAlpha=.45;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(0,5,22,9,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;',
'''ctx.globalAlpha=.48;ctx.fillStyle="#000";ctx.beginPath();ctx.ellipse(0,7,35,17,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;''')
s=s.replace('ctx.fillStyle="#493d31";ctx.strokeStyle="#1d1813";ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(0,0,20,8,0,0,Math.PI*2);ctx.fill();ctx.stroke();',
'''const water=["frog","goose","duck","otter","flamingo","swan","elephant"].includes(k);
  const ice=["penguin"].includes(k);
  const desert=["scorpion","lizard"].includes(k);
  const farm=["chicken","sheep","pig","turkey","goat","ram"].includes(k);
  const forest=["monkey","owl","snake","hedgehog","crow","raccoon","badger","skunk","sloth","koala","fox","panda","tiger","jaguar","silverback"].includes(k);
  ctx.fillStyle=ice?"#bdefff":water?"#5f9f9a":desert?"#c79a55":farm?"#7d9b55":forest?"#567447":"#78634b";
  ctx.strokeStyle=ice?"#e9fbff":water?"#b9ece5":desert?"#f0cf8b":farm?"#c9df91":forest?"#b2cf91":"#c4aa82";
  ctx.lineWidth=3;ctx.beginPath();ctx.ellipse(0,0,32,15,0,0,Math.PI*2);ctx.fill();ctx.stroke();''')
s=s.replace('ctx.font="16px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[0],-7,-1);ctx.font="12px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[1],10,1);',
'''ctx.font="22px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[0],-11,-2);ctx.font="17px Apple Color Emoji,Segoe UI Emoji,sans-serif";ctx.fillText(a[1],13,1);''')

# Remove the old generic grey stone plinth that was drawn AFTER the themed base and covered it.
old='''    ctx.beginPath();ctx.ellipse(t.x,t.y+13,29,16,0,0,Math.PI*2);ctx.fillStyle="#6a6455";ctx.fill();
    ctx.strokeStyle="#b5aa8d";ctx.lineWidth=2;ctx.stroke();
'''
if old not in s:
    raise RuntimeError('Old generic tower plinth not found; game layout changed')
s=s.replace(old,'')

p.write_text(s,encoding='utf-8')
print('Fixed themed tower bases: old covering plinth removed and habitat bases enlarged')
