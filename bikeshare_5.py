import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago','new york city','washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june','all']
    days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

    city = input("Enter city  from these chicago,new york city,washington : ").lower()
    while city not in cities:
        city =  input("wrong city, Enter city: ").lower()

    month = input("Enter months of january, february, march, april, may, june, all: ").lower()
    while month not in months:
        month = input("wrong month, Enter month: ").lower()

    day = input("Enter day of sunday, monday , tuesday, wednesday, thursday, friday, saturday, all: ").lower()
    while day not in days:
        day =  input("wrong day, Enter day: ").lower()
    


    print('-'*40)
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

    # load the data
    df = pd.read_csv(CITY_DATA[city])

    # convert the start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract data
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_freq_month = df['month'].mode()[0]
    print('Most Popular Month:', most_freq_month)

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Day Of Week:', common_day_of_week)

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("Most commonly start Station: ", popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("Most used end station: ", popular_end_station)

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    most_freq_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print("Most frequent combination of the Start Station and End Station trip:\n", most_freq_combination_station)

    print("\nThis took %s seconds. " % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel time: ", total_travel_time)

    # display mean travel time
    mean_time_travel = df['Trip Duration'].mean()
    print("Mean travel time: ", mean_time_travel)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:', df['User Type'].value_counts())

    # washington doesn't have gender status and throws an exception:
    try:
        # Display counts of gender
        print('Gender Stats:', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)
        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year:',most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print('Most Common Year:',most_common_year)
    except KeyError as ke:
        print('\nWashington doens\'t have a gender stats\n', ke)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):

    #Show 5 records from the selected city.
    #Asks user to type if he wants to show raw data or no
    print('\nRaw Data Is Ready To Show\n')
    i = 0
    while True:
        user_input = input('Do You Like To Show The Row Data, please, Type :  Yes , No\n').strip().lower()
        if user_input == 'no':
            print('\nMany Thanks')
            break
        elif user_input == 'yes':
                print(df[i:i+5])
                i+=5
                print("\nDo You Need See More 5 Raws?\n")
        else:
            print(user_input)
            print('That is not a rigt answer')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
