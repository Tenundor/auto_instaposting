from pathlib import Path
import requests


Path(Path.cwd() / 'images').mkdir(parents=True, exist_ok=True)
filename = Path.cwd() / 'images/HST-SM4.jpeg'
url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

response = requests.get(url)
response.raise_for_status()

with open(filename, 'wb') as file:
    file.write(response.content)
