:: download USD source
git clone https://github.com/PixarAnimationStudios/USD.git
:: activate conda
call conda activate usd_py38
:: use x64 2019
:: build USD
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat" && python USD\build_scripts\build_usd.py .\inst --build-args USD,-DPXR_INSTALL_LOCATION=../pxr/pluginfo 
:: build stubs
call conda develop %~dp0\inst\lib\python
call SET PATH=%PATH%;%~dp0\inst\bin;%~dp0\inst\lib
call python generate_use_stubs.py 
:: make a pypi directory -> BUILD_DIR
mkdir pypi
call python setup.py bdist_wheel