import sqlite3

file_path = 'stephen_king_adaptations.txt'
stephen_king_adaptations_list = []

with open(file_path, 'r') as file:
    for line in file:
        stephen_king_adaptations_list.append(line.strip().split(','))

conn = sqlite3.connect('stephen_king_adaptations.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table 
             (movieID TEXT PRIMARY KEY, movieName TEXT, movieYear INTEGER, imdbRating REAL)''')
c.executemany('INSERT INTO stephen_king_adaptations_table VALUES (?, ?, ?, ?)', stephen_king_adaptations_list)

conn.commit()

# User interaction loop
while True:
    print("Please select an option:")
    print("1. Search by movie name")
    print("2. Search by movie year")
    print("3. Search by movie rating")
    print("4. Stop")
    
    choice = input("Your choice: ")
    
    if choice == "1":
        movie_name = input("Enter the movie name: ")
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (movie_name,))
        result = c.fetchone()
        if result:
            print(f"Movie details: ID: {result[0]}, Name: {result[1]}, Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No such movie exists in our database.")

    elif choice == "2":
        movie_year = int(input("Enter the movie year: "))
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (movie_year,))
        results = c.fetchall()
        if results:
            for result in results:
                print(f"Movie details: ID: {result[0]}, Name: {result[1]}, Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No movies were found for that year in our database.")

    elif choice == "3":
        movie_rating = float(input("Enter the minimum IMDB rating: "))
        c.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (movie_rating,))
        
        results = c.fetchall()
        if results:
            for result in results:
                print(f"Movie details: ID: {result[0]}, Name: {result[1]}, Year: {result[2]}, IMDB Rating: {result[3]}")
        else:
            print("No movies at or above that rating were found in the database.")

    elif choice == "4":
        print("Program has stopped.")
        break

    else:
        print("Invalid choice, please choose again.")

conn.close()
