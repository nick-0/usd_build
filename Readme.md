# Build Pixar's USD

Context:
-------

-Windows x64 2019

-Python 3.8

-Builds & Packages Stubs: hubbas: https://gist.github.com/hubbas/ba27e8e9b41a27a6e206f9fb15368a63

-Includes usdtools (usdview,...)

Requires:
---------

-Anaconda

-Visual Studio Build Tools 2019

-CMake

-NASM


Installation:
-------------

```console
> conda create --name usd_py38 python=3.8
> conda activate usd_py38
(usd_py38)> git clone https://github.com/nick-0/usd_stubs_windows.git
(usd_py38)> cd usd_stubs_windows
(usd_py38)> build_usd.bat

```
This should clone the USD master branch, build it, create stubs,
 and prepare everything to build a python wheel.

 This very much closely follows the azure-pypi-pipeline.yml for windows,
 with modifications to include the usdtool suite.
