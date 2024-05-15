from cx_Freeze import setup, Executable

setup(
    name="LipSync Automation",
    version="1.0",
    description="Automation for LipSync Test in IPGs",
    executables=[Executable("Main.py")]
)
