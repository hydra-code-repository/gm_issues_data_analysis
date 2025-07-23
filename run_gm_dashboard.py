import streamlit.web.cli as stcli
import sys
import os

if __name__ == '__main__':
    # Obter o diretório onde está o executável
    if getattr(sys, 'frozen', False):
        # Se executando como executável PyInstaller
        application_path = sys._MEIPASS
    else:
        # Se executando como script Python
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Caminho para o arquivo principal
    main_script = os.path.join(application_path, 'gm_issues_dashboard.py')
    
    sys.argv = [
        "streamlit",
        "run",
        main_script,
        "--server.port=8502",
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())