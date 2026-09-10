from pathlib import Path

p = Path('index.html')
s = p.read_text()

old = '''  localStorage.setItem("wildwatchSave",JSON.stringify(rec.save));
  location.reload();
}'''
new = '''  sessionStorage.setItem("critterAutoContinueFromSlot","1");
  localStorage.setItem("wildwatchSave",JSON.stringify(rec.save));
  location.reload();
}'''

if old not in s:
    raise SystemExit('loadFromSlot reload marker not found')
s = s.replace(old, new, 1)

marker = '</script>'
route = '''// When a player chooses an existing save slot, continue straight into their game
// instead of making them land on Home and press Continue Battle again.
setTimeout(()=>{
  if(sessionStorage.getItem("critterAutoContinueFromSlot")!=="1") return;
  sessionStorage.removeItem("critterAutoContinueFromSlot");
  const continueButton=document.getElementById("continueBtn");
  if(continueButton){
    continueButton.click();
  }else{
    showScreen("battleScreen");
  }
},350);
'''

if 'critterAutoContinueFromSlot' not in s.split(marker)[0] or s.count('critterAutoContinueFromSlot') < 2:
    if marker not in s:
        raise SystemExit('script closing tag not found')
    s = s.replace(marker, route + marker, 1)

p.write_text(s)
