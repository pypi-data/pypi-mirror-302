import cv2
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts.progress_bar import formatters
from prompt_toolkit.completion import PathCompleter, WordCompleter
import typer
from ultralytics import YOLO
from loguru import logger

app = typer.Typer()


def get_model_path():
    home = Path.home()
    yolo_dir = home / "yolov8"
    models = list(yolo_dir.glob("*.pt"))
    if models:
        model_names = [m.name for m in models]
        completer = WordCompleter(model_names)
        selected_model = prompt("Select a model: ", completer=completer)
        return str(yolo_dir / selected_model)
    else:
        return prompt("Enter path to YOLO model: ", completer=PathCompleter())


@app.command()
def run(
    margin_percentage: int = typer.Option(
        3, help="Margin percentage for bounding box (0-10)"
    ),
    model_size: int = typer.Option(640, help="Model size (320, 640, or 1280)"),
    model: str = typer.Option(None, help="YOLO model to use"),
    recursive: bool = typer.Option(False, help="Search for images recursively"),
):
    try:
        if model is None:
            model = get_model_path()

        # Load the YOLO model
        yolo_model = YOLO(model)
        yolo_model.fuse()  # Fuse the model for better performance

        input_dir = Path(prompt("Select Input Directory: ", completer=PathCompleter()))
        if not input_dir.is_dir():
            typer.echo("Invalid directory, exiting...")
            raise typer.Exit()

        output_dir = input_dir / "cropped"
        output_dir.mkdir(parents=True, exist_ok=True)

        image_pattern = "**/*.jpg" if recursive else "*.jpg"
        images_paths = list(input_dir.glob(image_pattern))
        typer.echo(f"Found {len(images_paths)} images to process.")

        def process_image(img_path):
            image = cv2.imread(str(img_path))
            if image is None:
                return False

            # Detect objects in the image
            results = yolo_model(image, imgsz=model_size, verbose=False)[0]

            # Filter for person class (usually class 0 in COCO dataset)
            person_boxes = results.boxes[results.boxes.cls == 0]

            if len(person_boxes) == 0:
                (output_dir / "no-person" / img_path.name).parent.mkdir(
                    parents=True, exist_ok=True
                )
                cv2.imwrite(str(output_dir / "no-person" / img_path.name), image)
                return False

            processed = False
            for i, box in enumerate(person_boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                margin_x = int((x2 - x1) * margin_percentage / 100)
                margin_y = int((y2 - y1) * margin_percentage / 100)

                x1, y1 = max(0, x1 - margin_x), max(0, y1 - margin_y)
                x2, y2 = (
                    min(image.shape[1], x2 + margin_x),
                    min(image.shape[0], y2 + margin_y),
                )
                cropped_image = image[y1:y2, x1:x2]

                if cropped_image.shape[0] * cropped_image.shape[1] < 360 * 360:
                    continue

                output_path = output_dir / img_path.relative_to(input_dir).with_stem(
                    f"{img_path.stem}_cropped_person_{i}"
                )
                output_path.parent.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(output_path), cropped_image)
                processed = True

            return processed

        # Catppuccin Mocha inspired style
        style = Style.from_dict(
            {
                "label": "bg:#f5e0dc #1e1e2e",
                "percentage": "bg:#f5e0dc #1e1e2e",
                "bar-a": "#cba6f7",
                "bar-b": "#f38ba8",
                "bar-c": "#585b70",
                "current": "#a6e3a1",
                "total": "#89dceb",
                "time-elapsed": "#fab387",
                "time-left": "#89b4fa",
            }
        )

        custom_formatters = [
            formatters.Label(),
            formatters.Text(": [", style="class:percentage"),
            formatters.Percentage(),
            formatters.Text("]", style="class:percentage"),
            formatters.Text(" "),
            formatters.Bar(sym_a="█", sym_b="█", sym_c="░"),
            formatters.Text("  "),
            formatters.Progress(),
            formatters.Text("  "),
            formatters.Text("elapsed: ", style="class:time-elapsed"),
            formatters.TimeElapsed(),
            formatters.Text(" eta: ", style="class:time-left"),
            formatters.TimeLeft(),
        ]

        title = HTML('<style bg="#cba6f7" fg="#1e1e2e">Processing Images</style>')

        with ProgressBar(style=style, formatters=custom_formatters, title=title) as pb:
            processed_count = 0
            for img_path in pb(images_paths, label="Processing"):
                if process_image(img_path):
                    processed_count += 1

        failed_count = len(images_paths) - processed_count

        typer.echo(
            f"\nProcessing finished! Successfully processed {processed_count} images. Failed to process {failed_count} images."
        )
        typer.echo(
            f"Images with no person detected or all crops too small: {failed_count}"
        )
        typer.echo("These images have been saved in the 'no-person' subdirectory.")
    except Exception as e:
        logger.error(f"An error occurred in multi command: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
