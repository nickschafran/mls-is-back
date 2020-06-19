MLS is Back Predictions
=======================

This is an R script to generate predictions for who will win the group stage
of the [MLS is Back](https://www.mlssoccer.com/mls-is-back-tournament)
tournament using 
[FiveThirtyEight's Global Club Soccer Rankings](https://projects.fivethirtyeight.com/global-club-soccer-rankings/).
More details on the tournament can be found 
[here](https://www.mlssoccer.com/mls-is-back-tournament/tournament-structure).

Instructions
------------
Everything to run the script and reproduce the output is available in the repo
except for the FiveThirtyEight data, which can be found 
[here](https://data.fivethirtyeight.com/#soccer-spi). 

For practice, it's implemented in both python and R.

You can run the python script from the command line by running 
`$ python mls_is_back.py`. It will also write the results to a file named
`mls_is_back.csv`. Pandas is required as specified in `requirements.txt`.

You can run the R script from the command line by running 
`$ R < mls_is_back.R --no-save`. It will write the results to a file named
`mls_is_back.csv`. The tidyr and dplyr packages are required.
