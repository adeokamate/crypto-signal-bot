from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.signals import router as signals_router
from api.backtest import router as backtest_router
from api.portfolio import router as portfolio_router
from api.analytics import router as analytics_router
from api.dashboard import router as dashboard_router


app = FastAPI(
    title="Crypto Signal Bot API",
    description="API backend for crypto signal analysis, backtesting, paper trading and analytics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Crypto Signal Bot API is running"
    }


app.include_router(signals_router)
app.include_router(backtest_router)
app.include_router(portfolio_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)