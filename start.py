import subprocess

def start():
    # Start the backend
    python_path = '.venv/Scripts/python.exe'
    backend = subprocess.Popen([python_path, './server/run.py'])

    # Start the frontend
    frontend = subprocess.Popen(['pnpm', 'run', 'dev'], cwd='./client')

    # Wait for both processes to finish
    backend.wait()
    frontend.wait()

if __name__ == '__main__':
    start()