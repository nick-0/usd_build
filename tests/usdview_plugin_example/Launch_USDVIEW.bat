call SET PXR_PLUGINPATH_NAME=%~dp0tutorialPlugin
@REM call SET PXR_PLUGINPATH=%~dp0tutorialPlugin
call conda develop %~dp0
call usdview %~dp0..\MassProps_01.usda
