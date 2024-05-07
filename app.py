from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import bcrypt
import sqlite3

# Initialize chatbot
chatbot = ChatBot('MyChatBot')
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot
trainer.train('chatterbot.corpus.english')

# SQLite3 database connection
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT, email TEXT)''')
conn.commit()

def register():
    print("Please enter your details to register:")
    username = input("Username: ")
    email = input("Email: ")
    password = input("Password: ")

    # Hash the password before storing
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Store user details in database
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, hashed_password, email))
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

def login():
    print("Please login with your credentials:")
    username = input("Username: ")
    password = input("Password: ")

    # Retrieve user details from database
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        print("Login successful!")
        return True
    else:
        print("Invalid username or password.")
        return False

def password_recovery():
    print("Password Recovery:")
    username = input("Enter your username: ")
    email = input("Enter your email: ")

    # Retrieve user details from database
    c.execute("SELECT * FROM users WHERE username=? AND email=?", (username, email))
    user = c.fetchone()

    if user:
        # Send password to email or display it
        print(f"Your password is: {user[1]}")  # In a real-world scenario, this should be sent securely via email
    else:
        print("User not found or email does not match.")

def main():
    while True:
        print("\nWelcome to the ChatBot application!")
        print("1. Register")
        print("2. Login")
        print("3. Password Recovery")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            if login():
                # Start chatbot interaction
                while True:
                    user_input = input("You: ")
                    response = chatbot.get_response(user_input)
                    print("ChatBot:", response)
                    if user_input.lower() == 'exit':
                        break
        elif choice == '3':
            password_recovery()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close database connection
conn.close()
