# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In program, I created a list that contains all the cells with length of 2. Now, unitlist is iterated to find naked twins. How did this happened? If two cells have same value and are in same column, row or square units then it is identified as Naked Twins. Once it is identified, we will iterate through the same unit to remove the numbers from other cells. Remember to remove individual characters, not the whole string. For example, if '23' is naked twins. Remove '2' and '3' separately. If you start replacing '23' then strings like '379' will be skipped.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In this case, we have take care that numbers shouldn't be repeated in diagonal cells. We have two diagonals for a sudoku. One starts from left top, I called it left_diagonal and other from right top, I called it right_diagonal. To do a Diagonal Sudoku, we can an additional constraint in 'eliminate' and 'only choice' functions. I created two lists, 'left_diagonal' and 'right_diagonal'. These two lists are used to identfied diagonal constraints. In case of elimination, I added these two list along with iteration of peer iteration. To work with only choice function, I created a new 'updateunitlist' with both right and left diagonals. This small changes makes the 'only_choice' work.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

