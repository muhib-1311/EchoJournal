import os

def search_entries(keyword):
    journal_dir = os.path.join(os.path.dirname(__file__), "journal_entries")
    if not os.path.exists(journal_dir):
        print("📂 No journal entries folder found.")
        return

    found = False
    for filename in os.listdir(journal_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(journal_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                if keyword.lower() in content.lower():
                    print(f"\n🔎 Found in {filename}:\n------------------")
                    print(content.strip())
                    found = True

    if not found:
        print("❌ No matching entries found.")

if __name__ == "__main__":
    keyword = input("🔍 Enter a word to search in journal entries: ").strip()
    if keyword:
        search_entries(keyword)
    else:
        print("⚠️ Please enter a valid keyword.")
