import os, sys, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


"""
使用watchdog，时刻监控www目录下的代码改动，有改动保存时，先把当前app.py进程杀掉，再重启，就完成了服务器进程的自动重启
"""
def log(s):
    print(f'[Monitor] {s}')

class MyFileSystemEventHander(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        # if event.src_path.endswith('.py'):  # 此处为源码，加上此句修改文件不会自动启动
        log(f'Python source file changed: {event.src_path}')
        self.restart()


command = ['echo', 'ok']
process = None

def kill_process():
    global process
    if process:
        log(f'kill process [{process.pid}]')
        process.kill()
        process.wait()
        log(f'Process ended with code {process.returncode}')
        process = None

def start_process():
    global process, command
    log(f"Start process {' '.join(command)}")
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def restart_process():
    kill_process()
    start_process()

def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    log(f"Watching directory {path}...")
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python3':
        argv.insert(0, 'python3')
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)