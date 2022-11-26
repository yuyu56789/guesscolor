from PyInstaller.utils.hooks import copy_metadata
datas = copy_metadata('kiwisolver') + copy_metadata('configparser') + copy_metadata('streamlit')  



