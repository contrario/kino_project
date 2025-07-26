import os
import subprocess

def show_menu():
    print("\n🧠 Welcome to SmartFetcher + Analyzer Toolkit")
    print("1️⃣  Κατέβασε νέα δεδομένα KINO (SmartFetcher)")
    print("2️⃣  Ανάλυση δεδομένων KINO (SmartAnalyzer)")
    print("3️⃣  Έξοδος")

def main():
    while True:
        show_menu()
        choice = input("Επιλογή (1/2/3): ").strip()

        if choice == '1':
            print("\n🚀 Εκκίνηση SmartFetcher...\n")
            subprocess.run(["python", "smart_fetcher.py"], check=True)

        elif choice == '2':
            print("\n📈 Εκκίνηση SmartAnalyzer...\n")
            subprocess.run(["python", "smart_analyzer.py"], check=True)

        elif choice == '3':
            print("👋 Έξοδος από το εργαλείο.")
            break
        else:
            print("❌ Μη έγκυρη επιλογή. Δοκίμασε ξανά.")

if __name__ == "__main__":
    main()
2