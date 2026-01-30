from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth,ceo,manager,ai_tasks

app=FastAPI(title="Smart Sales& Enterprises AI Assistant")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth",tags=["Auth"])
app.include_router(ai_tasks.router,prefix="/AI", tags=["AI"])
app.include_router(manager.router,prefix="/manager",tags=["Manager"])
app.include_router(ceo.router,prefix="/ceo",tags=["ceo"])
