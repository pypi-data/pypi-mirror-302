import os
from pathlib import Path
from typing import Optional



def ask(prompt: str, valid_answers: Optional[list[str]] = None, default_index=-1):
    """Ask the user for input.

    Args:
        prompt (str): Question for the user
        valid_answers (list[str], optional): A list of valid responses. Defaults to list().
        default_index (int, optional): Used if the user does not enter anything. Defaults to -1.

    Returns:
        _type_: _description_
    """
    default_answer = None
    if valid_answers:
        if default_index is not None:
            default_answer = valid_answers[default_index]
            if len(valid_answers) > 1:
                valid_answers[default_index] = default_answer.upper()
    else:
        valid_answers = []

    while True:
        valid_answers_str = f" ({'/'.join(valid_answers)})" if valid_answers else ""
        answer = input(f"{prompt}{valid_answers_str}: ")
        if default_answer:
            if answer == "" or answer == default_answer.upper():
                return default_answer
        if valid_answers and answer not in valid_answers:
            continue
        return answer


def create_desktop_file_content() -> str:
    """Create a valid .desktop file.
    e.g.:
        #!/usr/bin/env xdg-open
        [Desktop Entry]
        Version=1.0
        Type=Application
        Terminal=false
        Exec=/snap/bin/skype
        Name=Skype
        Comment=Skype
        Icon=/snap/skype/101/meta/gui/skypeforlinux.png
    """

    is_term = str(ask("Show the console?", ["y", "n"]) == "y").lower()
    name = ask("Name?")
    path = os.path.expanduser(ask("Path?"))
    icon = ask("Icon?")

    return f"""#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal={is_term}
Exec={path}
Name={name}
Comment=
Icon={icon}
"""


def save_desktop_file(content: str):
    """Write the content to a file requested by the user.

    Args:
        content (str): File content.
    """

    while True:
        dir_path = ask("Where would you like to save it? ", ["~/.local/share/applications"])
        dir_path = os.path.expanduser(dir_path)
        name = ask("What would you like to call it?")
        path = Path(dir_path, name)
        if path.exists():
            if ask("Overwrite existing file?", ["y","n"]) != "y":
                continue  # try again
        break  # use this path

    with open(path, "w", encoding="UTF-8") as fh:
        fh.write(content)


if __name__ == "__main__":
    contents = create_desktop_file_content()
    print(contents)
    save_desktop_file(contents)
