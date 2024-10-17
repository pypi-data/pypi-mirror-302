import os

import pytest
from mkdocs_puml.model import Count
from mkdocs_puml.storage import FileStorage, RAMStorage
from mkdocs_puml.plugin import PlantUMLPlugin, ThemeMode
from mkdocs_puml.puml import Fallback, PlantUML
from mkdocs_puml.theme import Theme
from tests.conftest import BASE_PUML_KEYWORD, CUSTOM_PUML_KEYWORD
from tests.plugins.conftest import is_uuid_valid, patch_plugin_to_single_theme


def test_on_config(plugin_config):
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml, PlantUML)
    assert isinstance(plugin.themer, Theme)
    assert isinstance(plugin.storage, RAMStorage)

    assert plugin.theme_light == "default/light"
    assert plugin.theme_dark == "default/dark"
    assert plugin.puml_keyword == BASE_PUML_KEYWORD
    assert "assets/mkdocs_puml/puml.css" in plugin_config["extra_css"]
    assert "assets/mkdocs_puml/puml.js" in plugin_config["extra_javascript"]

    assert "assets/mkdocs_puml/interaction.css" in plugin_config["extra_css"]
    assert "assets/mkdocs_puml/interaction.js" in plugin_config["extra_javascript"]


def test_on_config_theme_disabled(plugin_config):
    plugin = PlantUMLPlugin()
    plugin_config.theme.enabled = False
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml, PlantUML)
    assert plugin.themer is None

    assert plugin.theme_light is None
    assert plugin.theme_dark is None
    assert "assets/mkdocs_puml/puml.css" in plugin_config["extra_css"]
    assert "assets/mkdocs_puml/puml.js" in plugin_config["extra_javascript"]


def test_on_config_file_storage(plugin_config, patch_path_mkdir):
    plugin = PlantUMLPlugin()
    plugin.config = plugin_config
    plugin_config.cache.backend = "local"
    plugin_config.cache.local.load_dict({"path": "test"})

    plugin.on_config(plugin_config)

    assert isinstance(plugin.storage, FileStorage)


def test_on_config_interaction_disabled(plugin_config):
    plugin_config.interaction.enabled = False

    plugin = PlantUMLPlugin()
    plugin.config = plugin_config

    plugin.on_config(plugin_config)

    assert isinstance(plugin.puml, PlantUML)
    assert isinstance(plugin.themer, Theme)
    assert isinstance(plugin.storage, RAMStorage)

    assert plugin.theme_light == "default/light"
    assert plugin.theme_dark == "default/dark"
    assert plugin.puml_keyword == BASE_PUML_KEYWORD
    assert "assets/mkdocs_puml/puml.css" in plugin_config["extra_css"]
    assert "assets/mkdocs_puml/puml.js" in plugin_config["extra_javascript"]

    assert "assets/mkdocs_puml/interaction.css" not in plugin_config["extra_css"]
    assert "assets/mkdocs_puml/interaction.js" not in plugin_config["extra_javascript"]


def test_on_page_markdown_single_theme(plant_uml_plugin, md_lines):
    patch_plugin_to_single_theme(plant_uml_plugin)

    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.storage.items()) == 2

    for key in plant_uml_plugin.storage.keys():
        assert is_uuid_valid(key)

    for val in plant_uml_plugin.storage.schemes().values():
        assert "@startuml" in val and "@enduml" in val


def test_on_page_markdown_dual_themes(plant_uml_plugin, md_lines):
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert len(plant_uml_plugin.storage.keys()) == 4

    for key, val in plant_uml_plugin.storage.items():
        if val.mode == ThemeMode.LIGHT:
            assert is_uuid_valid(key)
        else:
            uuid_key, _, dark = key.rpartition("-")
            assert is_uuid_valid(uuid_key)
            assert dark == "dark"

    for val in plant_uml_plugin.storage.schemes().values():
        assert "@startuml" in val and "@enduml" in val


