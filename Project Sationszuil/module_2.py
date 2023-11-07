import psycopg2
import datetime

# Function to moderate messages and save to my PostgreSQL database
def moderate_and_save_messages():
    messages = [] # Creates an empty list to store the data of the messages

    # Opens the "messages.txt" file in reading mode
    with open("messages.txt", "r") as file:
        for line in file:
            # Splits each line into message, date_time, user_name, and station using a comma 
            data = line.strip().split(",")
            message, date_time, user_name, station = data[:4]
            # Asks for the moderator for approval of each message thats in the messages.txt file
            approved = input(f"Message: {message}\nApprove this message? (yes/no): ").lower() == "yes"
            # Prompts the moderator for their name and email
            moderator = input("Moderator name: ")
            moderator_email = input("Moderator email: ")
            # Gets the current date and time and formats it as a string
            review_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Appends the data of the messages, including approval and moderator information, to the list
            messages.append((message, date_time, user_name, station, approved, moderator, moderator_email, review_date_time))

    if messages:
        # Establishes a connection to my PostgreSQL database
        conn = psycopg2.connect(
            dbname="Stationzuil",
            user="postgres",
            password="Dibbel12",
            host="20.117.103.104",
            port="5432"
        )
        cur = conn.cursor() # Creates a cursor object for executing the SQL commands
        cur.executemany("""
            INSERT INTO messages (message, date_time, user_name, station, approved, moderator, moderator_email, review_date_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, messages)
        conn.commit() # Commits the changes to the database
        cur.close() # Closes the cursor
        conn.close() # Closes the database connection

    # Clears the contents of the "messages.txt" file
    open("messages.txt", "w").close()

if __name__ == "__main__":
    moderate_and_save_messages()