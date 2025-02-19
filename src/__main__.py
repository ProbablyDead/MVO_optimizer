from src.functions.test_functions import get_functions
from src.mvo.MVO_optimizer import MVO_optimizer
from src.gui.App import AppMainScreen

app = AppMainScreen(get_functions(), MVO_optimizer)
app.start_app()
