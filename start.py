import subprocess

def start_backend():
    subprocess.Popen(['uvicorn','server:app','--host','0.0.0.0','--port','8000'])

def start_frontend():
    subprocess.Popen(['streamlit','run','app.py'])

def install_packages():
    subprocess.run(['pip','install','-r','requirements.txt','-I','--no-cache-dir','--ignore-installed','--ignore-requires-python','--no-deps'])

def main():
    install_packages()
    start_backend()
    subprocess.run(['sleep','20'])
    start_frontend()

if __name__=="__main__":
    main()