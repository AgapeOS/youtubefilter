import subprocess

def run_script(name, args=[]):
    print(f"\n🔧 Running: {name} {' '.join(args)}")
    result = subprocess.run(["python", name, *args])
    if result.returncode != 0:
        print(f"❌ Failed: {name}")
        exit(1)
    print(f"✅ Finished: {name}")

def main():
    print("🌐 Starting AgapeOS YouTube Channel Refresh")

    # Step 1: Update channel info from handles
    print("Grabbing Channel Information")
    run_script("scripts/grab_channel_info.py")
    
    print("Step 2: Cache videos for each channel (incrementally)")
    run_script("scripts/cache_channel_videos.py")

    print("Step 3: Build channel HTML pages")
    run_script("scripts/generate_channel_pages.py")

    print("Step 4: Build all_videos.json (used for recommendations + video viewer)")
    run_script("scripts/generate_all_videos.py")

    print("Step 5: Build main index.html with approved channels")
    run_script("scripts/generate_channel_list.py")

    print("\n🎉 All done! Your static site is updated and ready.")

if __name__ == "__main__":
    main()
