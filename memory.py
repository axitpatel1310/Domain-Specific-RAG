from pathlib import Path
import json

from config import MEMORY_DIR


def load_profile(profile_id):

    memory_file = (
        Path(MEMORY_DIR)
        / f"{profile_id}.json"
    )

    if memory_file.exists():

        with open(
            memory_file,
            "r",
            encoding="utf-8"
        ) as f:

            memory_data = json.load(f)

    else:

        memory_data = {
            "tone": "1",
            "messages": []
        }

        with open(
            memory_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memory_data,
                f,
                indent=4,
                ensure_ascii=False
            )

    return memory_file, memory_data


def save_profile(
    memory_file,
    memory_data
):

    with open(
        memory_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            memory_data,
            f,
            indent=4,
            ensure_ascii=False
        )