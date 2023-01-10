from __future__ import annotations
import enum
import random
import itertools
from typing import List, Tuple


class GridState(enum.Enum):
    EMPTY = 0
    RED = 1
    BLACK = 2

    def __str__(state: GridState) -> str:
        if state is GridState.EMPTY:
            return "_"
        if state is GridState.RED:
            return "R"
        if state is GridState.BLACK:
            return "B"


class WinResult(enum.Enum):
    DID_NOT_WIN = 0
    WIN = 1
    NO_REMAINING_LOCATIONS = 2


class GameWinner(enum.Enum):
    DRAW = 0
    RED = 1
    BLACK = 2
    NOT_DONE = 3


class Game:
    def __init__(self, width: int, height: int, consecutive_to_win: int) -> None:
        self.board = Board(width, height, consecutive_to_win, generic_win_condition)
        self.max_columns = width

    # Ignore: I would've used this if I wanted an interactive input from user.
    # def play_game(self) -> GameWinner:
    #     color = GridState.RED
    #     while True:
    #         column = query_for_valid_column(self.board, self.max_columns)
    #         game_outcome = self.get_game_outcome(
    #             self.board.place_piece(column, color), color
    #         )
    #         if game_outcome is not GameWinner.NOT_DONE:
    #             return game_outcome
    #         color = Game.get_next_color(color)

    def get_game_outcome(self, result: WinResult, color: GridState) -> GameWinner:
        if result is WinResult.WIN:
            if color is GridState.RED:
                return GameWinner.RED
            elif color is GridState.BLACK:
                return GameWinner.BLACK
        elif result is WinResult.NO_REMAINING_LOCATIONS:
            return GameWinner.DRAW
        else:
            return GameWinner.NOT_DONE

    def play_move_sequence(
        self, move_sequence_1: List[int], move_sequence_2
    ) -> Tuple[GameWinner, int]:
        for index, (move1, move2) in enumerate(
            list(itertools.zip_longest(move_sequence_1, move_sequence_2))
        ):
            if not self.board.valid_location(move1):
                print(f"Move number: {index + 1} is not a valid move for color: RED")
            else:
                game_outcome = self.get_game_outcome(
                    self.board.place_piece(move1, GridState.RED), GridState.RED
                )
                print(
                    f"Printing board after move #: {index + 1} of red. Board: \n{self.board}"
                )
                if game_outcome is not GameWinner.NOT_DONE:
                    return game_outcome, index
            if move2 is None:
                print(f"Player 2 did not register a move for move: {index + 1}")
                break
            if not self.board.valid_location(move2):
                print(f"Move number: {index + 1} is not a valid move for color: BLACK")
            else:
                game_outcome = self.get_game_outcome(
                    self.board.place_piece(move2, GridState.BLACK), GridState.BLACK
                )
                print(
                    f"Printing board after move #: {index + 1} of black. Board: \n{self.board}"
                )
                if game_outcome is not GameWinner.NOT_DONE:
                    return game_outcome, index
        return GameWinner.NOT_DONE, len(move_sequence_1)

    @staticmethod
    def get_next_color(current_color: GridState) -> GridState:
        if current_color is GridState.RED:
            return GridState.BLACK
        else:
            return GridState.RED


def query_for_valid_column(board: Board, max_columns) -> int:
    while True:
        column = choose_column(max_columns)
        if board.valid_location(column):
            return column


def choose_column(width: int) -> None:
    return random.randint(0, width - 1)


class Board:
    def __init__(
        self, width: int, height: int, consecutive_to_win: int, win_condition: ...
    ) -> None:
        self.grid = [[GridState.EMPTY for _ in range(width)] for _ in range(height)]
        self.column_indices = [0] * width
        self.consecutive_to_win = consecutive_to_win
        self.win_condition = win_condition

    def place_piece(self, column_index: int, color: GridState) -> WinResult:
        self.grid[self.column_indices[column_index]][column_index] = color
        self.column_indices[column_index] += 1
        result = self.win_condition(
            self.grid, self.column_indices, column_index, color, self.consecutive_to_win
        )
        if result:
            return WinResult.WIN
        elif self.all_columns_full():
            return WinResult.NO_REMAINING_LOCATIONS
        return WinResult.DID_NOT_WIN

    def all_columns_full(self) -> bool:
        return all(
            [row_reached >= len(self.grid) for row_reached in self.column_indices]
        )

    def valid_location(self, column_index: int) -> bool:
        return 0 <= column_index < len(self.grid[0]) and 0 <= self.column_indices[
            column_index
        ] < len(self.grid)

    def __str__(self) -> str:
        return board_state_in_string_form(self.grid)


