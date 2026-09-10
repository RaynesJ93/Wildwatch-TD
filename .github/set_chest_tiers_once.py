from pathlib import Path
p=Path('index.html')
s=p.read_text()
old='''const chestConfig={
  common:{name:"Common Chest",cost:250,rarities:{Common:.65,Rare:.27,Epic:.07,Legendary:.01}},
  uncommon:{name:"Uncommon Chest",cost:500,rarities:{Common:.30,Rare:.48,Epic:.19,Legendary:.03}},
  epic:{name:"Rare Chest",cost:750,rarities:{Common:.08,Rare:.32,Epic:.50,Legendary:.10},exclusive:["rhino","lion"]},
  legendary:{name:"Legendary Chest",cost:1500,rarities:{Common:.02,Uncommon:.08,Rare:.20,Epic:.30,Legendary:.40},legendary:true}
};'''
new='''const chestConfig={
  common:{name:"Common Chest",cost:250,rarities:{Common:1}},
  uncommon:{name:"Uncommon Chest",cost:500,rarities:{Uncommon:1}},
  epic:{name:"Rare Chest",cost:750,rarities:{Rare:1}},
  legendary:{name:"Legendary Chest",cost:1500,rarities:{Legendary:1},legendary:true}
};'''
if old not in s: raise SystemExit('chest config anchor missing')
s=s.replace(old,new,1)
old='''  const exclusiveRare=["rhino","lion"];
  const allowedPool=Object.keys(animals).filter(k=>{
    if(k==="elephant") return btn.dataset.chest==="epic";
    if(k==="whiteRhino" || k==="silverback") return btn.dataset.chest==="legendary";
    if(btn.dataset.chest==="legendary") return true;
    if(exclusiveRare.includes(k)) return btn.dataset.chest==="epic";
    if(k==="capybara") return btn.dataset.chest==="uncommon";
    return true;
  });'''
new='''  const chestTier={common:"Common",uncommon:"Uncommon",epic:"Rare",legendary:"Legendary"}[btn.dataset.chest];
  const allowedPool=Object.keys(animals).filter(k=>animals[k].rarity===chestTier);'''
if old not in s: raise SystemExit('allowed pool anchor missing')
s=s.replace(old,new,1)
p.write_text(s)
