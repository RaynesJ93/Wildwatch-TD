from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<div class="small" style="margin-top:4px">Each card level gives +6% base damage and +3.5% attack range. Cards can reach Level 50.</div>'
if old not in s:
    raise SystemExit('card level explanatory text not found')
s=s.replace(old,'',1)
if 'Each card level gives +6% base damage and +3.5% attack range. Cards can reach Level 50.' in s:
    raise SystemExit('card level explanatory text still present')
p.write_text(s,encoding='utf-8')
print('Removed repeated card-level explanatory text from collection cards')
