from collections.abc import Callable
from filecmp import cmp
from functools import cached_property
from os import unlink
from os.path import join as path_join
from pathlib import Path
from shutil import move
from tempfile import NamedTemporaryFile
from typing import Any

from jinja2 import BaseLoader, Environment, TemplateNotFound
from yaml import safe_load

from ..configuring.paths import Paths
from ..configuring.settings import Settings


class AbsoluteLoader(BaseLoader):
    def get_source(
        self, environment: Environment, template: str
    ) -> tuple[str, str, Callable[[], bool]]:
        template_path = Path(template)
        if not template_path.exists():
            raise TemplateNotFound(template)
        mtime = template_path.stat().st_mtime
        source = template_path.read_text(encoding="utf8")
        return (
            source,
            str(template_path),
            lambda: mtime == template_path.stat().st_mtime,
        )


class Renderer:
    def __init__(self, paths: Paths, settings: Settings):
        self._paths = paths
        self._settings = settings

    def render(
        self, *, template_path: Path, output_path: Path, **template_kwargs: Any
    ) -> None:
        template = self._env.get_template(str(template_path))
        try:
            with NamedTemporaryFile("w", encoding="utf8", delete=False) as fh:
                fh.write(template.render(**template_kwargs))
                fh.write("\n")
            if not output_path.exists() or not cmp(fh.name, str(output_path)):
                move(fh.name, output_path)
        finally:
            try:
                unlink(fh.name)
            except FileNotFoundError:
                pass

    @cached_property
    def _env(self) -> Environment:
        env = Environment(
            loader=AbsoluteLoader(),
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\V{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
        )
        env.filters["camelcase"] = self._to_camel_case
        env.filters["path_join"] = lambda paths: path_join(*paths)
        env.filters["image"] = self._img
        return env

    def _to_camel_case(self, string: str) -> str:
        return "".join(substring.capitalize() or "_" for substring in string.split("_"))

    def _img(
        self, value: str, modifier: str = "", scale: float = 1.0, lang: str = "fr"
    ) -> str:
        metadata_path = (self._paths.shared_dir / Path(value)).with_suffix(".yml")
        if metadata_path.exists():
            metadata = safe_load(metadata_path.read_text(encoding="utf8"))

            def get_en_or_fr(key: str) -> str:
                if lang != "fr":
                    key_en = f"{key}_en"
                    return metadata[key_en] if key_en in metadata else metadata[key]
                else:
                    return metadata[key]

            title = self._settings.default_img_values.title.get_default(
                get_en_or_fr("title"), lang
            )
            author = self._settings.default_img_values.author.get_default(
                get_en_or_fr("author"), lang
            )
            license = self._settings.default_img_values.license.get_default(
                get_en_or_fr("license"), lang
            )
            info = f"[{title}, {author}, {license}.]"
        else:
            info = ""

        return f"\\img{modifier}{info}{{{value}}}{{{scale:.2f}}}"
