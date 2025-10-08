from xml.etree import ElementTree
from uuid import uuid4

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.application.constructor.dto import (
    Edge, NodeDto, ParsedDto,
    TreeEdgeDto, TreeNodeDto,
    TgBotCallbackDto, TgBotStartDto, TgBotCommandsDto
)


class XmlParserService:

    @staticmethod
    def parse(xml_content) -> ParsedDto:
        def _validate_xml_parsed_data(data: ParsedDto) -> ParsedDto:
            none_nodes: list[NodeDto] = []
            for node in data.nodes:
                none_nodes.append(node)
                for edge in data.edges:
                    if node.id in (edge.target, edge.source):
                        none_nodes.pop()
                        break

            for node in none_nodes:
                data.nodes.remove(node)

            index = 0
            for i in range(len(data.edges)):
                if data.edges[i].value is None:
                    data.edges[i].value = none_nodes[index].value
                    index += 1

            return data

        root = ElementTree.fromstring(xml_content)
        nodes = root.findall('.//mxCell[@vertex="1"]')
        edges = root.findall('.//mxCell[@edge="1"]')

        return _validate_xml_parsed_data(
            ParsedDto(
                nodes=[
                    NodeDto(
                        id=node.get('id'),
                        value=node.get('value')
                    ) for node in nodes
                ],
                edges=[
                    Edge(
                        id=edge.get('id'),
                        value=edge.get('value'),
                        source=edge.get('source'),
                        target=edge.get('target')
                    ) for edge in edges
                ]
            )
        )


class TreeService:

    @staticmethod
    def _find_main_node(data: ParsedDto) -> NodeDto:
        target_nodes_id = set(edge.target for edge in data.edges if edge.target is not None)
        for node in data.nodes:
            if node.id not in target_nodes_id:
                return node
        return data.nodes[0]

    def _build_tree(self, main_node_id: str, data: ParsedDto) -> TreeNodeDto:
        tree: TreeNodeDto | None = None
        for node in data.nodes:
            if node.id == main_node_id:
                tree = TreeNodeDto(
                    value=node.value,
                    elements=None
                )
                break

        for edge in data.edges:
            if edge.source == main_node_id:
                if tree.elements is None:
                    tree.elements = []
                tree.elements.append(
                    TreeEdgeDto(
                        value=edge.value,
                        element=self._build_tree(edge.target, data),
                    )
                )

        return tree

    def create_tree(self, data: ParsedDto) -> TreeNodeDto:
        return self._build_tree(
            main_node_id=self._find_main_node(data).id,
            data=data
        )


class ConstructorService:

    def create_config(self, data: TreeNodeDto) -> TgBotCommandsDto:
        start_callbacks = []
        start_keyboard = []
        start_father_callback = str(uuid4())
        for element in data.elements:
            start_callbacks.append(str(uuid4()))
            start_keyboard.append(
                InlineKeyboardButton(text=element.value, callback_data=start_callbacks[-1])
            )
        start_keyboard = InlineKeyboardMarkup(inline_keyboard=[start_keyboard[::-1]]).model_dump()

        callback_commands = self._build_callbacks(
            father_callback=start_father_callback,
            edges=data.elements,
            callbacks=start_callbacks,
            commands={}
        )
        return TgBotCommandsDto(
            start=TgBotStartDto(
                text=data.value,
                reply_markup=start_keyboard,
                callback=start_father_callback
            ),
            callbacks=callback_commands
        )

    def _build_callbacks(
            self,
            edges: list[TreeEdgeDto],
            callbacks: list[str],
            commands: dict[str, TgBotCallbackDto],
            father_callback: str
    ):
        if edges is None:
            return {}
        new_callbacks, callbacks_commands, father_callbacks = self._register_handler(edges, callbacks, father_callback)
        commands.update(callbacks_commands)
        for edge, callbacks, father_callback in zip(edges, new_callbacks, father_callbacks):
            commands.update(self._build_callbacks(edge.element.elements, callbacks, commands, father_callback))
        return commands

    @staticmethod
    def _register_handler(
            edges: list[TreeEdgeDto],
            callbacks: list[str],
            father_callback: str
    ) -> tuple[
        list[list[str]],
        dict[str, TgBotCallbackDto],
        list[str]
    ]:
        new_callbacks = []
        callback_commands = {}
        father_callbacks = []

        for edge, callback in zip(edges, callbacks):
            keyboard = []
            edge_node_edges_callbacks = []

            if edge.element.elements is not None:
                for item in edge.element.elements:
                    edge_node_edges_callbacks.append(str(uuid4()))
                    keyboard.append(InlineKeyboardButton(
                        text=item.value, callback_data=edge_node_edges_callbacks[-1]
                    ))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                keyboard[::-1],
                [
                    InlineKeyboardButton(
                        text='‹ Назад',
                        callback_data=father_callback
                    )
                ]
            ]).model_dump()

            new_callbacks.append(edge_node_edges_callbacks)
            father_callbacks.append(callback)

            callback_commands[callback] = TgBotCallbackDto(
                text=edge.element.value,
                reply_markup=keyboard

            )

        return new_callbacks, callback_commands, father_callbacks