def test_on_page_markdown_custom_keyword(plant_uml_plugin, md_lines):
    # Test if PlantUML diagrams are correctly extracted with a custom keyword
    plant_uml_plugin.config.puml_keyword = CUSTOM_PUML_KEYWORD
    plant_uml_plugin.on_page_markdown("\n".join(md_lines))

    assert (
        len(plant_uml_plugin.storage.items()) == 4
    )  # 2 (light / dark) on each diagram


def test_on_env(mock_requests, plant_uml_plugin, diagrams_dict, plugin_environment):
    mock_requests(len(diagrams_dict))

    plant_uml_plugin.storage.data = diagrams_dict
    plant_uml_plugin.on_env(plugin_environment)

    for _, diagram in plant_uml_plugin.storage.items():
        assert diagram.diagram.startswith("<svg")


def test_on_env_fallback(
    mock_requests_fallback, plant_uml_plugin, diagrams_dict, plugin_environment
):
    mock_requests_fallback(len(diagrams_dict))

    plant_uml_plugin.storage.data = diagrams_dict
    plant_uml_plugin.on_env(plugin_environment)

    for _, diagram in plant_uml_plugin.storage.items():
        assert isinstance(diagram.diagram, Fallback)

    assert len(plant_uml_plugin.storage.invalid) == len(diagrams_dict)


def test_on_post_page(plant_uml_plugin, diagrams_dict, html_page):
    plant_uml_plugin.storage.data = diagrams_dict
    output = plant_uml_plugin.on_post_page(html_page.content, html_page)

    assert output.count('<div class="puml light" style="">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.LIGHT]
    )
    assert output.count('<div class="puml dark" style="">') == len(
        [True for v in diagrams_dict.values() if v.mode == ThemeMode.DARK]
    )


def test_on_post_build(tmp_path, plant_uml_plugin):
    # Test if static files are correctly copied during the build process
    config = {"site_dir": str(tmp_path)}
    dest_dir = tmp_path.joinpath("assets/mkdocs_puml")
    os.makedirs(dest_dir)

    plant_uml_plugin.on_post_build(config)

    assert dest_dir.joinpath("puml.css").exists()
    assert dest_dir.joinpath("puml.js").exists()

    assert dest_dir.joinpath("interaction.css").exists()
    assert dest_dir.joinpath("interaction.js").exists()


def test_on_post_build_with_subdirectory(tmp_path, plant_uml_plugin):
    # Test if the plugin correctly handles subdirectories in the static folder
    config = {"site_dir": str(tmp_path)}

    plant_uml_plugin.on_post_build(config)

    dest_dir = tmp_path.joinpath("assets/mkdocs_puml")
    assert dest_dir.joinpath("puml.css").exists()


@pytest.mark.parametrize(
    "fallback,count,expected",
    [
        (
            0,
            Count(1, 0),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 1 light diagram[/dim] [green bold]✔️[/green bold]",
        ),
        (
            0,
            Count(0, 1),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 1 dark diagram[/dim] [green bold]✔️[/green bold]",
        ),
        (
            0,
            Count(2, 0),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 2 light diagrams[/dim] [green bold]✔️[/green bold]",
        ),
        (
            0,
            Count(0, 2),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 2 dark diagrams[/dim] [green bold]✔️[/green bold]",
        ),
        (
            0,
            Count(1, 1),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 1 light and 1 dark diagrams[/dim] "
            "[green bold]✔️[/green bold]",
        ),
        (
            0,
            Count(0, 0),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: All diagrams loaded from cache"
            "[/dim] [green bold]✔️[/green bold]",
        ),
        (
            3,
            Count(3, 0),
            "[dim][bold magenta]mkdocs_puml[/bold magenta]: Built 3 light diagrams."
            "[/dim][bold red] 3 diagram failed to render ⨯[/bold red]",
        ),
    ],
)
def test_status_message(plant_uml_plugin, fallback, count, expected):
    msg = plant_uml_plugin._prepare_status_message(fallback, count)
    assert msg == expected
