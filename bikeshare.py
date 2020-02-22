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
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please specify which city you want to analyze (Chicago, New York City or Washington): ")
    city = city.lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("We do not recognize the city you entered, please enter either Chicago, New York City or Washington: ")
        city = city.lower()
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Please specify which month you want to analyze (January, February, March, April, May, June or All): ")
    month = month.lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input("We do not recognize the month you entered, please enter either January, February, March, April, May, June or All: ")
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please specify which day you want to analyze (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All): ")
    day = day.lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        day = input("We do not recognize the day you entered, please enter either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All: ")
        day = day.lower()

    print('\n' + '-'*40)
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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def raw_data(df):
    """Displays raw data."""
    
    answer = input('\nDo you want to display raw data (yes or no): ')
    answer = answer.lower()
    x = 0
    y = 5
    while answer == 'yes':
        print(df[x:y])
        x += 5
        y += 5
        answer = input('\nDo you want to continue displaying raw data (yes or no): ')
        answer = answer.lower()
        while answer != 'yes' and answer != 'no':
            answer = input('\nWe do not recognize the answer you entered, please enter yes or no: ')
            answer = answer.lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_mode = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_name = months[month_mode - 1].capitalize()
    print('The most common month is {}'.format(month_name)) 

    # TO DO: display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print('The most common day is {}'.format(day_mode)) 
    
    # TO DO: display the most common start hour
    hours = df['Start Time'].dt.hour
    hour_mode = hours.mode()[0]
    print('The most common start hour is {}'.format(hour_mode)) 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is {}'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is {}'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' and ' + df['End Station']
    combination = df['Start and End Station'].mode()[0]
    print('The most frequent combination of start station and end station trip is {}'.format(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_type = df.groupby(['User Type']).count()
    num_subscriber = count_user_type['Start Time']['Subscriber']
    num_customer = count_user_type['Start Time']['Customer']
    print('The count of subscribers is {} and the count of customers {}'.format(num_subscriber, num_customer))


    # TO DO: Display counts of gender
    if city == 'chicago' or city == 'new york city':
        count_gender = df.groupby(['Gender']).count()
        num_female = count_gender['Start Time']['Female']
        num_male = count_gender['Start Time']['Male']
        print('The count of females is {} and the count of males {}'.format(num_female, num_male))
    else:
        print('There is no gender data for Washington')
        
    # TO DO: Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth is {}'.format(int(earliest_yob)))
        most_recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is {}'.format(int(most_recent_yob)))
        most_common_yob = df['Birth Year'].mode().iat[0]
        print('The most common year of birth (or one of them) is {}'.format(int(most_common_yob)))
    else:
        print('There is no year of birth data for Washington')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
