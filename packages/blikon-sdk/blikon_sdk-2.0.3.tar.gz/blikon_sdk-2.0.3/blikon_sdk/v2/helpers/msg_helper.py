from googletrans import Translator
from blikon_sdk.v2.models.sdk_configuration_model import SDKConfiguration
from blikon_sdk.v2.core.core import Core


SOURCE_LANGUAGE = "en"


def msg(text: str) -> str:
    sdk_configuration: SDKConfiguration = Core.get_sdk_configuration()
    translator = Translator()
    traduccion: str = text
    try:
        app_language = sdk_configuration.sdk_settings.client_application_language
        if app_language != SOURCE_LANGUAGE:
            result = translator.translate(text, src=SOURCE_LANGUAGE, dest=app_language)
            traduccion = result.text
    except Exception as e:
        pass
    return traduccion

