import pandas as pd
import numpy as np
import time

CITY_OPTIONS = {
    1: 'chicago.csv',
    2: 'new_york_city.csv',
    3: 'washington.csv'
}

MONTH_FILTER = {
    1: 'january',
    2: 'february',
    3: 'march',
    4: 'april',
    5: 'may',
    6: 'june'
}

DAY_FILTER = {
    0: 'sunday',
    1: 'monday',
    2: 'tuesday',
    3: 'wednesday',
    4: 'thursday',
    5: 'friday',
    6: 'saturday'
}

def get_filters():
    city = ''
    while city not in CITY_OPTIONS:
        try:
            city_input = int(input("\nSelect a city to analyze (Type 1 - 3):\n1. Chicago\n2. New York City\n3. Washington\n"))
            city = CITY_OPTIONS.get(city_input)
            if not city:
                print("Invalid input. Invalid input. Please enter a number corresponding to the city (1 - 3).")
            else:
                break
        except ValueError:
            print("Invalid input. Invalid input. Please enter a number corresponding to the city (1 - 3).")

    # get user input for filter type (month, day, both, none)
    filter_type = input("Would you like to filter the data by month, day, both or none?\n").lower()
    while filter_type not in ['month', 'day', 'both', 'none']:
        print("Invalid filter type entered. Please only enter only 'month', 'day', 'both' or 'none'")
        filter_type = input("Would you like to filter the data by month, day, both or none? ").lower()

    # get user input for month (january - june)
    month = 'all'
    day = 'all'
    if filter_type in ['month', 'both']:
        while True:
            try:
                month_input = int(input("Which month of the data you want to view? (Type 1 - 6)\n1. January\n2. February\n3. March\n4. April\n5. May\n6. June\n"))
                month = month_input
                if month not in MONTH_FILTER:
                    print("Invalid input. Please enter the number corresponding to the month filters(1 - 6) that you want to view.")
                    continue
                if filter_type == 'both':
                    break
                else:
                    return city, month, day
            except ValueError:
                print("Invalid input. Please enter the number corresponding to the month filters(1 - 6) that you want to view.")

    # get user input for day of week (monday - sunday)
    if filter_type in ['day', 'both']:
        while True:
            try:
                day_input = int(input("Which day of the week of the data you want to view? (Type 0 - 6)\n0. Sunday\n1. Monday\n2. Tuesday\n3. Wednesday\n4. Thursday\n5. Friday\n6. Saturday\n"))
                day = day_input
                if day not in DAY_FILTER:
                    print("Invalid input. Please enter the number corresponding to the day filters(0 - 6) that you want to view.")
                    continue
                if filter_type == 'both':
                    break
                else:
                    return city, month, day
            except ValueError:
                print("Invalid input. Please enter the number corresponding to the day filters(0 - 6) that you want to view.")
    return city, month, day

def load_data(city):
    """
    Loads data for the specified city and returns a dataframe.
    """
    df = pd.read_csv(city)
    return df

def time_stats(df, month='all', day='all'):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    display_month_day(month, day)
    start_time = time.time()

    # Convert the 'Start Time' column to a datetime data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Filter by selected month if applicable
    if month != 'all':
        df = df[df['Start Time'].dt.month == month]

    # Filter by selected day if applicable
    if day !='all':
        df = df[df['Start Time'].dt.dayofweek == day]

    # display the most common month
    if month == 'all':
        common_month = df['Start Time'].dt.month.mode()[0]
        print("The most common month is:", MONTH_FILTER[common_month])
    else:
        print("Selected month:", MONTH_FILTER[month])

    # display the most common day of week
    if day == 'all':
        common_day = df['Start Time'].dt.dayofweek.mode()[0]
        print("The most common day of the week is:", DAY_FILTER[common_day])
    else:
        print("Selected day:", DAY_FILTER[day])

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    hour_count = df['Start Time'].dt.hour.value_counts()[common_hour]
    print("The most common start hour is:", common_hour, ". Count: ", hour_count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, month='all', day='all'):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    display_month_day(month, day)
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        df = df.loc[df['Start Time'].dt.month == month].copy()
    if day != 'all':
        df = df.loc[df['Start Time'].dt.dayofweek == day].copy()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_counts = df['Start Station'].value_counts()[start_station]
    print("The most commonly used start station is:", start_station, ". Count: ", start_station_counts)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_counts = df['End Station'].value_counts()[end_station]
    print("The most commonly used end station is:", end_station, ". Count: ", end_station_counts)

    # display most frequent combination of start station and end station trip
    df.loc[:, 'Route'] = df['Start Station'] + ' --> ' + df['End Station']
    popular_route = df['Route'].mode()[0]
    popular_route_counts = df['Route'].value_counts()[popular_route]
    print("The most popular trip is:", popular_route, ". Count: ", popular_route_counts)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df, month='all', day='all'):
    print('\nCalculating Trip Duration...\n')
    display_month_day(month, day)
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if month != 'all':
        df = df.loc[df['Start Time'].dt.month == month]
    if day != 'all':
        df = df.loc[df['Start Time'].dt.dayofweek == day]

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: ", format_time(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: ", format_time(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', gender_count)
    else:
        print("\nGender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest birth year: ', earliest_birth_year)
        print('Most recent birth year: ', most_recent_birth_year)
        print('Most common birth year: ', most_common_birth_year)
    else:
        print("\nBirth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def format_time(seconds):
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours > 0:
        return f"{hours} hours {minutes} minutes {seconds} seconds"
    else:
        return f"{minutes} minutes {seconds} seconds"


def display_month_day(month, day):
    selected = ''
    if month != 'all':
        selected += "Selected Month: {}".format(MONTH_FILTER[month])
    else:
        selected += 'Selected Months: All'
    
    if day != 'all':
        selected += " Selected Day: {}".format(DAY_FILTER[day])
    else:
        selected += " Selected Days: All"

    print('-'*50)
    print(selected)
    print('-'*50)

def main():
    while True:
    #Get city filters
        city, month, day = get_filters()

        df = load_data(city)

        # print time statistics
        time_stats(df, month, day)

        # print station statistics
        station_stats(df, month, day)

        # print trip duration statistics
        trip_duration_stats(df, month, day)

        # print user statistics
        user_stats(df)

        # Prompt the user for raw data
        while True:
            raw_data = input('\nWould you like to see raw data (5 rows)? Please enter yes or no.\n')
            if raw_data.lower() == 'yes':
                start = 0
                end = 5
                while end <= len(df.index) - 1:
                    print(df.iloc[start:end].to_json(orient='records', lines=True))
                    start += 5
                    end += 5
                    more_data = input('\nWould you like to see more raw data (Next 5 rows)? Enter yes or no.\n')
                    if more_data.lower() == 'no':
                        break
                if end >= len(df.index):
                    print(df.iloc[start:].to_json(orient='records', lines=True))
                    break
            elif raw_data.lower() == 'no':
                break
            else:
                print('Invalid input. Please enter "yes" or "no".')

        restart = ''
        while restart.lower() not in ['yes', 'no']:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() not in ['yes', 'no']:
                print('Invalid input. Please enter "yes" or "no".')
        if restart.lower() == 'no':
            break

if __name__ == "__main__":
    main()
