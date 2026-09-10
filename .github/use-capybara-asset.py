from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Replace the old CSS-drawn Capybara with the dedicated asset everywhere animalVisual() is used.
pattern=r'''  if\(k==="capybara"\)\{\n    const size=cls==="reward-portrait"\?68:cls==="animal-portrait"\?48:30;\n    return `.*?`;\n  \}\n'''
replacement='''  if(k==="capybara"){
    const size=cls==="reward-portrait"?68:cls==="animal-portrait"?48:30;
    return `<img src="assets/capybara.svg" alt="Capybara" class="animal-emoji ${cls}" style="width:${size}px;height:${size}px;object-fit:cover;border-radius:16px;display:block">`;
  }
'''
ns,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    if 'assets/capybara.svg' not in s:
        raise SystemExit('Could not locate Capybara visual block')

# Remove the Beaver emoji fallback from the Capybara definition and update old Chest wording.
s=s.replace('capybara:{name:"Capybara", emoji:"🦫"','capybara:{name:"Capybara", emoji:""')
s=s.replace('Exclusive to the Uncommon Chest.','Exclusive to the Uncommon Pack.')
s=s.replace('Exclusive to the Uncommon Chest','Exclusive to the Uncommon Pack')

p.write_text(s,encoding='utf-8')
print('Capybara asset is now used throughout the game')
