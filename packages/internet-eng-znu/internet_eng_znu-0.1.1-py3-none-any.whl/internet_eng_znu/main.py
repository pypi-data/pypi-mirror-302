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
app = typer.Typer()
error_style = "red"
success_style = "green"
console = Console()

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
def upload(student_number: int, student_password: str, project_type: str):
    supported_project_types = ['node']
    if project_type not in supported_project_types:
        message = f"The project type you entered ({project_type}) is not supported. Supported project types are: {', '.join(supported_project_types)}"
        console.print(Panel(message, style=error_style, box=box.SQUARE))
        return
    if not os.path.exists("./project.zip"):
        message = "There is no \"project.zip\" in the current directory. Create a zip file containing your project files called \"project.zip\", open up your terminal where that file is located and then try again."
        console.print(Panel(message, style=error_style, box=box.SQUARE))
        return
    
    
    url = "http://127.1:5000/upload?student_number={}".format(student_number)
    file_path = "./project.zip"
    with Progress(SpinnerColumn(), TextColumn("{task.description}"), BarColumn(), DownloadColumn(), TimeRemainingColumn()) as progress:
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
    with Live(Spinner("dots", text="Wait till your project gets deployed..."), refresh_per_second=10):
        # Simulate a task taking time (e.g., uploading a file)
        url = "http://127.1:5000/deploy?student_number={}&project_type={}".format(student_number, project_type)
        response = requests.get(url)

    print_server_response(response, console)

        
        

if __name__ == "__main__":
    app()