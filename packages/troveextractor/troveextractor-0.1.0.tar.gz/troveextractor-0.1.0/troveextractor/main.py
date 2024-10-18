def greet(name: str) -> str:
    """Return a greeting message for the given name.

    Args:
        name (str): The name to greet.

    Returns:
        str: A greeting message.

    Raises:
        ValueError: If the name is empty.
    """
    if not name:
        raise ValueError("Name cannot be empty.")
    return f"Hello, {name}!"
