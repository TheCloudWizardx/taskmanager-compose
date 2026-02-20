# Task Manager Application - Docker Capstone Project

**Author:** [Dev Gupta]
**Date:** [February 11, 2026]
**Status:** ✅ Complete

---

## Project Overview

A full-stack task management application demonstrating Docker containerization skills:
- Multi-container architecture
- Custom Docker networks
- Data persistence with volumes

---

## Architecture
```
Client (Browser)
       ↓
   Nginx (Port 80)
       ↓
   ├─→ Frontend (Static HTML/CSS/JS)
   └─→ Backend API (Flask on port 5000)
           ↓
       PostgreSQL (Port 5432)
           ↓
       Volume (task-db-data)
```

---

## Components

### 1. Frontend
- **Tech:** HTML, CSS, JavaScript
- **Features:** 
  - Add/complete/delete tasks
  - Real-time statistics
  - Health check indicator
- **Served by:** Nginx

### 2. Backend
- **Tech:** Python Flask
- **Features:**
  - RESTful API
  - PostgreSQL integration
  - CORS enabled
- **Endpoints:**
  - `GET /api/health` - Health check
  - `GET /api/tasks` - List tasks
  - `POST /api/tasks` - Create task
  - `PUT /api/tasks/<id>` - Update task
  - `DELETE /api/tasks/<id>` - Delete task

### 3. Database
- **Tech:** PostgreSQL 14
- **Storage:** Persistent volume
- **Tables:** tasks (id, title, completed, created_at)

### 4. Reverse Proxy
- **Tech:** Nginx
- **Function:** 
  - Serve static frontend
  - Proxy API requests to backend

---

## Deployment Instructions

### Prerequisites
- Docker installed
- Ports 80 available

### Step 1: Clone/Setup
```bash
mkdir ~/task-manager-app
cd ~/task-manager-app
# [Copy all project files]
```

### Step 2: Build Images
```bash
cd ~/task-manager-app/backend
docker build -t task-backend:v1 .

cd ~/task-manager-app/nginx
docker build -t task-nginx:v1 -f nginx/dockerfile .
```

### Step 3: Create Network and Volume
```bash
docker network create task-network
docker volume create task-db-data
```

### Step 4: Start Containers
```bash
# Database
docker run -d \
  --name database \
  --network task-network \
  -e POSTGRES_DB=taskdb \
  -e POSTGRES_USER=taskuser \
  -e POSTGRES_PASSWORD=taskpass \
  -v task-db-data:/var/lib/postgresql/data \
  postgres:14

# Backend
docker run -d \
  --name backend \
  --network task-network \
  -e DB_HOST=database \
  task-backend:v1

# Nginx
docker run -d \
  --name nginx \
  --network task-network \
  -p 80:80 \
  task-nginx:v1
```

### Step 5: Access Application
```bash
http://localhost
```

---

## Skills Demonstrated

✅ **Dockerfile Creation**
- Multi-stage awareness
- Layer optimization
- Environment variables

✅ **Container Networking**
- Custom networks
- Service discovery by name
- Port isolation

✅ **Data Persistence**
- Named volumes
- Database data retention
- Stateful applications

✅ **Reverse Proxy**
- Nginx configuration
- API proxying
- Static file serving

✅ **Full-Stack Development**
- Frontend-backend separation
- REST API design
- Database integration

✅ **Docker Best Practices**
- One process per container
- Non-root users (where applicable)
- Health checks
- Environment-based configuration

---

## Testing Results

### Functional Tests
- ✅ Add tasks
- ✅ Complete tasks
- ✅ Delete tasks
- ✅ Data persists after container restart
- ✅ Backend health check works
- ✅ Frontend loads correctly

### Technical Tests
- ✅ Containers communicate via custom network
- ✅ Database data survives container deletion
- ✅ Only port 80 exposed to host
- ✅ API requests properly proxied
- ✅ Static files served correctly

---

## Troubleshooting Guide

### Issue: Frontend loads but can't connect to backend
**Solution:** Check nginx config proxies to correct backend hostname

### Issue: Backend can't connect to database
**Solution:** Verify all containers on same network, check DB credentials

### Issue: Tasks don't persist after restart
**Solution:** Ensure volume is mounted correctly to database container

---

## Future Enhancements

- [ ] Add user authentication
- [ ] Implement task categories
- [ ] Add due dates
- [ ] Deploy to cloud (AWS/Azure)
- [ ] Add Docker Compose for easier deployment
- [ ] Implement CI/CD pipeline

---

## Lessons Learned

[Due to this project now I've a broader view of devops, like the development team works and sends the code and how the devops engineer build the container with all the dependecies and libraries, maintaining up time and scalabilty with high availibility.]

---

## Acknowledgments

Built as capstone project for Week 1 Docker fundamentals training.

---

**Project completed:** [February 10, 2026]
**Time invested:** [4-5]
**Status:** Production-ready ✅
