import os
import requests
import zipfile
import platform

def download_edgedriver():
    arch = platform.architecture()[0] 
    edgedriver_url = ""

    if arch == '64bit':
        edgedriver_url = "https://msedgedriver.azureedge.net/129.0.2792.79/edgedriver_win64.zip"
    elif arch == '32bit':
        edgedriver_url = "https://msedgedriver.azureedge.net/129.0.2792.79/edgedriver_win32.zip"
    else:
        return

    edgedriver_zip_path = "edgedriver.zip"
    edgedriver_exe_path = "edgedriver_win64/msedgedriver.exe" if arch == '64bit' else "edgedriver_win32/msedgedriver.exe"

    if not os.path.exists(edgedriver_exe_path):
        response = requests.get(edgedriver_url)
        with open(edgedriver_zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(edgedriver_zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')

        os.remove(edgedriver_zip_path)

if __name__ == "__main__":
    download_edgedriver()