def board_state_in_string_form(grid: List[List[GridState]]) -> str:
    return "\n".join(["".join([str(item) for item in row]) for row in reversed(grid)])


def generic_win_condition(
    board: List[List[GridState]],
    column_indices: List[int],
    most_recent_column: int,
    grid_state: GridState,
    consecutive: int,
) -> bool:

    row_for_column = column_indices[most_recent_column]

    def check_down():
        if row_for_column < consecutive:
            return False
        result_down = all(
            [
                elem[most_recent_column] is grid_state
                for elem in board[row_for_column - consecutive : row_for_column]
            ]
        )
        return result_down

    def _check_direction(
        get_starting_spot: ...,
        get_starting_row_col_based_off_length: ...,
        get_spot_along_path_based_off_i: ...,
    ):
        row_for_column = column_indices[most_recent_column] - 1
        first_starting_row, first_starting_col = get_starting_spot(
            row_for_column, most_recent_column, consecutive
        )
        for i in range(consecutive):
            (
                current_starting_row,
                current_starting_col,
            ) = get_starting_row_col_based_off_length(
                first_starting_row, first_starting_col, i
            )
            result = __check_point_set_along_path(
                current_starting_row,
                current_starting_col,
                consecutive,
                grid_state,
                get_spot_along_path_based_off_i,
            )
            if result:
                return True
        return False

    #Downwards means that the diagonal slopes downwards, with respect to left to right
    def check_downwards_diag():
        return _check_direction(
            lambda row, col, i: (row - i + 1, col + i - 1),
            lambda row, col, i: (row + i, col - i),
            lambda row, col, i: (row + i, col - i),
        )

    def in_bounds(row: int, col: int) -> bool:
        return 0 <= row < len(board) and 0 <= col < len(board[0])

    #Downwards means that the diagonal slopes upwards, with respect to left to right
    def check_upwards_diag():
        return _check_direction(
            lambda row, col, i: (row + i - 1, col + i - 1),
            lambda row, col, i: (row - i, col - i),
            lambda row, col, i: (row - i, col - i),
        )

    def check_horizontal():
        return _check_direction(
            lambda row, col, i: (row, col - i + 1),
            lambda row, col, i: (row, col + i),
            lambda row, col, i: (row, col + i),
        )

    def __check_point_set_along_path(
        starting_row: int,
        starting_col: int,
        length: int,
        state: GridState,
        next_point_function: ...,
    ):
        for i in range(length):
            current_row, current_col = next_point_function(
                starting_row, starting_col, i
            )
            if (
                not in_bounds(current_row, current_col)
                or not board[current_row][current_col] is state
            ):
                return False
        return True

    return (
        check_down()
        or check_downwards_diag()
        or check_upwards_diag()
        or check_horizontal()
    )


def run_test_cases():
    #Test horizontal win by Player 1
    game = Game(width=7, height=6, consecutive_to_win=4)
    result = game.play_move_sequence([1, 2, 3, 4, 5, 5], [0, 0, 0, 5, 5])
    assert result == (GameWinner.RED, 3)

    #Test vertical win by Player 1: should terminate after 4 moves (index 3), so 5th move is ignored
    game = Game(width=7, height=6, consecutive_to_win=4)
    result = game.play_move_sequence([1, 1, 1, 1, 3], [2, 2, 2, 3, 3])
    assert result == (GameWinner.RED, 3)

    #Test win by Player 1 after 5 moves
    game = Game(width=7, height=6, consecutive_to_win=4)
    result = game.play_move_sequence([1, 1, 1, 3, 1], [2, 2, 2, 4])
    assert result == (GameWinner.RED, 4)

    #Test win by Player 1 with upward trending diagonal
    game = Game(width=7, height=6, consecutive_to_win=4)
    result = game.play_move_sequence([0, 1, 3, 2, 3, 3], [1, 2, 2, 3, 4])
    assert result == (GameWinner.RED, 5)

    #Test win by Player 2 with downward trending diagonal
    game = Game(width=7, height=6, consecutive_to_win=4)
    result = game.play_move_sequence([2, 1, 1, 0, 0], [3, 2, 1, 0, 0])
    assert result == (GameWinner.BLACK, 4)

run_test_cases()
