# Vercel Deployment Fix - Database Connection

## Problem
Your Flask app was failing with `Error 2003: Can't connect to MySQL server on 'localhost:3306' (111 Connection refused)` when deployed to Vercel because the app was trying to connect to a local MySQL instance that doesn't exist in the serverless environment.

## Solution Implemented

### 1. **Updated Configuration (config/config.py)**
   - Added automatic DATABASE_URL detection
   - Converts different MySQL URL formats to SQLAlchemy format
   - Falls back to localhost for local development
   - Production config now properly uses environment variables

### 2. **Updated Flask App (app.py)**
   - Added intelligent environment detection
   - Automatically switches to production config when DATABASE_URL is set
   - Added error handling for table creation
   - Safe mode: Only drops tables in development

### 3. **Created WSGI Entry Point (wsgi.py)**
   - Required for Vercel to run the Flask app
   - Properly initializes the app with auto-detected config

### 4. **Created Vercel Configuration (vercel.json)**
   - Tells Vercel how to build and deploy your app
   - Sets FLASK_ENV to production
   - Configures Python 3.12 runtime
   - Sets up proper routing

## How to Deploy to Vercel

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Fix Vercel deployment - add database configuration"
git push origin main
```

### Step 2: Connect to Vercel
1. Go to https://vercel.com
2. Click "Import Project"
3. Select your GitHub repository
4. Click "Import"

### Step 3: Set Environment Variables in Vercel
In your Vercel project settings:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:

   **DATABASE_URL** (Required)
   ```
   mysql+mysqlconnector://username:password@your-host:3306/smart_agriculture
   ```
   - Replace `username` with your MySQL username
   - Replace `password` with your MySQL password
   - Replace `your-host` with your MySQL hostname (e.g., from PlanetScale, AWS RDS, or another provider)

   **FLASK_ENV** (Optional - already set in vercel.json)
   ```
   production
   ```

   **SECRET_KEY** (Recommended)
   ```
   your-secret-key-here
   ```

   **JWT_SECRET_KEY** (Recommended)
   ```
   your-jwt-secret-key-here
   ```

   **OPENWEATHER_API_KEY** (If you use this API)
   ```
   your-api-key-here
   ```

### Step 4: Deploy
After setting environment variables, Vercel will automatically redeploy your app.

## MySQL Database Options for Production

Since Vercel doesn't provide MySQL hosting, you need to use an external MySQL provider:

### Option 1: **PlanetScale** (Recommended - Free tier available)
1. Sign up at https://planetscale.com
2. Create a new database
3. Get connection string from "Connect" dropdown
4. Use format: `mysql+mysqlconnector://user:password@host/database`

### Option 2: **AWS RDS**
1. Create an RDS MySQL instance
2. Note the endpoint and credentials
3. Ensure security groups allow Vercel IP ranges

### Option 3: **Digital Ocean MySQL**
1. Create a Managed MySQL Database
2. Get connection string from database panel
3. Convert to SQLAlchemy format

### Option 4: **Google Cloud SQL**
1. Create SQL instance
2. Set up Cloud SQL Auth proxy
3. Get connection string

## Troubleshooting

### Issue: Still getting localhost error
- **Check**: Verify DATABASE_URL is set in Vercel environment variables
- **Check**: Make sure the DATABASE_URL format is correct
- **Check**: Redeploy after adding environment variables

### Issue: "Can't connect to MySQL" even with correct URL
- **Check**: Ensure your MySQL server allows connections from Vercel IP ranges
- **Check**: Verify database username and password are correct
- **Check**: Check if firewall is blocking the connection

### Issue: "Table doesn't exist" error
- The app will auto-create tables on first run
- If using a fresh database, this is normal
- Tables will be created automatically

## Local Development

Your local development setup remains unchanged:
```bash
# Still uses localhost:3306
python app.py
```

The app detects the environment and uses the appropriate config automatically.

## Testing the Deployment

After deployment, test the connection:
```bash
curl https://your-vercel-app.vercel.app/
```

The app should load without database connection errors.

## Security Notes

- Never commit `.env` files to GitHub
- Use Vercel's environment variables UI to manage secrets
- Rotate passwords periodically
- Use strong, unique passwords for production databases

## Additional Help

- Vercel Docs: https://vercel.com/docs
- Flask Deployment: https://flask.palletsprojects.com/deployment/
- SQLAlchemy MySQL: https://docs.sqlalchemy.org/en/20/dialects/mysql.html
