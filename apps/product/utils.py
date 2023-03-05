import uuid as uuid_lib


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
