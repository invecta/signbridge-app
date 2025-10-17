# Quick Heroku Deployment Script for SignBridge
# FASTEST way to get SignBridge running in production

# Prerequisites Check
echo "Checking prerequisites..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Installing Heroku CLI..."
    # Windows
    if [[ "" == "msys" ]]; then
        echo "Please install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli"
        echo "Or run: winget install Heroku.HerokuCLI"
    # macOS
    elif [[ "" == "darwin"* ]]; then
        brew install heroku/brew/heroku
    # Linux
    else
        curl https://cli-assets.heroku.com/install.sh | sh
    fi
fi

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is required but not installed. Please install Git first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is required but not installed. Please install Python first."
    exit 1
fi

echo "Prerequisites check complete!"

# Heroku Deployment Steps
echo "Starting Heroku deployment..."

# Step 1: Login to Heroku
echo "Step 1: Logging into Heroku..."
heroku login

# Step 2: Create Heroku app
echo "Step 2: Creating Heroku app..."
APP_NAME="signbridge-"
heroku create 

# Step 3: Set up environment variables
echo "Step 3: Setting up environment variables..."
heroku config:set SECRET_KEY=5d5ff4fb1ae3e5c4a59690f71dc9a7cac3e0166bf36728c6263c29b1fcfcdc2e --app 
heroku config:set ENVIRONMENT=production --app 
heroku config:set API_KEY=6b8d28e6133e213b02fdabbec4a73519 --app 

# Step 4: Add PostgreSQL database
echo "Step 4: Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini --app 

# Step 5: Add Redis cache
echo "Step 5: Adding Redis cache..."
heroku addons:create heroku-redis:mini --app 

# Step 6: Create Procfile
echo "Step 6: Creating Procfile..."
cat > Procfile << EOF
web: python src/main.py
worker: python src/worker.py
EOF

# Step 7: Create runtime.txt
echo "Step 7: Creating runtime.txt..."
echo "python-3.11.0" > runtime.txt

# Step 8: Update requirements.txt for production
echo "Step 8: Updating requirements.txt..."
cat > requirements.txt << EOF
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
EOF

# Step 9: Deploy to Heroku
echo "Step 9: Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Step 10: Scale the application
echo "Step 10: Scaling application..."
heroku ps:scale web=1 --app 

# Step 11: Open the application
echo "Step 11: Opening application..."
heroku open --app 

echo "Deployment complete!"
echo "Your SignBridge app is now running at: https://.herokuapp.com"
echo ""
echo "Next steps:"
echo "1. Set up custom domain (optional)"
echo "2. Configure monitoring"
echo "3. Set up CI/CD pipeline"
echo "4. Configure backup strategies"
echo ""
echo "Useful commands:"
echo "- View logs: heroku logs --tail --app "
echo "- Scale app: heroku ps:scale web=2 --app "
echo "- View config: heroku config --app "
echo "- Restart app: heroku restart --app "
