import requests
import typer
from rich.progress import track
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, DownloadColumn, BarColumn, ProgressColumn, TotalFileSizeColumn, TextColumn, FileSizeColumn, TaskProgressColumn, TimeRemainingColumn, TransferSpeedColumn
import os
from rich.live import Live
from rich.spinner import Spinner
import time
from rich.panel import Panel
from rich import box
from rich.style import Style
from . import keymanager

app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)

error_style = "red"
success_style = "green"
console = Console()
key_manager = keymanager.KeyManager()
LOCAL_SERVER_PATH = '127.1:5000'
REMOTE_SERVER_PATH = '78.38.35.219/deployment'
CURRENT_SERVER_PATH = REMOTE_SERVER_PATH

class FileWithProgress:
    def __init__(self, file_path, progress, progress_task, chunk_size=1024):
        self.file_path = file_path
        self.file_size = os.path.getsize(file_path)
        self.file = open(file_path, 'rb')
        self.chunk_size = chunk_size
        self.bytes_uploaded = 0
        self.progress = progress
        self.progress_task = progress_task

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.file.read(self.chunk_size)
        if not chunk:
            self.file.close()
            raise StopIteration
        self.bytes_uploaded += len(chunk)
        self.progress.update(self.progress_task, completed=self.bytes_uploaded)
        return chunk

    def close(self):
        self.file.close()
    
def print_server_response(response, console):
    try:
        data = response.json()
    except:
        console.print(Panel("The server sent an unexpected response.", style=success_style if response.status_code == 200 else error_style, box=box.SQUARE))
    else:
        console.print(Panel(data.get("message"), style=success_style if response.status_code == 200 else error_style, box=box.SQUARE))

@app.command()
def deploy(project_type: str, student_number: int, student_password: int):
    supported_project_types = ['node', 'static']
    encrypted_password = key_manager.encrypt_message(str(student_password))
    if project_type not in supported_project_types:
        message = f"The project type you entered ({project_type}) is not supported. Supported project types are: {', '.join(supported_project_types)}"
        console.print(Panel(message, style=error_style, box=box.SQUARE))
        return
    
    if not os.path.exists("./project.zip"):
        message = "There is no \"project.zip\" in the current directory. Create a zip file containing your project files called \"project.zip\", open up your terminal where that file is located and then try again."
        console.print(Panel(message, style=error_style, box=box.SQUARE))
        return
    
    # authenticate first to prevent wasteful uploading
    with Live(Spinner("dots", text="We are authenticating you...", style="white"), refresh_per_second=10):
        url = "http://{}/authenticate?student_number={}&password={}".format(CURRENT_SERVER_PATH, student_number, encrypted_password)
        response = requests.post(url)
        
    if response.status_code != 200:
        message = 'Authentication failed. Contact the system owner to get your credentials.'
        console.print(Panel(message, style=error_style, box=box.SQUARE))
        return
    else:
        message = 'Authentication was successfull.'
        console.print(Panel(message, style=success_style, box=box.SQUARE))
        
    url = "http://{}/upload?student_number={}&password={}".format(CURRENT_SERVER_PATH, student_number, encrypted_password)
    file_path = "./project.zip"
    
    with Progress(SpinnerColumn(style="white"), TextColumn("{task.description}"), BarColumn(), DownloadColumn(), TimeRemainingColumn()) as progress:
        total_size = os.path.getsize(file_path)
        task = progress.add_task("Uploading your project to the server: ", total=total_size)
        with open(file_path, 'rb') as file:
            file_reader = FileWithProgress(file_path, progress, task, chunk_size=102400)
            response = requests.post(
                url, 
                data=file_reader,
                headers={'Content-Type': 'application/octet-stream'},
                proxies={
                    "http": "",
                    "https": "",
                    "socks5": "",
                    "all": "",
                }
            )
    print_server_response(response, console)
    if response.status_code != 200:
        return
    
    with Live(Spinner("dots", text="Wait till your project gets deployed...", style="white"), refresh_per_second=10):
        url = "http://{}/deploy?student_number={}&project_type={}&password={}".format(CURRENT_SERVER_PATH, student_number, project_type, encrypted_password)
        response = requests.get(url)

    print_server_response(response, console)

        
@app.command()
def who_made_this():
    message = '2024 Ali Safapour'
    panel = Panel(message, style="blue", box=box.SQUARE)

    console.print(panel)

if __name__ == "__main__":
    app()