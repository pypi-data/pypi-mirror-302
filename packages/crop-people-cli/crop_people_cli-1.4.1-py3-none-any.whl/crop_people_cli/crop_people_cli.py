import typer
from crop_people_cli.commands.single import app as single_app
from crop_people_cli.commands.multi import app as multi_app
from loguru import logger
import sys
from pathlib import Path

app = typer.Typer()

app.add_typer(single_app, name="single")
app.add_typer(multi_app, name="multi")

# Setup loguru logger
config_dir = Path.home() / ".config" / "crop_people_cli"
log_dir = config_dir / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "crop_people_cli.log"

logger.remove()  # Remove default handler
logger.add(log_file, rotation="10 MB", level="DEBUG", format="{time} {level} {message}")
logger.add(sys.stderr, level="ERROR")  # Only log errors to console

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        raise typer.Exit(code=1)
