# Google-Photoslide-Challenge

1. Data is stored in a dictionary (key: tag-count of slide, value: ID of slide) for fast retrieval
2. Take two slides with high score/tag count as head and tail of the slideshow
3. carry out the following while the slideshow is not completed:
  a. Loop through dictionary from highest to lowest tag-counts
  b. compute transition score of slides relative to the head and tail slide
  c. keep track of maximum scores and respective slides for each ends
  d. add a condition to break the loop when (tag-count > 2 x maximum score) because theretically, no slide with equal or lower tag counts is going to break the maximum score record
  e. append slides with maximum scores to head and tail of slideshow
  f. Remove the slide IDs from the dictionary
<br/>
*duration: 4 hours 40 minutes<br/>
*score: 409,226
