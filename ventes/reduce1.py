from operator import itemgetter
import sys

current_item = None
current_count = 0
item = None

# Reducer for counting purchases by category

for line in sys.stdin:
    # Cleaning and splitting the input data
    line = line.strip()
    item, count = line.split("\t", 1)

    # Convert count (currently a string) to an integer
    try:
        count = int(count)
    except ValueError:
        # Ignore/discard this line if the count is not a valid integer
        continue

    # If the current item is the same as the new item, increment the count
    if current_item == item:
        current_count += count
    else:
        # If the item changes, output the result for the previous item
        if current_item:
            print("{0}\t{1}".format(current_item, current_count))
        # Set the new current item and reset the count
        current_item = item
        current_count = count

# Output the result for the last item
if current_item:
    print("{0}\t{1}".format(current_item, current_count))
