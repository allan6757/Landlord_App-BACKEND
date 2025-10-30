# Deployment Checklist ✅

## 🌐 Production URLs

- **Backend API**: https://landlord-app-backend-1eph.onrender.com
- **Frontend App**: https://landlord-app-frontend.vercel.app

---

## Backend (Render) - Environment Variables

Make sure these are set in your Render dashboard:

```bash
# Required
SECRET_KEY=<your-production-secret-key>
JWT_SECRET_KEY=<your-production-jwt-secret>
DATABASE_URL=<automatically-set-by-render>
FLASK_ENV=production

# CORS - Allow your frontend
CORS_ORIGINS=https://landlord-app-frontend.vercel.app,http://localhost:3000
FRONTEND_URL=https://landlord-app-frontend.vercel.app

# M-Pesa (if using payments)
MPESA_CONSUMER_KEY=<your-mpesa-key>
MPESA_CONSUMER_SECRET=<your-mpesa-secret>
MPESA_BUSINESS_SHORTCODE=<your-shortcode>
MPESA_PASSKEY=<your-passkey>

# Email (if using email verification)
SENDGRID_API_KEY=<your-sendgrid-key>
SENDGRID_FROM_EMAIL=noreply@yourdomain.com

# Image Upload (if using Cloudinary)
CLOUDINARY_CLOUD_NAME=<your-cloud-name>
CLOUDINARY_API_KEY=<your-api-key>
CLOUDINARY_API_SECRET=<your-api-secret>
```

---

## Frontend (Vercel) - Environment Variables

Set these in your Vercel project settings:

### For React (Create React App):
```bash
REACT_APP_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

### For Vite:
```bash
VITE_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

### For Next.js:
```bash
NEXT_PUBLIC_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

---

## ✅ Deployment Verification

### 1. Test Backend Health
```bash
curl https://landlord-app-backend-1eph.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Rental Platform API is running",
  "database": "connected",
  "environment": "production"
}
```

### 2. Test CORS
Open browser console on https://landlord-app-frontend.vercel.app and run:
```javascript
fetch('https://landlord-app-backend-1eph.onrender.com/api/properties', {
  headers: { 'Authorization': 'Bearer <your-token>' }
})
.then(r => r.json())
.then(console.log)
```

Should NOT see CORS errors.

### 3. Test Authentication
Try registering/logging in from your frontend app.

### 4. Test API Endpoints
- Create a property (landlord)
- View properties
- Send a message
- Make a payment (if M-Pesa configured)

---

## 🔧 Common Issues

### CORS Errors
**Problem**: Frontend can't connect to backend  
**Solution**: Verify `CORS_ORIGINS` in Render includes your Vercel URL

### 404 on API Calls
**Problem**: API endpoints return 404  
**Solution**: Ensure you're using `/api` prefix in all requests

### Database Connection Failed
**Problem**: Backend can't connect to database  
**Solution**: Check `DATABASE_URL` is set correctly in Render

### M-Pesa Not Working
**Problem**: Payments fail  
**Solution**: Verify all M-Pesa credentials are set and valid

---

## 📝 Post-Deployment Tasks

- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] User registration works
- [ ] User login works
- [ ] Properties can be created
- [ ] Properties can be viewed
- [ ] Chat/messaging works
- [ ] Payments work (if configured)
- [ ] Email verification works (if configured)
- [ ] Image uploads work (if configured)

---

## 🔄 Updating Deployments

### Backend (Render)
- Push changes to your GitHub repo
- Render auto-deploys on push (if enabled)
- Or manually deploy from Render dashboard

### Frontend (Vercel)
- Push changes to your GitHub repo
- Vercel auto-deploys on push
- Or manually deploy from Vercel dashboard

---

## 📞 Support

If you encounter issues:
1. Check Render logs for backend errors
2. Check Vercel logs for frontend errors
3. Verify all environment variables are set correctly
4. Test API endpoints with Postman/curl
5. Check browser console for frontend errors
