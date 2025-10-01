import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


pd.set_option('display.max_columns', None)

def get_user_input(prompt, options):
    """Helper function to get validated user input."""
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return value
        else:
            print("Check your input, try again.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    cities = ['chicago', 'new york city', 'washington']
    city = get_user_input("Enter city (chicago, new york city, washington): ", cities)

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = get_user_input("Enter month (january to june) or 'all': ", months)

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = get_user_input("Enter day of week or 'all': ", days)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    # Load data from the CSV file corresponding to the selected city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract the month (as a number) from the 'Start Time' column
    df['month'] = df['Start Time'].dt.month

    # Extract the day of the week (as a string) from the 'Start Time' column
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if a specific month is selected (not 'all')
    if month != 'all':
        # List of valid months corresponding to the data set (January to June)
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # Convert the month name to its corresponding number (e.g., 'march' -> 3)
        month = months.index(month) + 1

        # Filter the DataFrame to include only rows with the selected month
        df = df[df['month'] == month]

    # Filter by day of week if a specific day is selected (not 'all')
    if day != 'all':
        # Capitalize the day name and filter the DataFrame accordingly
        df = df[df['day_of_week'] == day.title()]

    # Return the filtered DataFrame
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Find the most common month (numerical value from 1 to 6)
    common_month = df['month'].mode()[0]
    month_name = ['January', 'February', 'March', 'April', 'May', 'June']
    print("Most common month:", month_name[common_month - 1])

    # Find the most common day of the week (e.g., 'Monday', 'Tuesday')
    common_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", common_day)

    # Create a new column with the hour extracted from 'Start Time'
    df['hour'] = df['Start Time'].dt.hour

    # Find the most common hour when trips start
    common_hour = df['hour'].mode()[0]
    print("Most common start hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Find the most common starting station
    start_station = df['Start Station'].mode()[0]
    print("Most common start station:", start_station)

    # Find the most common ending station
    end_station = df['End Station'].mode()[0]
    print("Most common end station:", end_station)

    # Create a new column that combines start and end stations into a trip description
    df['trip'] = df['Start Station'] + " -> " + df['End Station']

    # Find the most frequent complete trip (start to end)
    common_trip = df['trip'].mode()[0]
    print("Most frequent trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the total travel time (sum of all trip durations)
    total_time = df['Trip Duration'].sum()
    print("Total travel time (seconds):", total_time)

    # Calculate the average travel time
    mean_time = df['Trip Duration'].mean()
    print("Average travel time (seconds):", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Print the counts of each user type (e.g., Subscriber, Customer)
    print("User Types:\n", df['User Type'].value_counts())

    # Check if the 'Gender' column exists in the DataFrame
    if 'Gender' in df.columns:
        # If it exists, print the count of each gender
        print("\nGender Counts:\n", df['Gender'].value_counts())
    else:
        # If the column is missing (e.g., for Washington), print a message
        print("\nNo gender data available for this city.")

    # Check if the 'Birth Year' column exists in the DataFrame
    if 'Birth Year' in df.columns:
        # Get the earliest birth year (minimum)
        earliest = int(df['Birth Year'].min())

        # Get the most recent birth year (maximum)
        latest = int(df['Birth Year'].max())

        # Get the most common birth year (mode)
        most_common = int(df['Birth Year'].mode()[0])

        # Print all birth year statistics
        print("\nEarliest birth year:", earliest)
        print("Most recent birth year:", latest)
        print("Most common birth year:", most_common)
    else:
        # If the column is missing, print a message
        print("No birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """ Printing raw data to console."""

    start_loc = 0
    view_data = input("Do you want to see the first 5 rows of raw data? (yes/no):").strip().lower()
    print("Data:\n")

    while view_data == 'yes' and start_loc < len(df):
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(df):
            print("No more data to display.")
            break

        answer = ['yes', 'no']
        while True:
            view_data = input("\nDo you want to see the next 5 rows of raw data? (yes/no):").strip().lower()
            if view_data in answer:
                break
            else:
                print("Check your input, try again.")
        print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()