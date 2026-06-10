from pathlib import Path
import json

from config import MEMORY_DIR

# ------------------------------
# Profile Selection
# ------------------------------

profile_id = input("Enter profile name: ").strip()

memory_file = Path(MEMORY_DIR) / f"{profile_id}.json"

# ------------------------------
# Load Existing Profile
# ------------------------------

if memory_file.exists():

    with open(
        memory_file,
        "r",
        encoding="utf-8"
    ) as f:

        memory_data = json.load(f)

    print(
        f"\nLoaded "
        f"{len(memory_data['messages'])} "
        f"previous messages for '{profile_id}'"
    )

# ------------------------------
# Create New Profile
# ------------------------------

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

    print(
        f"\nCreated new profile '{profile_id}'"
    )

# ------------------------------
# Runtime Variables
# ------------------------------

chat_history = memory_data["messages"]
current_tone = memory_data["tone"]