import setuptools
import platform

system = platform.system().lower()

# Determine which files to include based on platform
if system == "darwin":
    data_files = [("sybil-bin/binaries/mac", ["sybil-bin/binaries/mac/sybil.arm64"])]
elif system == "linux":
    data_files = [("sybil-bin/binaries/linux", ["sybil-bin/binaries/linux/sybil"])]
else:
    raise OSError(f"Unsupported platform: {system}")

setuptools.setup(
    name="sybil-bin",
    version="0.5.2",
    description="A sybil binary package with platform-specific binaries",
    packages=["sybil-bin"],
    package_data={"sybil-bin": ["binaries/mac/*", "binaries/linux/*"]},
    data_files=data_files,
    include_package_data=True,
    install_requires=[],
    entry_points={
    },
)

