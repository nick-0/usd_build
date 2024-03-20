:: download USD source
git clone https://github.com/PixarAnimationStudios/USD.git
:: activate conda
call conda activate spectra
:: install python packages
call python -m pip install --upgrade pip
call python -m pip install PySide2
call python -m pip install PyOpenGL
:: use x64 2022
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
:: build USD
call python USD\build_scripts\build_usd.py D:\dev\usd\usd_24.03_py310 --draco --openimageio --build-variant release

:: Add dlls to __init__.py
echo import os >> "D:\dev\usd\usd_24.03_py310\lib\python\pxr\__init__.py"
echo from pathlib import Path >> "D:\dev\usd\usd_24.03_py310\lib\python\pxr\__init__.py"
echo p = Path(__file__).parents[2] >> "D:\dev\usd\usd_24.03_py310\lib\python\pxr\__init__.py"
echo os.add_dll_directory(p) >> "D:\dev\usd\usd_24.03_py310\lib\python\pxr\__init__.py"

:: Remove src & build directories
rmdir /S /Q "D:\dev\usd\usd_24.03_py310\src"
rmdir /S /Q "D:\dev\usd\usd_24.03_py310\build"