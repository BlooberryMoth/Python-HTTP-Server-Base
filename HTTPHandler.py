from Main import Server
import json


def handle_GET_request(url: list[str], parameters: dict) -> tuple[int, list[tuple[str, str]], str]:
    file_name, file_format, *_ = url[-1].split('.') + [""]
    if file_format:
        try:
            with open(f'./http/{"/".join(url)}') as file_in: file = file_in.buffer.read()
            return 200, [], file
        except: return Server.fourohfour
    else:
        try:
            with open(f'./http/{"/".join(url)}/index.html') as file_in: index = file_in.buffer.read()
            return 200, [("Content-Type", "text/html")], index
        except: return Server.fourohfour
    

def handle_POST_request(data: bytes) -> tuple[int, list[tuple[str, str]], str]:
    try: data = json.loads(data.decode())
    except: return error(400, "Invalid body form.")
    try: method = data['method']
    except: return error(400, "No method provided.")

    match method:
        case _: return error(400, "Unknown method.")

def error(status: int, reason: str): return status, [("Content-Type", "application/json")], json.dumps({"error": status, "reason": reason})