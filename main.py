from fastapi import FastAPI,  Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database.database import get_db
from database.database import engine, Base
#from routes.organization_routes import router as org_router
from routes.users_routes import router as user_router
from routes.auth_routes import router as auth_router
#from routes.certification_routes import router as certification_router
#from routes.leave_route import router as leave_router
#from routes.leave_route import router as leaverequests_router
#from routes.timesheet_routes import router as timesheet_router
#from routes.project_routes import router as project_router
#from routes.userprojectmapping_routes import router as userprojectmapping_router
#from routes.performance_routes import router as performance_review_router
from sqlalchemy import text 
from routes.goal_routes import router as goals_router
from routes.feedback_routes import router as feedback_router
import logging

# Load .env for local; in cloud, Secret Manager values are read at access time
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DigiElevate API", version="1.0.0")

# CORS: relax for dev to avoid blocked requests from Vite (any port)
# NOTE: For prod, replace with explicit origins and enable credentials if needed.
# CORS must be added first, before other middleware
allowed_origin = [
   "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origin,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



# mount your API under /api
app.include_router(auth_router, prefix="/api/auth")
#app.include_router(org_router, prefix="/api/organization")
app.include_router(user_router, prefix="/api/user")
#app.include_router(certification_router, prefix="/api/user/certification")
#app.include_router(leave_router, prefix="/api/user/leave")
#app.include_router(leave_router, prefix="/api/user/leaverequests")
#app.include_router(timesheet_router, prefix="/api/user/timesheet")
#app.include_router(project_router, prefix="/api/user/project")
#app.include_router(userprojectmapping_router, prefix="/api/user/userprojectmapping")
#app.include_router(performance_review_router, prefix="/api/performance")
app.include_router(goals_router,prefix="/api/goals")
app.include_router(feedback_router,prefix="/api/feedback")



@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting DigiElevate application...")
    
    # Test database connection first
    try:
        logger.info("Testing database connection...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        logger.info("Database connection successful!")
    except Exception as e:
        error_msg = str(e)
        logger.error("=" * 60)
        logger.error("DATABASE CONNECTION FAILED")
        logger.error("=" * 60)
        logger.error(f"Error: {error_msg}")
        
        # Check if database doesn't exist
        if "does not exist" in error_msg or "database" in error_msg.lower() and "exist" in error_msg.lower():
            logger.error("DATABASE DOES NOT EXIST")
            logger.error("")
            logger.error("The database 'digielevate' needs to be created first.")
            logger.error("")
            logger.error("To create the database, run one of these commands:")
            logger.error("")
            logger.error("Option 1 - Using psql command line:")
            logger.error("   psql -U postgres")
            logger.error("   CREATE DATABASE digielevate;")
            logger.error("   \\q")
            logger.error("")
            logger.error("Option 2 - Using createdb command:")
            logger.error("   createdb -U postgres digielevate")
            logger.error("")
            logger.error("Option 3 - Using pgAdmin:")
            logger.error("   1. Open pgAdmin")
            logger.error("   2. Right-click on 'Databases'")
            logger.error("   3. Select 'Create' -> 'Database'")
            logger.error("   4. Name it 'digielevate' and click 'Save'")
            logger.error("")
            logger.error("After creating the database, restart this application.")
            logger.error("=" * 60)
            logger.warning("Application will start but database operations will fail!")
            logger.warning("Create the database before using database-dependent endpoints.")
            return
        
        if "could not open file" in error_msg or "Invalid argument" in error_msg:
            logger.error("POSTGRESQL DATABASE CORRUPTION DETECTED")
            logger.error("")
            logger.error("This error typically indicates:")
            logger.error("1. Database file system corruption")
            logger.error("2. Insufficient disk space")
            logger.error("3. File system permissions issues")
            logger.error("4. PostgreSQL data directory problems")
            logger.error("")
            logger.error("Recommended solutions:")
            logger.error("1. Check disk space: df -h (Linux/Mac) or check Windows disk")
            logger.error("2. Check PostgreSQL logs for more details")
            logger.error("3. Try restarting PostgreSQL service:")
            logger.error("   - Windows: Restart PostgreSQL service from Services")
            logger.error("   - Linux: sudo systemctl restart postgresql")
            logger.error("4. Connect to PostgreSQL and run: SELECT pg_reload_conf();")
            logger.error("5. If corruption persists:")
            logger.error("   - Try: REINDEX DATABASE your_database_name;")
            logger.error("   - Or restore from backup using pg_restore")
            logger.error("=" * 60)
        else:
            logger.error("Please check your DATABASE_URL in .env file")
            logger.error("Verify PostgreSQL is running and accessible")
            logger.error("=" * 60)
        
        logger.warning("Application will start but database operations may fail!")
        logger.warning("Fix the database issue before using database-dependent endpoints.")
        return
    
    # Try to create tables (they may already exist)
    try:
        logger.info("Initializing database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully!")
    except Exception as e:
        error_msg = str(e)
        
        # Check if it's the corruption error
        if "could not open file" in error_msg or "Invalid argument" in error_msg:
            logger.error("=" * 60)
            logger.error("DATABASE CORRUPTION DETECTED DURING TABLE CREATION")
            logger.error("=" * 60)
            logger.error("The database connection works, but table creation failed due to corruption.")
            logger.error("")
            logger.error("IMMEDIATE ACTIONS REQUIRED:")
            logger.error("1. Stop this application")
            logger.error("2. Restart PostgreSQL service:")
            logger.error("   - Windows: Services → PostgreSQL → Restart")
            logger.error("   - Linux: sudo systemctl restart postgresql")
            logger.error("")
            logger.error("3. Connect to PostgreSQL and check database integrity:")
            logger.error("   psql -U your_user -d your_database")
            logger.error("   SELECT pg_reload_conf();")
            logger.error("")
            logger.error("4. Try to repair the database:")
            logger.error("   REINDEX DATABASE your_database_name;")
            logger.error("   VACUUM FULL;")
            logger.error("")
            logger.error("5. Alternative: Use Alembic migrations instead of create_all():")
            logger.error("   alembic upgrade head")
            logger.error("")
            logger.error("6. Or create tables manually using SQL script:")
            logger.error("   psql -U your_user -d your_database -f create_timesheet_table.sql")
            logger.error("")
            logger.error("7. If corruption persists, restore from backup")
            logger.error("=" * 60)
            logger.error("")
            logger.warning("⚠️  Tables may not be created. Database operations will fail!")
            logger.warning("⚠️  Fix the database corruption before using the application.")
            logger.warning("⚠️  Or use: alembic upgrade head (to create tables via migrations)")
        else:
            logger.warning(f"Could not create tables (they may already exist): {error_msg}")
            logger.warning("If tables don't exist, you may need to run migrations manually.")
            logger.warning("Try: alembic upgrade head")
    
    logger.info("DigiElevate API is ready!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to DigiElevate API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
        "auth": "/api/auth"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to verify database connectivity"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }




# dev entry (if you run python -m app.main)
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8080)