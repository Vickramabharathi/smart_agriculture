"""
WSGI entry point for Vercel and other production servers.
This file is required for deploying Flask apps to serverless platforms like Vercel.
"""
import os
from app import create_app

# Auto-detect environment
app = create_app()

if __name__ == '__main__':
    app.run()
