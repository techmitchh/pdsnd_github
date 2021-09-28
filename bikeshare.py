import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Global Variables
selected_month = ""
selected_city = ""
selected_day = ""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_input = False
    month_input = False
    day_input = False
    cities = ['chicago', 'new york', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    
    while not city_input:
        city = input(f"What city would you like to see data for: {', '.join(cities)}?: \n").lower()
        if city not in cities:
            print("Sorry your input was not correct. Please input Chicago, New York, Washington ")
        else:
            global selected_city
            selected_city += city
            city_input = True

    while not month_input:
        month = input(f"Which month would you like to filter by: {', '.join(months)}? \n").lower()
        if month not in months:
            print("Sorry your input was not correct. Please input the correct month ")
        else:
            global selected_month
            selected_month += month
            month_input = True

    while not day_input:
        day = input(f"What day would you like data for: {', '.join(days)}? \n").lower()
        if day not in days:
            print("Sorry your input was not correct. Please input the correct day ")
        else:
            global selected_day
            selected_day += day
            day_input = True

    print('-'*40)
    print(city, month, day + "\n")
    
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
    try:
        df = pd.read_csv(CITY_DATA[city])
        
        df['Start Time'] = pd.to_datetime(df['Start Time'])     # convert the Start Time column to datetime
        df['month'] = df['Start Time'].dt.month                 # extract month and day of week from Start Time to create new columns
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        df['hour'] = df['Start Time'].dt.hour
    
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june'] # use the index of the months list to get the corresponding int
            month = months.index(month) + 1
        
            df = df[df['month'] == month] # filter by month to create the new dataframe

            

        if day != 'all': # filter by day of week if applicable
            days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
            day = days.index(day)
            df = df[df['day_of_week'] == day] # filter by day of week to create the new dataframe

        print(f"Getting results for {city.title()}")
        return df
       
    except Exception as e:
        print(f"Exception error occured in Load Data: {e}")


def time_stats(df): 
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - loads users input from load_data function

    Returns:
        prints most common month, week, day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
        global selected_month
        global selected_day

        # Months
        months = ['january', 'february', 'march', 'april', 'may', 'june'] 
        max_month = df['month'].value_counts().idxmax() # Counts months, then pulls month with most counts
        common_month = months[max_month - 1] 
        
        # Days
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        max_day = df['day_of_week'].value_counts().idxmax() # Gets most common day of week
        common_day = days[max_day]

        # Hours
        common_hour = df['hour'].value_counts().idxmax() # Gets most common start hour
        

        if selected_month == 'all':
            print(f"The most common month is ({max_month}){common_month.title()}") # Display the most common month
        else:
            print(f"You selected month: ({max_month}){common_month.title()}")

        if selected_day == 'all':
            print(f"The most common day of the week is ({max_day}){common_day.title()}")
        else:
            print(f"You selected day: ({max_day}){common_day.title()}")
        
        print(f"The most common hour is {common_hour}")

    except Exception as e:
        print(f"Exception error occured in Time Stats: {e}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return df


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    try:
        common_ststation = df['Start Station'].value_counts() # Display most commonly used start station
        print("The most common Start Station is...\n{}\n\n".format(common_ststation.head(1)))
        
        common_enstation = df['End Station'].value_counts() # Display most commonly used end station
        print("The most common End Station is...\n{}\n\n".format(common_enstation.head(1)))
        
        start_endstation = df.groupby(['Start Station'])['End Station'].value_counts() # Display most frequent combination of start station and end station trip
        print("The most frequent station combination is...")
        print(start_endstation.head(1))

    except Exception as e:
        print(f"Exception error occured in Station Stats: {e}")
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        total_time = df['Trip Duration'].sum() # Display total travel time
        print(f"{round(total_time)}: Total time in minutes\n")
        
        avg_time = df['Trip Duration'].mean() # Display mean travel time
        print(f"{round(avg_time)}: Avg Trip Duration in minutes")
    except Exception as e:
        print(f"Exception occurred in Trip Duration Stats: {e}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    global selected_city

    
    try:
        count_user = df['User Type'].value_counts() # Display counts of user types
        print("Counts of User Types...")
        print(f"{count_user}\n\n")
        

        if selected_city != 'washington'.lower(): # Washington does not have Gender nor Birth information
            count_gender = df['Gender'].value_counts() # Gender Count
            print("Count of Gender...") 
            print(f"{count_gender}\n\n")

            earliest_birth = df['Birth Year'].min() # Display earliest, most recent, and most common year of birth
            recent_birth = df['Birth Year'].max()
            common_birth = df['Birth Year'].value_counts().idxmax()

            print(f"The earliest birth year is {earliest_birth}\
                The most recent bith year is {recent_birth}\
                The most common birth year is {common_birth}")

    except Exception as e:
        print(f"Exception occured in User Stats: {e}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw(df):
    """Displays option to view 5 rows of Raw Data"""
    start_time = time.time()
    view = False
    start_loc = 0
    end_loc = 5
    correct_selection = ['yes', 'no']
    try:
        while not view:
            select_view = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
            if select_view not in correct_selection:
                print("Sorry your input was not correct. Please input yes or no ")
            else:
                view = True

        while view:
            if select_view == 'no':
                break
            elif select_view == 'yes':
                data_sort = df.sort_values(by=['Start Time'])
                data_rows = data_sort.iloc[start_loc:end_loc]
                print(data_rows) # Print 5 rows of data
                view_display = input('Do you wish to continue?: ').lower()
                if view_display not in correct_selection:
                    print("Please input yes or no")
                    if view_display == 'yes':
                        continue
                if view_display == 'yes': # If yes df.iloc adjusts by 5
                    start_loc += 5
                    end_loc += 5
                    continue
                elif view_display == 'no':
                    break
    except Exception as e:
        print(f"Exception occured at View Raw: {e}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    global selected_month
    global selected_day
    global selected_city
    correct_selection = ['yes', 'no']
    select_restart = True
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw(df)
        
        while select_restart:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart not in correct_selection:
                print("Sorry your input was not correct. Please input yes or no ")
            else:
                select_restart = False
        
        if restart != 'no':
            selected_month = ""
            selected_city = ""
            selected_day = ""
            continue
        else:
            break



if __name__ == "__main__":
	main()
