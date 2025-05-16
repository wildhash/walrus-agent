# Deployment Guide for Walrus

## Deployment Options

### Option 1: Vercel + Fly.io (Recommended)

#### Frontend Deployment (Vercel)
1. Push your code to GitHub
2. Connect your GitHub repo to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy frontend from Vercel dashboard

#### Backend Deployment (Fly.io)
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Create app: `fly launch`
4. Deploy: `fly deploy`

### Option 2: Docker + AWS/GCP

#### Docker Setup
1. Create a `Dockerfile` for backend
2. Create a `docker-compose.yml` for local testing
3. Build and push to container registry
4. Deploy to AWS ECS or GCP Cloud Run

## Environment Setup

### Required Environment Variables
```
OPENAI_API_KEY=your_openai_api_key
CDP_API_KEY_NAME=your_cdp_api_key_name
CDP_API_KEY_PRIVATE_KEY=your_cdp_api_private_key
PRIVATE_KEY=your_ethereum_private_key
NETWORK=base-sepolia
```

## Connecting Frontend & Backend

1. Update API URL in frontend code
2. Configure CORS on backend to allow frontend domain
3. Test deployment with environment variables

## Monitoring & Maintenance

1. Set up logging with Fly.io or cloud provider
2. Monitor API usage and responses
3. Set up alerts for errors
