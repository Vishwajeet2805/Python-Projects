import pandas as pd
import os
from datetime import datetime

# Function to input movie/web series details
def input_media_data():
    title = input("Enter title: ")
    media_type = input("Is this a Movie or Web Series? (Enter 'movie' or 'web series'): ").strip().lower()
    genre = input(f"Enter genre for {title}: ")
    release_year = int(input(f"Enter release year for {title}: "))
    director = input(f"Enter director for {title}: ")
    rating = float(input(f"Enter rating (1-10) for {title}: "))

    # If it's a web series, ask for additional details
    seasons = episodes = None
    if media_type == 'web series':
        seasons = int(input(f"Enter number of seasons for {title}: "))
        episodes = int(input(f"Enter number of episodes for {title}: "))

    return {
        "Title": title,
        "Type": media_type.capitalize(),
        "Genre": genre,
        "Release Year": release_year,
        "Director": director,
        "Rating": rating,
        "Seasons": seasons if media_type == 'web series' else None,
        "Episodes": episodes if media_type == 'web series' else None,
        "Date Added": datetime.now().strftime("%Y-%m-%d")
    }

# Function to save movie/web series data to CSV
def save_to_csv(media_data, filename='media_collection.csv'):
    if not os.path.isfile(filename):
        # If the file doesn't exist, write header
        df = pd.DataFrame([media_data])
        df.to_csv(filename, index=False)
    else:
        # Append new data to the CSV
        df = pd.DataFrame([media_data])
        df.to_csv(filename, mode='a', header=False, index=False)

# Function to display the media collection
def display_media_collection(filename='media_collection.csv'):
    df = pd.read_csv(filename)
    print("\nMedia Collection:")
    print(df)

# Function to analyze the media data
def analyze_media_data(filename='media_collection.csv'):
    df = pd.read_csv(filename)

    # Average rating of all movies and web series
    avg_rating = df["Rating"].mean()
    print(f"\nAverage Media Rating: {avg_rating:.2f}/10")

    # Number of movies and web series
    media_count = df["Type"].value_counts()
    print("\nMedia Type Count (Movies vs Web Series):")
    print(media_count)

    # List media by a specific genre
    genre_filter = input("\nEnter a genre to filter media by: ")
    filtered_media = df[df["Genre"].str.contains(genre_filter, case=False)]
    print(f"\nMedia in the genre '{genre_filter}':")
    print(filtered_media)

    # List media by type (Movie or Web Series)
    media_type_filter = input("\nEnter a media type to filter by (Movie/Web Series): ").strip().lower()
    filtered_by_type = df[df["Type"].str.lower() == media_type_filter]
    print(f"\nList of {media_type_filter.capitalize()}s:")
    print(filtered_by_type)

# Main function
def main():
    print("Welcome to the Movie and Web Series Collection Organizer!")

    while True:
        # Input media data (movie or web series)
        media_data = input_media_data()

        # Save media data to CSV
        save_to_csv(media_data)

        # Ask the user if they want to add another media entry
        another = input("Do you want to add another media item? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    # Display the media collection
    display_media_collection()

    # Analyze the media data after all data is entered
    analyze_media_data()

# Run the main function
if __name__ == "__main__":
    main()
