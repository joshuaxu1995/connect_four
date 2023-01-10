# connect_four

Testing design principles for creating a standard connect 4 board game. I wanted to make this code as modular as possible: adjustable to different grid dimensions, win conditions, and requirements on length of the sequence to win.

There are 2 main organizing units in this code.
* Game - the main execution engine for the connect 4 - handles the sequence of moves from the players. 
* Board - contains the mutable matrix data structure that holds the state of the board.

Seeking help on the following questions:
1. How would you design this if it were up to you?
2. I tried to use modular, substitutable functions as much as possible: for instance, notice the function `_check_direction` takes in 3 functions as parameters.
3. One alternative design pattern is to avoid mutability at all: instead of changing the structure of the board by adding pieces, what if we take a transformation f that maps f(old_board) => new_board. That takes on a more "functional" language approach - but we aren't use Ocaml or another functional language, so you would be sacrificing performance in aims of achieving immutability. Which approach do you prefer? 

I created a few very basic test cases to test for horizontal, vertical, and diagonal wins by various different players.