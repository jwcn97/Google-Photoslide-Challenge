# Google-Photoslide-Challenge

1. Store the list of tuples slide_i and slide_j in a dictionary with scores as the key
2. Dictionary is sorted (and always going to be searched) from highest to lowest
2. Take two nodes with the highest score and keep searching for slides with high transitions to the head and tail in decreasing order of score
3. Clear the cache periodically every 1000 to speed up the search