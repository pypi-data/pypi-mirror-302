from pathlib import Path

import typer
from amsdal.manager import AmsdalManager
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.utils.classes import import_class
from amsdal_utils.utils.text import to_snake_case
from rich import print

from amsdal_cli.app import app
from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.text import rich_info
from amsdal_cli.utils.text import rich_success


@app.command(name='restore, rst')
def restore_command(
    ctx: typer.Context,
    *,
    config: Path = typer.Option(None, help='Path to custom config.yml file'),  # noqa: B008
) -> None:
    """
    Restores the models JSON schemas to /src directory from the database.

    Args:
        ctx (typer.Context): The Typer context object.
        config (Path, optional): Path to custom config.yml file.

    Returns:
        None
    """
    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR

    app_source_path.mkdir(exist_ok=True)

    build_app(
        app_source_path=app_source_path,
        config_path=config or cli_config.config_path,
        output=Path('.'),
    )

    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.register_internal_classes()

    print(rich_info('Reading classes...'))
    class_object_model = import_class('models.core.class_object.ClassObject')
    class_objects = class_object_model.objects.filter(  # type: ignore[attr-defined]
        _address__class_version=Versions.LATEST,
        _address__object_version=Versions.LATEST,
        _metadata__is_deleted=False,
        _metadata__class_schema_type=SchemaTypes.USER,
    ).execute()

    print(f'[yellow]Found {len(class_objects)} classes...[/yellow]')

    for class_object in class_objects:
        class_name = class_object.object_id
        model_path = app_source_path / 'models' / to_snake_case(class_name) / 'model.json'
        print(rich_info(f'Restoring {class_name}...'), end=' ')
        model_path.parent.mkdir(exist_ok=True)
        model_path.write_text(class_object.class_schema)
        print(rich_success('Restored!'))

    print()
    print(rich_success('Done! All classes are restored.'))
