import yaml


def get_yaml_text(
        file_path: str,
        *keys: str,
        default: str = 'Текст'
) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        result = data
        for key in keys:
            result = result.get(key)
            if result is None:
                return default
        return result
    except FileNotFoundError:
        return default
    except Exception:
        return default


