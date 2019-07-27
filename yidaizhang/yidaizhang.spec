# -*- mode: python -*-

block_cipher = None


a = Analysis(['D:\\pachong\\yidaizhang\\yidaizhang.py'],
             pathex=['D:\\pachong\\yidaizhang'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='yidaizhang',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='D:\\pachong\\yidaizhang\\YICO.ico')
