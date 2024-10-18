import os
import platform
import requests
import tarfile
import zipfile
from pathlib import Path
from platformdirs import user_data_dir

BASE_URL = "https://github.com/spacejar-labs/spacejar-cli/releases/download/v0.1.0-test/"
BINARY_NAME = "spacejar"

BINARY_URLS = {
    "Linux": f"{BASE_URL}spacejar-0.1.0-x86_64-unknown-linux-gnu.tar.gz",
    "Darwin": f"{BASE_URL}spacejar",
    "Windows": f"{BASE_URL}spacejar-0.1.0-x86_64-pc-windows-msvc.zip"
}

def get_os():
    os_name = platform.system()
    if os_name not in BINARY_URLS:
        raise RuntimeError(f"Unsupported operating system: {os_name}")
    return os_name

def download_binary(os_name, install_dir):
    url = BINARY_URLS[os_name]
    response = requests.get(url, stream=True)
    response.raise_for_status()

    if url.endswith(".tar.gz"):
        with tarfile.open(fileobj=response.raw, mode="r:gz") as tar:
            tar.extractall(path=install_dir)
    elif url.endswith(".zip"):
        with zipfile.ZipFile(response.raw) as zip_ref:
            zip_ref.extractall(path=install_dir)
    else:
        # Direct binary download (for macOS)
        binary_path = install_dir / BINARY_NAME
        with open(binary_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def get_install_dir():
    paths = [
        Path.home() / ".local" / "bin",
        Path.home() / "bin",
        Path(user_data_dir("spacejar"))
    ]
    for path in paths:
        print(f"Checking path: {path}")
        if os.access(str(path.parent), os.W_OK):
            print(f"Found writable parent directory: {path.parent}")
            path.mkdir(parents=True, exist_ok=True)
            print(f"Created directory (if it didn't exist): {path}")
            return path
        else:
            print(f"Parent directory not writable: {path.parent}")
    raise RuntimeError("No writable directory found in PATH")

def install_binary():
    print("Installing Rust binary...")
    os_name = get_os()
    install_dir = get_install_dir()

    print(f"Downloading {BINARY_NAME} binary for {os_name}...")
    download_binary(os_name, install_dir)

    binary_path = install_dir / BINARY_NAME
    if os_name != "Windows":
        binary_path.chmod(0o755)

    print(f"Binary installed at: {binary_path}")
    print(f"Make sure {install_dir} is in your PATH.")

    # Update PATH if necessary
    if str(install_dir) not in os.environ["PATH"]:
        print(f"Consider adding the following to your shell configuration:")
        print(f"export PATH=\"$PATH:{install_dir}\"")

def main():
    install_binary()

if __name__ == "__main__":
    main()