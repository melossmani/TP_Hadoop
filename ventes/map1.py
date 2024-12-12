import sys

# Mapper for counting purchases by category

for line in sys.stdin:
    # Cleaning and splitting the input data
    data = line.strip().split("\t")

    # Check if the line has the expected number of columns
    if len(data) == 6:
        # Unpack the data into variables
        date, time, store, item, cost, payment = data

        # Assuming 'item' represents the category of purchase
        # Output the category and a count of 1 for each purchase
        print("{0}\t1".format(item))
