from pydantic import BaseModel
from yaml import safe_load

from ..exceptions import DeckzException
from .paths import GlobalPaths


class LocalizedValues(BaseModel):
    fr: dict[str, str] = {}
    en: dict[str, str] = {}
    all: dict[str, str] = {}

    def get_default(self, value: str, lang: str) -> str:
        if lang == "fr" and value in self.fr:
            return self.fr[value]
        if lang == "en" and value in self.en:
            return self.en[value]
        return self.all[value] if value in self.all else value


class DefaultImageValues(BaseModel):
    license: LocalizedValues = LocalizedValues()
    author: LocalizedValues = LocalizedValues()
    title: LocalizedValues = LocalizedValues()


class Settings(BaseModel):
    build_command: list[str]
    default_img_values: DefaultImageValues = DefaultImageValues()

    @classmethod
    def from_global_paths(cls, global_paths: GlobalPaths) -> "Settings":
        if not global_paths.settings.is_file():
            raise DeckzException(
                f"Could not find settings file at {global_paths.settings}."
            )
        return cls.model_validate(
            safe_load(global_paths.settings.read_text(encoding="utf8"))
        )
