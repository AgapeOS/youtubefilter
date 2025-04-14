import json

OLD_HANDLES_PATH = "data/handles.json"
NEW_HANDLES_PATH = "data/new_handles.json"

def load_all_handles_from_old(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    handles = set()
    for group in data.values():
        handles.update(group)
    return handles

def load_all_handles_from_new(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    handles = set()
    for category in data.values():
        for age_group in category.values():
            handles.update(age_group)
    return handles

def main():
    old_handles = load_all_handles_from_old(OLD_HANDLES_PATH)
    new_handles = load_all_handles_from_new(NEW_HANDLES_PATH)

    missing = sorted(old_handles - new_handles)

    if missing:
        print("🔍 The following handles are missing from new_handles.json:\n")
        for handle in missing:
            print(f"  - {handle}")
    else:
        print("✅ No missing handles. All @handles from handles.json are present in new_handles.json.")

if __name__ == "__main__":
    main()
