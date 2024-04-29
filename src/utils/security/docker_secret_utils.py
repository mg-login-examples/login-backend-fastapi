import os


def load_from_run_secrets(name: str) -> str | None:
    path = f"/run/secrets/{name}"
    if not os.path.exists(path):
        return None

    with open(path, "r") as secret_file:
        return secret_file.read().strip()
