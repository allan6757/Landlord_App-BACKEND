# Render Deployment Guide

## Quick Deploy Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### 2. Deploy on Render
1. Go to [render.com](https://render.com) and sign in
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Select this repository
5. Render will automatically detect `render.yaml` and create:
   - PostgreSQL database
   - Web service with auto-deploy

### 3. Environment Variables (Auto-configured)
- `SECRET_KEY` - Auto-generated
- `JWT_SECRET_KEY` - Auto-generated  
- `DATABASE_URL` - Auto-linked to PostgreSQL
- `FLASK_ENV` - Set to `production`

### 4. Get Your API URL
After deployment, your API will be available at:
```
https://rental-platform-api.onrender.com
```

## Frontend Integration

### Update Frontend API Base URL
Replace your frontend API calls to use:
```javascript
const API_BASE_URL = 'https://rental-platform-api.onrender.com/api'
```

### CORS Configuration
The backend is configured to accept requests from any origin (`*`) for development. 
For production, update `CORS_ORIGINS` environment variable in Render dashboard:
```
CORS_ORIGINS=https://your-frontend-domain.com,https://your-app.netlify.app
```

## API Endpoints Available

### Authentication
- `POST /api/auth/register`
- `POST /api/auth/login` 
- `GET /api/auth/profile`

### Properties
- `GET /api/properties`
- `POST /api/properties`
- `GET /api/properties/{id}`
- `PUT /api/properties/{id}`
- `DELETE /api/properties/{id}`

### Payments
- `GET /api/payments`
- `POST /api/payments`
- `GET /api/payments/{id}`
- `PUT /api/payments/{id}`

### Chat
- `GET /api/conversations`
- `POST /api/conversations`
- `GET /api/conversations/{id}/messages`
- `POST /api/conversations/{id}/messages`

## Sample API Usage

```javascript
// Login
const response = await fetch('https://rental-platform-api.onrender.com/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'landlord@example.com', password: 'password123' })
})

// Use token for authenticated requests
const token = response.data.access_token
const properties = await fetch('https://rental-platform-api.onrender.com/api/properties', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

## Database
- PostgreSQL database auto-created
- Sample data automatically seeded
- Migrations run on each deployment