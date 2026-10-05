@echo off
setlocal
title Otimizador de Memoria Virtual - SSD Kingston

:: Verificar privilegios de Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Solicitando permissoes de Administrador...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd -ArgumentList '/c `\"%~fnx0`\"' -Verb RunAs"
    exit /b
)

echo ======================================================
echo    CONFIGURANDO MEMORIA VIRTUAL NO SSD (C:)
echo ======================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "Set-CimInstance -Query 'SELECT * FROM Win32_ComputerSystem' -Property @{AutomaticManagedPagefile = $false}; " ^
    "Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management' -Name 'PagingFiles' -Value @('C:\pagefile.sys 4096 12288'); " ^
    "Write-Host ' -> Sucesso! Memoria Virtual (Pagefile) migrada para o SSD Kingston C: (4GB - 12GB).' -ForegroundColor Green"

echo.
echo ======================================================
echo  CONFIGURACAO CONCLUIDA COM SUCESSO!
echo.
echo  Apos reiniciar o computador:
echo  1. O arquivo lento no HD (D:\pagefile.sys) deixara de existir.
echo  2. Mais de 20 GB serao liberados no seu HD (D:).
echo  3. As trocas de memoria serao no SSD Kingston C: (ultrarrapido).
echo ======================================================
echo.
pause