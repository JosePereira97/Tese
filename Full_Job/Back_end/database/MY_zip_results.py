from zipfile import ZipFile
import os
file_path = os.path.abspath(os.path.dirname(__file__)) #falar com o joao preciso de info
def Get_my_Files(workflow): #build ZIP
    #ZipObj = ZipFile(f'{file_path}/Input_MOSCA.zip', 'w') //fazer o ZIP de resultados esta em falta
    if 'preprocess' in workflow:
        pass
    pass