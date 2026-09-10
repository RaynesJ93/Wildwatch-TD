from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker='</style>'
override='''\n/* Keep all card-pack writing the same red colour */\n#packsScreen .chestBtn{color:#e53935!important;text-shadow:none!important}\n'''
if '#packsScreen .chestBtn{color:#e53935!important;text-shadow:none!important}' not in s:
    if marker not in s: raise SystemExit('style marker not found')
    s=s.replace(marker,override+'\n'+marker,1)
p.write_text(s)
