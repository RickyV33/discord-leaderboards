import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = None
        self.restart_script()

    def restart_script(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen([sys.executable, self.script])

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'{event.src_path} has been modified, restarting script...')
            self.restart_script()

if __name__ == "__main__":
    script_to_watch = 'app.py'  # Change this to your script name
    event_handler = ChangeHandler(script_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()