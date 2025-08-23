# Specimen Tracker Startup Script
Write-Host "Starting Specimen Tracker..." -ForegroundColor Green
Write-Host ""

# Change to the script directory
Set-Location $PSScriptRoot

# Start the Flask application
Write-Host "Starting Flask server on http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Red
Write-Host ""

# Open browser after a short delay
Start-Sleep -Seconds 2
Start-Process "http://localhost:5000"

# Start the Flask app
& "C:\Users\findl\AppData\Local\Programs\Python\Python313\python.exe" wsgi.py
