class IncorrectXmlFileException(Exception):
    def __init__(self):
        super().__init__('Incorrect xml file')
