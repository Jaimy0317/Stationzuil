import random
import datetime

# List of the available stations
stations = ["Amsterdam", "Arnhem", "Nijmegen"]

# A function that creates the message
def create_message(message, user_name, station):
    # Gets the current date and time in a Y-M-D H-M-S format thats suppported by PostGreSQL
    current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Formats the message with the provided information from this function
    return f"{message},{current_date_time},{user_name},{station}\n"

# A function that saves the message to the message.txt file
def save_message_to_txt(message):
    with open("messages.txt", "a") as file:
        # Open the messages.txt file in append mode and writes the message to the messages.txt file
        file.write(message)

print("Welcome! Please leave behind your experience of the station you're currently at")

while True:
    print("1. Submit a message")
    print("2. Exit")
    user_choice = input("Enter your choice: ")

    if user_choice == "1":
        message = input("Enter your message (max of 140 characters): ")[:140]
        user_name = input("Enter your name (leave it blank for an anonymous name): ")
        if not user_name:
            user_name = "Anoniem" #Sets an anonymous name if no username is provided
        station = random.choice(stations) # Randomly selects a station from the stations list
        
        # Creates the message 
        message = create_message(message, user_name, station)
        save_message_to_txt(message)
        print("Message submitted successfully.")

    elif user_choice == "2":
        print("Thank you for your review. Enjoy your day!")
        break # Exits the program 