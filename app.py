import random
import string
import time

# ====================================================
# MODULE 1: SECRET CODE TRANSLATOR
# ====================================================
def get_random_chars():
    return ''.join(random.choices(string.ascii_lowercase, k=3))

def encode_message(message):
    words = message.split(" ")
    new_words = []
    for word in words:
        if len(word) >= 3:
            modified = word[1:] + word[0]
            new_words.append(get_random_chars() + modified + get_random_chars())
        else:
            new_words.append(word[::-1])
    return " ".join(new_words)

def decode_message(cipher):
    words = cipher.split(" ")
    new_words = []
    for word in words:
        if len(word) < 3:
            new_words.append(word[::-1])
        else:
            inner = word[3:-3]
            new_words.append(inner[-1] + inner[:-1])
    return " ".join(new_words)

def run_translator():
    while True:
        print("\n--- ENIGMA CRYPTOGRAPHY ---")
        print("1. Encrypt Text")
        print("2. Decrypt Code")
        print("3. Back to Main Menu")
        choice = input("Select Option (1-3): ")
        
        if choice == "1":
            msg = input("Enter message to hide: ")
            print("Secret Code:", encode_message(msg))
        elif choice == "2":
            msg = input("Enter code to crack: ")
            print("Original Text:", decode_message(msg))
        elif choice == "3":
            break

# ====================================================
# MODULE 2: LIBRARY MANAGEMENT (CRUD)
# ====================================================
class Library:
    def __init__(self):
        self.books = []
        
    def add(self, name):
        self.books.append(name)
        print(f"Book '{name}' added to catalog.")
        
    def show(self):
        if not self.books:
            print("Library is currently empty.")
        else:
            print("\n--- LIBRARY CATALOG ---")
            for i, b in enumerate(self.books, 1):
                print(f"{i}. {b}")
                
    def delete(self, name):
        if name in self.books:
            self.books.remove(name)
            print(f"Book '{name}' has been deleted.")
        else:
            print("Error: Book not found.")

def run_library():
    lib = Library()
    while True:
        print("\n--- CENTRAL LIBRARY SYSTEM ---")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Show All Books")
        print("4. Back to Main Menu")
        choice = input("Select Option (1-4): ")
        
        if choice == "1":
            book_name = input("Enter Book Name: ")
            lib.add(book_name)
        elif choice == "2":
            del_name = input("Enter name of book to delete: ")
            lib.delete(del_name)
        elif choice == "3":
            lib.show()
        elif choice == "4":
            break

# ====================================================
# MODULE 3: SNAKE-WATER-GUN BATTLE
# ====================================================
def run_game():
    options = ['s', 'w', 'g']
    names = {'s': 'SNAKE', 'w': 'WATER', 'g': 'GUN'}
    while True:
        print("\n--- SNAKE-WATER-GUN GAME ---")
        user = input("Choose (s) Snake, (w) Water, (g) Gun or (q) to Quit: ").lower()
        
        if user == 'q':
            break
        if user not in options:
            print("Invalid input! Try again.")
            continue
        
        comp = random.choice(options)
        print(f"Computer: {names[comp]} | You: {names[user]}")
        
        if comp == user:
            print("Result: It's a Tie!")
        elif (comp == 's' and user == 'g') or (comp == 'g' and user == 'w') or (comp == 'w' and user == 's'):
            print("Result: YOU WIN!")
        else:
            print("Result: YOU LOSE!")

# ====================================================
# MAIN CORE COMMANDER HUB
# ====================================================
def main_hub():
    while True:
        print("\n=============================================")
        print("       🌟 THE GIANT PYTHON HUB V1.0 🌟")
        print("=============================================")
        print("Please select a module:")
        print("1. Enigma Translator")
        print("2. Library Management")
        print("3. Snake-Water-Gun Game")
        print("4. Shutdown System")
        
        choice = input("\nEnter Choice (1-4): ")

        if choice == "1":
            run_translator()
        elif choice == "2":
            run_library()
        elif choice == "3":
            run_game()
        elif choice == "4":
            print("\nShutting down system. Goodbye.")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_hub()
