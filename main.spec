# -*- mode: python -*-
a = Analysis(['main.py'],
             pathex=['C:\\Users\\Lucas\\Documents\\GitHub\\LolNormalStats'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
