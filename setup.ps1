# Koala Fleet - Project Setup Script

# Create project structure
$folders = @(
    "agents\orchestrator",
    "agents\hr_agent",
    "agents\finance_agent",
    "agents\it_agent",
    "config",
    "tests",
    "docs",
    "scripts"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder
}

# Create requirements.txt
@"
google-adk>=0.1.0
google-cloud-firestore>=2.11.0
google-cloud-aiplatform>=1.38.0
python-dotenv>=1.0.0
"@ | Out-File -FilePath "requirements.txt" -Encoding UTF8

# Create .env.example
@"
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=koala-fleet
GOOGLE_CLOUD_LOCATION=us-central1
"@ | Out-File -FilePath ".env.example" -Encoding UTF8

# Create .gitignore
@"
venv/
__pycache__/
*.pyc
.env
*.log
.DS_Store
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8

# Create main.py placeholder
@"
from google.adk import Agent

def main():
    print('Koala Fleet - Starting...')
    # TODO: Initialize orchestrator agent

if __name__ == '__main__':
    main()
"@ | Out-File -FilePath "main.py" -Encoding UTF8

Write-Host "Project structure created!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. python -m venv venv"
Write-Host "2. venv\Scripts\activate"
Write-Host "3. pip install -r requirements.txt"
Write-Host "4. Copy .env.example to .env and add your API key"
