import json
from datetime import datetime
import matplotlib
import statistics
from scipy.stats import ttest_1samp
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from collections import defaultdict

with open("lastfmstats-ronaldjmcinnes.json", "r", encoding="utf-8", errors="replace") as file:
    data = json.load(file)

# Create a dictionary to store  counts per date
_counts = defaultdict(int)

try:
    #data = json.loads(file)  # Parse the JSON data

    # Create a dictionary to store  counts per date
    _counts = defaultdict(int)

    # Iterate through the scrobbles
    for scrobble in data["scrobbles"]:
        # Convert milliseconds to seconds
        timestamp_seconds = scrobble["date"] // 1000
        # Convert timestamp to date (YYYY-MM-DD format)
        date = datetime.utcfromtimestamp(timestamp_seconds).strftime("%Y-%m-%d")
        # Increment the count for this date
        _counts[date] += 1

    # Print the results
    for date, count in _counts.items():
        print(f"Date: {date}, songs Played: {count}")

    song_count = []
    total_scrobbles = 0;
    day_count = 0;
    for count in _counts.items():
        total_scrobbles += int(count[1]);
        song_count.append(int(count[1]));
        day_count += 1;
    print(f"Total Scrobbles: {total_scrobbles}")

    """
    # POPULATION STATISTICS
    mean = statistics.mean(song_count)
    variance = statistics.variance(song_count)
    standard_deviation = statistics.stdev(song_count)
    print(f"\n\nAverage Scrobbles per Day: {mean}")
    """

    """*******************SAMPLE*******************"""
    sample_list = []
    for x in range(0, 50):
        sample_list.append(random.choice(song_count))
    samp_song_total = 0
    for y in range(0,50):
        samp_song_total += sample_list[y]
    print(sample_list)

    # SAMPLE STATISTICS
    samp_mean = statistics.mean(sample_list)
    samp_variance = statistics.variance(sample_list)
    samp_standard_deviation = statistics.stdev(sample_list)
    print(f"\nSample Standard Deviation: {samp_standard_deviation}")
    print(f"\n\nAverage Scrobbles per Day (IN SAMPLE): {samp_mean}\n")

    # Create the bar graph (population)
    plt.bar(range(len(song_count)), song_count)
    plt.title("Scrobble Counts over Last Four Years")
    plt.xlabel('Days')
    plt.ylabel('Number of Scrobbles')
    plt.show()

    poll_data = [21,
                15,
                120,
                81,
                35,
                50,
                60,
                47,
                32,
                57]
    poll_mean = statistics.mean(poll_data)
    print(f"\nThe mean of the poll data: {poll_mean}")

    t_statistic, p_value = ttest_1samp(sample_list, popmean=poll_mean)
    print(f"***STATISTICS***\nt-value: {t_statistic}\np-value: {p_value}")

    # Create the bar graph (sample)
    plt.bar(range(len(sample_list)),sample_list)
    plt.title("Random Sample of 50 Days' Scrobble Counts")
    plt.axhline(y=mean, color='r', linestyle='--',label=f'average scrobbles per day: {samp_mean}')
    plt.xlabel('Sample')
    plt.ylabel('Scrobbles')
    plt.legend()
    plt.show()

except json.JSONDecodeError as e:
    print(f"Invalid JSON syntax: {e}")
