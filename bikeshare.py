import time
import pandas as pd
import numpy as np
from os import system, name
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_mapping = { 'jan': 1,
                  'feb': 2,
                  'mar': 3,
                  'apr': 4,
                  'may': 5,
                  'jun': 6,
                  'all': 'all' }

day_mapping = { 'all': 'all',
                'mon': 'monday',
                'tue': 'tuesday',
                'wed': 'wednesday',
                'thu': 'thursday',
                'fri': 'friday',
                'sat': 'saturday',
                'sun': 'sunday' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_input_city = 1
    valid_input_filter = 1
    
    city = ''
    month_filter = ''
    day_filter = ''
    
    while valid_input_city:
        city = input('Which city\'s data would you like to explore out of Chicago, New York City, or Washington? \n').lower()
        if city in CITY_DATA:
            valid_input_city = 0
        else:
            print('\nCity not available right now :(, please try again...', end = '\n')
    

    # TO DO: get user input for month (all, january, february, ... , june)
    while valid_input_filter:
        
        filter_input = input('\nWould you like to apply filters on month, day, both, or none? \n')
    
        if filter_input.lower() == 'both':
            month_filter = list(input('\nPlease select the month(s) out of All, Jan, Feb, Mar, Apr, May, and Jun: \n').split(' '))
        
            # Check if entered values are valid as per data. 
            for mon in month_filter:
                
                if mon.lower() not in month_mapping:
                    print('\nIncorrect month filters selected, please choose valid filters...')
                    break
            else:
                day_filter = list(input('\nPlease select the day(s) out of All, Mon, Tue, Wed, Thu, Fri, Sat, and Sun: \n').split(' '))
        
                for day in day_filter:
                    if day.lower() not in day_mapping:
                        print('\nIncorrect day filters selected, please choose valid filters...')
                        break
                    else:
                        valid_input_filter = 0
                
        elif filter_input.lower() == 'month':
            month_filter = list(input('\nPlease select the month(s) out of All, Jan, Feb, Mar, Apr, May, and Jun: \n').split(' '))
            for mon in month_filter:
                if mon.lower() not in month_mapping:
                    print('\nIncorrect month filters selected, please choose valid filters...')
                    break
            else:
                valid_input_filter = 0
        
        elif filter_input.lower() == 'day':
            day_filter = list(input('\nPlease select the day(s) out of All, Mon, Tue, Wed, Thu, Fri, Sat, and Sun: \n').split(' '))
        
            for day in day_filter:
                
                if day.lower() not in day_mapping:
                    print('\nIncorrect day filters selected, please choose valid filters...')
                    break
                else:
                    valid_input_filter = 0
                
        else:
            print('\nNo filter selected, analyzing complete data...')
            valid_input_filter = 0
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*40)
    return city, month_filter, day_filter


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

    # Convert Start Time and End Time to datetime type. Derive new columns for Month Number, Weekday, and Hour
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Start Month'] = df['Start Time'].dt.month
    df['End Month'] = df['End Time'].dt.month
    df['Start Day'] = df['Start Time'].dt.weekday_name
    df['End Day'] = df['End Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    df['End Hour'] = df['End Time'].dt.hour
    
    # Filter the dataframe based on the filters selected

    if month != '':
        for i in range(len(month)):
            month[i] = month_mapping[month[i].lower()]
    if day != '':
        for i in range(len(day)):
            day[i] = day_mapping[day[i].lower()]
    
    if 'all' not in month and month!='':
        df = df[df['Start Month'].isin(month)]
    
    if 'all' not in day and day != '':
        df = df[df['Start Day'].str.lower().isin(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Start Month'].mode()[0]
    month_distribution_count = df['Start Month'].value_counts()
    
    print('Most Common Month for bike sharing is: {}.'.format(calendar.month_name[common_month]), end = '\t')
    print('\tCount: {}'.format(month_distribution_count[common_month]))

    # TO DO: display the most common day of week
    common_day = df['Start Day'].mode()[0]
    day_distribution_count = df['Start Day'].value_counts()
    
    print('Most Common Day for bike sharing is: {}.'.format(common_day), end = '\t')
    print('\tCount: {}'.format(day_distribution_count[common_day]))

    # TO DO: display the most common start hour
    common_hour = df['Start Hour'].mode()[0]
    hour_distribution_count = df['Start Hour'].value_counts()
    
    print('Most Common Hour for bike sharing is: {}.'.format(common_hour), end = '\t')
    print('\tCount: {}'.format(hour_distribution_count[common_hour]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    print('Most Commonly Used Start Station is: {}.'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('Most Commonly Used End Station is: {}.'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('Most Frequent Start Station and End Station combination is:\n{}.'.format((df['Start Station'] + '\n' + df['End Station']).mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Travel Time: {} seconds.'.format(np.sum(df['Trip Duration'])))

    # TO DO: display mean travel time
    print('Average Travel Time: {} seconds.'.format(np.mean(df['Trip Duration'])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(city, df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    unique_user_type = df['User Type'].unique()
    user_type_count = df['User Type'].value_counts()
    
    for user in unique_user_type:
        print('Count of {}: {}'.format(user, user_type_count[user]))


    # Check if the city is New York City or Chicago and print Gender and Birth Year Stats as well

    if city.lower() in ['new york city', 'chicago']:
        
            
        # TO DO: Display counts of gender
        
        print('\nCalculating Gender Stats...\n')
        
        unique_gender = df['Gender'].dropna().unique()
        gender_distribution = df['Gender'].value_counts()
        
        for gender in unique_gender:
            print('Count of {}: {}'.format(gender, gender_distribution[gender]))

        # TO DO: Display earliest, most recent, and most common year of birth
        
        print('\nCalculating Birth Year Stats...\n')
        
        earliest_yob = int(np.min(df['Birth Year']))
        recent_yob = int(np.max(df['Birth Year']))
        common_yob = int(df['Birth Year'].mode()[0])
        
        print('Earliest Year of Birth is: {} \t Count: {}'.format(earliest_yob, df['Birth Year'].value_counts()[earliest_yob]))
        print('Most Recent Year of Birth is: {} \t Count: {}'.format(recent_yob, df['Birth Year'].value_counts()[recent_yob]))
        print('Most Common Year of Birth is: {} \t Count: {}'.format(common_yob, df['Birth Year'].value_counts()[common_yob]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def clear_screen():
    """ clear console after a restart is requested"""
    
    if name == 'ns':
        _ = system('cls')
    else:
        _ = system('clear')
    
    return
        
def print_data(start, stop, df):
    """Print data from file, 5 rows at a time."""
    
    print(df.iloc[start:stop, :])
    continue_print = input('\nWould you like to print next 5 rows (yes/no)?').lower()
    if continue_print == 'yes':
        print_data(start + 5, stop + 5, df)
    elif continue_print != 'no':
        print('\nNo valid input received...')
    else:
        return
    return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        start = 0
        stop = 5
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(city, df)
        
        print_data_rows = input('Would you like to print first 5 rows of data (yes/no)? ')
        if print_data_rows.lower() == 'yes':
              print_data(start, stop, df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            return
        else:
            clear_screen()
            main()


if __name__ == "__main__":
    main()