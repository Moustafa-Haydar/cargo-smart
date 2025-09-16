# Route Automation Setup Guide

## Overview
This automation system continuously monitors routes, predicts delays using ML, and suggests optimizations to operations managers.

## Architecture
- **n8n**: Automation workflow engine (runs every 5 minutes)
- **Django Backend**: ML predictions and route management APIs
- **Angular Frontend**: Operations manager interface with suggestion approval
- **PostgreSQL**: Database for both Django and n8n

## Setup Instructions

### 1. Start the Services
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 2. Access the Applications
- **Frontend (React)**: http://localhost:80
- **Operations Manager (Angular)**: http://localhost:4200 (if running locally)
- **Backend API**: http://localhost:5001
- **n8n Automation**: http://localhost:5678
  - Username: `admin`
  - Password: `admin123`
- **Database Admin**: http://localhost:8080

### 3. Import n8n Workflow
1. Go to http://localhost:5678
2. Login with admin/admin123
3. Click "Import from File"
4. Upload `n8n/workflows/route-monitoring-workflow.json`
5. Activate the workflow

### 4. Run Database Migrations
```bash
# Access backend container
docker-compose exec backend bash

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Test the System
1. **Check Active Shipments**: Visit `/api/agent_reroute/shipments/active/`
2. **Trigger Manual Evaluation**: POST to `/api/agent_reroute/batch-evaluate/` with shipment IDs
3. **View Suggestions**: Visit `/api/agent_reroute/suggestions/pending/`
4. **Check Routes Page**: Navigate to routes page in operations manager

## How It Works

### Automation Flow
1. **Every 5 minutes**, n8n triggers the workflow
2. **Fetches active shipments** from Django API
3. **Runs ML predictions** for delay probability
4. **Evaluates route alternatives** using the agent system
5. **Creates suggestions** for routes needing optimization
6. **Updates the database** with pending suggestions

### Operations Manager Interface
1. **Routes page** shows all routes and pending suggestions
2. **Suggestion cards** display:
   - Delay risk percentage
   - Current vs proposed ETA
   - Improvement percentage
   - AI rationale
3. **Approve/Reject buttons** for each suggestion
4. **Real-time updates** when actions are taken

### API Endpoints
- `GET /api/agent_reroute/shipments/active/` - Get active shipments
- `POST /api/agent_reroute/batch-evaluate/` - Batch evaluate routes
- `GET /api/agent_reroute/suggestions/pending/` - Get pending suggestions
- `POST /api/agent_reroute/suggestions/{id}/approve/` - Approve suggestion
- `POST /api/agent_reroute/suggestions/{id}/reject/` - Reject suggestion

## Configuration

### n8n Workflow Settings
- **Schedule**: Every 5 minutes (configurable)
- **Timeout**: 30 seconds per API call
- **Retry**: 3 attempts on failure

### ML Model Settings
- **Delay Threshold**: 0.3 (30% probability)
- **Improvement Threshold**: 5% minimum improvement
- **Suggestion Expiry**: 2 hours

### Database
- **PostgreSQL**: Main application database
- **n8n Database**: Separate database for workflow data
- **Persistence**: All data persisted in Docker volumes

## Monitoring

### Health Checks
- All services have health checks configured
- n8n workflow logs available in the interface
- Django logs accessible via `docker-compose logs backend`

### Troubleshooting
1. **Check service status**: `docker-compose ps`
2. **View logs**: `docker-compose logs [service-name]`
3. **Restart services**: `docker-compose restart [service-name]`
4. **Check database**: Access Adminer at http://localhost:8080

## Customization

### Modify Schedule
Edit the n8n workflow to change the monitoring frequency.

### Adjust ML Thresholds
Update `backend/apps/agent_reroute/decision_maker.py` settings.

### Add Notifications
Extend the n8n workflow to send emails/SMS when suggestions are created.

## Security Notes
- n8n has basic auth enabled (admin/admin123)
- Change default passwords in production
- Use environment variables for sensitive data
- Enable HTTPS in production
