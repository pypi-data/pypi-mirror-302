import os
import platform
import subprocess
import sys

def get_binary_path():
    system = platform.system().lower()
    
    if system == "darwin":  # Mac OS X
        return os.path.join(os.path.dirname(__file__), 'binaries', 'mac', 'sybil.arm64')
    
    elif system == "linux":
        return os.path.join(os.path.dirname(__file__), 'binaries', 'linux', 'sybil.amd64')
    
    else:
        raise OSError(f"Unsupported platform: {system}")
