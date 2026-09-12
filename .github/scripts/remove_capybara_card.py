from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
card='  capybara:{name:"Capybara", emoji:"", rarity:"Uncommon", uncommonOnly:true, cost:70, range:140, rate:.8, dmg:12, color:"#a8794f", desc:"Calm, dependable attacker. Exclusive to the Uncommon Pack."},\n'
if card not in s: raise SystemExit('capybara card definition not found')
s=s.replace(card,'',1)
visual='''  if(k==="capybara"){
    const size=cls==="reward-portrait"?68:cls==="animal-portrait"?48:30;
    return `<span class="animal-emoji ${cls}" style="display:inline-flex!important;align-items:center;justify-content:center;width:${size}px;height:${size}px;background:#a8794f!important;border-radius:46% 46% 42% 42%;position:relative;box-sizing:border-box;border:2px solid #6e4a30;font-size:${Math.round(size*.28)}px;line-height:1;color:#21150e">●&nbsp;●<span style="position:absolute;left:9%;top:3%;width:22%;height:22%;background:#8b6040;border-radius:50%;border:1px solid #5d3c28"></span><span style="position:absolute;right:9%;top:3%;width:22%;height:22%;background:#8b6040;border-radius:50%;border:1px solid #5d3c28"></span><span style="position:absolute;left:34%;bottom:19%;width:32%;height:23%;background:#6d4932;border-radius:55%;border:1px solid #4b3021"></span></span>`;
  }
'''
if visual not in s: raise SystemExit('capybara visual block not found')
s=s.replace(visual,'',1)
for old,new in [
('lion:0,capybara:0,whiteRhino:0','lion:0,whiteRhino:0'),
('lion:1,capybara:1,whiteRhino:1','lion:1,whiteRhino:1'),
('lion:0,capybara:0,whiteRhino:0','lion:0,whiteRhino:0')]:
    s=s.replace(old,new)
anchor='save.cardXP=save.cardXP||{};\n'
if anchor not in s: raise SystemExit('save cleanup anchor not found')
cleanup='''save.unlocked=(save.unlocked||[]).filter(k=>k!=="capybara");
save.deck=(save.deck||defaults.deck).map(k=>k==="capybara"?null:k).filter(Boolean);
delete save.shards.capybara;
delete save.cardLevels.capybara;
if(save.damageUpgrades)delete save.damageUpgrades.capybara;
'''
s=s.replace(anchor,anchor+cleanup,1)
p.write_text(s,encoding='utf-8')
print('Removed Capybara card and cleaned existing saves')
