import base64
import uuid as uuid_lib
from typing import Any


def generate_unique_filename(filename: str) -> str:
    """
    Generate a filename for the given file.
    """
    name_parts = filename.split(".")

    extension = name_parts.pop()
    start_name = "".join(name_parts)
    uuid_str = uuid_lib.uuid4()

    unique_filename = f"{start_name}_{uuid_str}.{extension}"
    return unique_filename


def prep_file_data(logo_file: Any) -> dict:
    filename = generate_unique_filename(logo_file.name)
    mimetype = logo_file.content_type
    encoded_file = base64.b64encode(logo_file.read()).decode("utf-8")
    data = {"file": encoded_file, "name": filename, "mimetype": mimetype}
    return data
