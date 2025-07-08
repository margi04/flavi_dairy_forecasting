# Set Python environment variable for this session (update the path as needed)
$pythonPath = "C:\Users\UTSAV BHAGAT\AppData\Local\Programs\Python\Python312"  # <-- Your actual python.exe folder
$env:Path += ";$pythonPath;$pythonPath\Scripts"
Write-Host "Python path added to PATH for this session."
python --version

