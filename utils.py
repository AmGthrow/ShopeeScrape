from urllib.parse import quote
import json

def URLEncodeQuery(**kwargs):
    """Encodes kwarg values to URL-friendly strings
    Ex. query="Redmi Phone" => {'query': 'Redmi%20Phone'}

    Returns:
        dict: object containing kwargs and URL-encoded kwarg values
    """
    for kwarg in kwargs:
        kwargs[kwarg] = quote(str(kwargs[kwarg]))
    return kwargs

def get_queries_from_config(config_path: str='config.json') -> [dict]:
    return json.load(open(config_path))['search_queries']