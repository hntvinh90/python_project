set name=CD
PyInstaller -F -w -i source\icon.ico source\%name%.py
mkdir bin
copy dist\CD.exe bin\%name%.exe
rmdir /S /Q dist
rmdir /S /Q build
del %name%.spec
pause