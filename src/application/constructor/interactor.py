from src.application.constructor.service import TreeService, XmlParserService, ConstructorService
from src.application.constructor.dto import TgBotCommandsDto
from src.application.constructor.exception import IncorrectXmlFileException


class BuildTgBotCommandsInteractor:

    def __init__(
            self,
            tree_service: TreeService = TreeService(),
            xml_parser_service: XmlParserService = XmlParserService(),
            constructor_service: ConstructorService = ConstructorService()
    ):
        self.tree_service = tree_service
        self.xml_parser_service = xml_parser_service
        self.constructor_service = constructor_service

    async def __call__(self, xml_content) -> TgBotCommandsDto:
        parsed_data = self.xml_parser_service.parse(xml_content)
        if not parsed_data.edges or not parsed_data.nodes:
            raise IncorrectXmlFileException()
        return self.constructor_service.create_config(
            data=self.tree_service.create_tree(parsed_data)
        )
