# by Richi Rod AKA @richionline / falken20
# ./my_chispas/__init__.py

from flask import Flask

from .config import get_settings
from .logger import Log, console

console.rule("My Chispas")
settings = get_settings()
Log.info(f"Settings: {settings}")

def create_app():
    app = Flask(__name__, 
                template_folder="../templates",
                static_folder="../docs")
    app.config['SECRET_KEY'] = settings.SECRET_KEY # TODO: Test with secret_key or SECRET_KEY
