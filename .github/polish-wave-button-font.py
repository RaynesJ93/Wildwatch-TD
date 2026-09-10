from pathlib import Path
p=Path('index.html')
s=p.read_text()
# Give the game a rounder, more playful game-style font without external dependencies.
s=s.replace('font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif','font-family:"Trebuchet MS","Arial Rounded MT Bold",system-ui,-apple-system,sans-serif',1)
# Make the wave control stable in size so starting a wave cannot reflow the HUD.
css='''\n    #startWave{flex:0 0 150px;min-width:150px;height:58px;padding:8px 10px;white-space:nowrap;font-family:"Trebuchet MS","Arial Rounded MT Bold",system-ui,sans-serif;font-size:16px;line-height:1;font-weight:900;text-align:center;letter-spacing:.2px}\n    @media(max-width:430px){#startWave{flex-basis:142px;min-width:142px;font-size:15px}}\n'''
s=s.replace('</style>',css+'  </style>',1)
s=s.replace('startWave.textContent="Wave running…";','startWave.textContent="Wave Active";',1)
p.write_text(s)
