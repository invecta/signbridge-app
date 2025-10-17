# SignBridge Heroku Deployment Guide (Windows)
# Step-by-step deployment instructions

## Prerequisites Installation

### 1. Install Heroku CLI
`powershell
# Option 1: Using winget (recommended)
winget install Heroku.HerokuCLI

# Option 2: Download from website
# Visit: https://devcenter.heroku.com/articles/heroku-cli
`

### 2. Install Git (if not already installed)
`powershell
winget install Git.Git
`

### 3. Verify Python Installation
`powershell
python --version
# Should show Python 3.8 or higher
`

## Heroku Deployment Steps

### Step 1: Login to Heroku
`powershell
heroku login
`

### Step 2: Create Heroku App
`powershell
# Create app with unique name
heroku create signbridge-app-[random-number]
# Example: heroku create signbridge-app-12345
`

### Step 3: Set Environment Variables
`powershell
# Set secret key
heroku config:set SECRET_KEY=your-secret-key-here

# Set environment
heroku config:set ENVIRONMENT=production

# Set API key
heroku config:set API_KEY=your-api-key-here
`

### Step 4: Add Database
`powershell
heroku addons:create heroku-postgresql:mini
`

### Step 5: Add Redis Cache
`powershell
heroku addons:create heroku-redis:mini
`

### Step 6: Create Procfile
Create a file named Procfile in the root directory:
`
web: python src/main.py
worker: python src/worker.py
`

### Step 7: Create runtime.txt
Create a file named untime.txt in the root directory:
`
python-3.11.0
`

### Step 8: Update requirements.txt
Ensure your requirements.txt includes:
`
opencv-python==4.12.0.88
numpy==2.2.6
speechrecognition==3.14.3
pyttsx3==2.99
PyAudio==0.2.14
tensorflow==2.20.0
scikit-learn
matplotlib
seaborn
h5py
flask==2.3.3
gunicorn==21.2.0
psycopg2-binary==2.9.7
redis==4.6.0
python-dotenv==1.0.0
`

### Step 9: Deploy to Heroku
`powershell
# Add all files to git
git add .

# Commit changes
git commit -m "Deploy to Heroku"

# Push to Heroku
git push heroku main
`

### Step 10: Scale Application
`powershell
heroku ps:scale web=1
`

### Step 11: Open Application
`powershell
heroku open
`

## Post-Deployment

### View Logs
`powershell
heroku logs --tail
`

### Scale Application
`powershell
# Scale to 2 web dynos
heroku ps:scale web=2

# Scale to 1 worker dyno
heroku ps:scale worker=1
`

### View Configuration
`powershell
heroku config
`

### Restart Application
`powershell
heroku restart
`

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt and Python version
2. **App crashes**: Check logs with heroku logs --tail
3. **Database issues**: Verify PostgreSQL addon is installed
4. **Memory issues**: Scale up dyno type

### Useful Commands:
`powershell
# Check app status
heroku ps

# View app info
heroku info

# Access app console
heroku run python

# View addons
heroku addons
`

## Cost Estimation
- **Hobby Dyno**: /month (web only)
- **Standard Dyno**: /month (web + worker)
- **PostgreSQL Mini**: /month
- **Redis Mini**: /month
- **Total**: -35/month

## Next Steps After Deployment
1. Set up custom domain
2. Configure SSL certificates
3. Set up monitoring
4. Configure backups
5. Set up CI/CD pipeline
