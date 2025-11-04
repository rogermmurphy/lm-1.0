from fastapi import FastAPI
from .config import settings
from .routes import notifications, messages

app = FastAPI(
    title="Notifications Service",
    description="Notifications and messaging service for LM GPA platform",
    version="1.0.0",
    redirect_slashes=False
)

# CORS middleware
# CORS handled by nginx gateway

# Include routers
app.include_router(notifications.router)
app.include_router(messages.router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "notifications",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
