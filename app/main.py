from app.dramatiq import set_host
set_host()
from fastapi import FastAPI
from app.routes import setup_routes
from app.utils.life_cycle_handler import setup_event_handlers
from app.utils.middlewares import setup_middlewares
app = FastAPI()
setup_routes(app)
setup_middlewares(app)
setup_event_handlers(app)
