PyInstaller -F -w -i source\icon.ico source\MCNP_IFE.py
mkdir bin
move dist\MCNP_IFE.exe bin
rmdir /S /Q dist
rmdir /S /Q build
del MCNP_IFE.spec
pause