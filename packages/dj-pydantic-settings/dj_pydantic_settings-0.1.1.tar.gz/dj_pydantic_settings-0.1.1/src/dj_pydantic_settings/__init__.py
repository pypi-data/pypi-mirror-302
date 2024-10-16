import inspect
import dj_database_url
from pydantic import AliasGenerator, BaseModel, ConfigDict, model_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict

alias_generator = AliasGenerator(serialization_alias=str.upper)


class DjangoModel(BaseModel):
    """
    Базовая модель для настроек. Так как в django конфигурация осуществляется путём определения констант
    в модуле settings, удобно иметь модель, которая сама переводит ключи в верхний регистр. Также это удобно для
    словарей TEMPLATES, REST_FRAMEWORK и т.п.
    """

    model_config = ConfigDict(alias_generator=alias_generator)


class Database(BaseModel):
    """
    Параметры подключения к базе данных. Основано на параметрах функции dj_database_url.parse
    """

    url: str
    engine: str | None = None
    conn_max_age: int | None = 0
    conn_health_checks: bool = False
    disable_server_side_cursors: bool = False
    ssl_require: bool = False
    test_options: dict | None = None

    @model_serializer
    def serialize(self) -> dj_database_url.DBConfig:
        return dj_database_url.parse(**{field: value for field, value in self})


class DjangoSettings(BaseSettings):
    """
    Базовый класс для настроек django-проекта
    """

    model_config = SettingsConfigDict(alias_generator=alias_generator)

    def __init__(self, **values):
        super().__init__(**values)
        self._set_globals()

    def _set_globals(self, offset=2) -> None:
        """
        Заполняет содержимым модели глобальные переменные модуля, в котором вызван

        offset по умолчанию 2, потому что при предполагаемом использовании метода стэк выглядит так:
            0. DjangoSettings._set_globals
            1. DjangoSettings.__init__
            2. <settings module>
        """
        stack = inspect.stack()
        settings_module_frame = stack[offset].frame
        settings_module_frame.f_locals.update(self.model_dump(by_alias=True))
