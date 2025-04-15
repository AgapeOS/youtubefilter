import subprocess
import hashlib
import os

def run_script(name, args=[]):
    print(f"\n🔧 Running: {name} {' '.join(args)}")
    result = subprocess.run(["python", name, *args])
    if result.returncode != 0:
        print(f"❌ Failed: {name}")
        exit(1)
    print(f"✅ Finished: {name}")

def hash_file(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def check_for_new_handles():
    current_hash = hash_file("data/handles.json")
    hash_path = ".handles_hash"

    if os.path.exists(hash_path):
        with open(hash_path, "r") as f:
            previous_hash = f.read().strip()
    else:
        previous_hash = ""

    # Save new hash regardless
    with open(hash_path, "w") as f:
        f.write(current_hash)

    return current_hash != previous_hash

def auto_commit_push(full_project=False):
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if status.stdout.strip():
        if full_project:
            print("📦 Committing entire project...")
            subprocess.run(["git", "add", "."], check=True)
            commit_msg = input("📝 Commit message: ").strip() or "Auto-refresh: full project update"
        else:
            print("📂 Committing cached files only...")
            subprocess.run(["git", "add", "html/cached/"], check=True)
            commit_msg = "Auto-refresh: update all cached channel JSON files"

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
    else:
        print("📭 No changes to commit.")

def main():
    print("🌐 Starting AgapeOS YouTube Channel Refresh")

    needs_handle_update = check_for_new_handles()

    if needs_handle_update:
        print("🆕 Detected changes in handles.json.")
    else:
        print("✅ No changes detected in handles.json.")

    confirm = input("📥 Did you add or modify any handles and want to re-fetch channel info? (y/n): ").strip().lower()
    if confirm == "y":
        run_script("scripts/grab_channel_info.py")
    else:
        print("⏭️ Skipping channel info fetch.")

    print("📥 Step 2: Cache videos for each channel")
    run_script("scripts/cache_channel_videos.py")

    print("🎨 Step 3: Build channel HTML pages")
    run_script("scripts/generate_channel_pages.py")

    print("🗂️ Step 4: Build main index.html")
    run_script("scripts/generate_channel_list.py")

    print("\n🎉 All done! Your static site is updated and ready.")

    response = input("✅ Do you want to commit and push updated cached files to GitHub? (y/n): ").strip().lower()
    print("\n🛠 Git Commit Options:")
    print("  1. Cached files only")
    print("  2. Entire project")
    print("  3. Skip Git commit/push")
    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        auto_commit_push(full_project=False)
    elif choice == "2":
        auto_commit_push(full_project=True)
    else:
        print("🔁 Skipped Git commit/push.")

if __name__ == "__main__":
    main()
