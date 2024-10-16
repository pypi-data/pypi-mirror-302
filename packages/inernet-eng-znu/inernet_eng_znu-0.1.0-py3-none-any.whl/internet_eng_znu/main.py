import requests
import typer
from rich.progress import track
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress
import os
from rich.live import Live
from rich.spinner import Spinner
import time

my_themes = Theme(
    {
        "error": "red on white",
        "success": "green on white"
    }
)
app = typer.Typer()
console = Console(theme=my_themes)

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
@app.command()
def upload(student_number: int, student_password: str, project_type: str):
    supported_project_types = ['node']
    if project_type not in supported_project_types:
        console.print(f"The project type you entered ({project_type}) is not supported. Supported project types: {', '.join(supported_project_types)}", style="error")
        return
    if not os.path.exists("./project.zip"):
        console.print("There is no \"project.zip\" in the current directory. Open up your terminal in the project directory, create a zip file called \"project.zip\" and then try again.", style="error")
        return
    
    
    url = "http://127.1:5000/upload?student_number={}".format(student_number)
    file_path = "./project.zip"
    with Progress() as progress:
        total_size = os.path.getsize(file_path)
        task = progress.add_task("Uploading your project to the server: ", total=total_size)
        with open(file_path, 'rb') as file:
            file_reader = FileWithProgress(file_path, progress, task, chunk_size=1024000)
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
        if response.status_code != 200:
            console.print("\nSomething went wrong.", style="error")
    console.print("\nFile uploaded.", style="success")
    with Live(Spinner("dots", text="Wait for your project to be deployed"), refresh_per_second=10):
        # Simulate a task taking time (e.g., uploading a file)
        time.sleep(5)
    console.print("Deployement failed.", style="error")

        

if __name__ == "__main__":
    app()