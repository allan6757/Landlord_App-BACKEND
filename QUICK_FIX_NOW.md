# 🚨 FIX THESE 3 THINGS NOW

## 1️⃣ Fix API URL in Frontend

In your frontend `.env` file:
```bash
VITE_API_BASE_URL=https://landlord-app-backend-1eph.onrender.com/api
```

In your API config file:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
```

---

## 2️⃣ Fix Role Check (Why Both Views Look Same)

**WRONG WAY:**
```javascript
const role = user.role;  // ❌ This doesn't work
```

**RIGHT WAY:**
```javascript
const role = user?.profile?.role;  // ✅ This works
```

**Use this everywhere:**
```javascript
// Get role
const getUserRole = () => {
  const user = JSON.parse(localStorage.getItem('user'));
  return user?.profile?.role;
};

// Check if landlord
const isLandlord = () => getUserRole() === 'landlord';

// Check if tenant  
const isTenant = () => getUserRole() === 'tenant';
```

**Show different views:**
```javascript
{isLandlord() && <LandlordDashboard />}
{isTenant() && <TenantDashboard />}

{isLandlord() && <button>Add Property</button>}
```

---

## 3️⃣ Fix API Calls (Add Token)

**Every API call needs Authorization header:**

```javascript
const token = localStorage.getItem('token');

fetch(`${API_BASE_URL}/properties`, {
  headers: { 
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
```

---

## ✅ Test Before Presentation

1. **Register as landlord:**
   - Email: landlord@test.com
   - Password: password123
   - Role: landlord ← MUST select this

2. **Check in console:**
   ```javascript
   const user = JSON.parse(localStorage.getItem('user'));
   console.log(user.profile.role); // Should show "landlord"
   ```

3. **Logout and register as tenant:**
   - Email: tenant@test.com
   - Password: password123
   - Role: tenant ← MUST select this

4. **Verify:**
   - Landlord sees "Add Property" button
   - Tenant does NOT see "Add Property" button
   - Each sees different dashboard

---

## 🆘 Still Broken?

**Check browser console for errors:**
- CORS error → Backend issue (already fixed)
- 401 error → Token not being sent
- 403 error → Wrong role trying to access

**Quick debug:**
```javascript
// Paste in browser console
console.log('Token:', localStorage.getItem('token'));
console.log('User:', JSON.parse(localStorage.getItem('user')));
console.log('Role:', JSON.parse(localStorage.getItem('user'))?.profile?.role);
```

---

## 📋 Presentation Checklist

- [ ] Can register as landlord
- [ ] Can register as tenant  
- [ ] Landlord sees "Add Property"
- [ ] Tenant does NOT see "Add Property"
- [ ] Can create property as landlord
- [ ] Properties load with token
- [ ] Chat loads with token

**Good luck with your presentation! 🎉**
