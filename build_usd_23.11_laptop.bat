:: download USD source
git clone https://github.com/PixarAnimationStudios/USD.git
:: activate conda
call conda activate usd_py310
:: install python packages
call python -m pip install --upgrade pip
call python -m pip install PySide2
call python -m pip install PyOpenGL
:: use x64 2022
call "C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
:: build USD
call python USD\build_scripts\build_usd.py C:\dev\usd\usd_23.11_py310 -v
:: build stubs
call conda develop C:\dev\usd\usd_23.11_py310\lib\python
call SET PATH=%PATH%;C:\dev\usd\usd_23.11_py310\bin;C:\dev\usd\usd_23.11_py310\lib
@REM call python generate_use_stubs.py 

echo import os >> "C:\dev\usd\usd_23.11_py310\lib\python\pxr\__init__.py"
echo from pathlib import Path >> "C:\dev\usd\usd_23.11_py310\lib\python\pxr\__init__.py"
echo p = Path(__file__).parents[2] >> "C:\dev\usd\usd_23.11_py310\lib\python\pxr\__init__.py"
echo os.add_dll_directory(p) >> "C:\dev\usd\usd_23.11_py310\lib\python\pxr\__init__.py"