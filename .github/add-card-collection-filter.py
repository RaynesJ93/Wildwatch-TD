from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Add filter UI above Cards grid.
old='''    <div class="section-title">Cards</div>\n    <div id="collectionCards" class="cards"></div>'''
new='''    <div class="section-title">Cards</div>\n    <div style="display:flex;align-items:center;gap:10px;margin:0 3px 10px;flex-wrap:wrap">\n      <label for="cardCollectionFilter" class="small" style="font-weight:900;color:var(--text)">Show:</label>\n      <select id="cardCollectionFilter" class="secondary" style="padding:9px 12px;border-radius:12px;min-width:165px;font-weight:900">\n        <option value="all">All Cards</option>\n        <option value="collected">Collected</option>\n        <option value="not-collected">Not Collected</option>\n      </select>\n    </div>\n    <div id="collectionCards" class="cards"></div>'''
if 'id="cardCollectionFilter"' not in s:
    if old not in s:
        raise SystemExit('Cards section marker not found')
    s=s.replace(old,new,1)

# Add filter logic to renderCollection.
old_loop='''  Object.entries(animals).sort((a,b)=>rarityOrder[a[1].rarity]-rarityOrder[b[1].rarity]).forEach(([k,a])=>{\n    const unlocked=save.unlocked.includes(k), d=document.createElement("div");'''
new_loop='''  const cardFilter=document.getElementById("cardCollectionFilter")?.value||"all";\n  Object.entries(animals).sort((a,b)=>rarityOrder[a[1].rarity]-rarityOrder[b[1].rarity]).forEach(([k,a])=>{\n    const unlocked=save.unlocked.includes(k);\n    if(cardFilter==="collected"&&!unlocked)return;\n    if(cardFilter==="not-collected"&&unlocked)return;\n    const d=document.createElement("div");'''
if 'const cardFilter=document.getElementById("cardCollectionFilter")' not in s:
    if old_loop not in s:
        raise SystemExit('renderCollection loop marker not found')
    s=s.replace(old_loop,new_loop,1)

# Hook dropdown change after renderCollection function exists.
hook='''function levelUpCard(k){return;}'''
insert='''const cardCollectionFilter=document.getElementById("cardCollectionFilter");\nif(cardCollectionFilter){\n  cardCollectionFilter.addEventListener("change",()=>renderCollection());\n}\n\nfunction levelUpCard(k){return;}'''
if 'cardCollectionFilter.addEventListener("change"' not in s:
    if hook not in s:
        raise SystemExit('levelUpCard marker not found')
    s=s.replace(hook,insert,1)

p.write_text(s,encoding='utf-8')
print('Added All / Collected / Not Collected card filter')
