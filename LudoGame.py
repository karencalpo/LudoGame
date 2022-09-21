# Author: Karen Calpo
# GitHub username: karencalpo
# Date: 8/12/2022
# Description: A Ludo Game application that can be played by 1-4 players. Moves are determined by the roll
# of a 6-sided die simulated by rolls passed as parameters into the application.

class Player:
    def __init__(self, position, start, end):
        """Contains the position of the player (A,B,C,D), it's start and
        end space, current position of it's two tokens (Tokens are p and q. Positions are ‘H’ for home yard,
        ‘R’ for ready to go position, ‘E’ for finished position, and other letters/numbers for the space
        the token has landed on), and current game state of the player"""
        self._position = position
        self._start = start  # integer for which square player starts
        self._end = end  # integer for which square player ends
        self._p_position = "H"
        self._q_position = "H"
        self._total_steps_q = -1
        self._total_steps_p = -1
        self._state = False
        self._tokens_stacked = False  # this will be set to true if both tokens are in the same square

    def get_completed(self):
        """Takes no parameters and returns True if the player has finished
        the game and False if they have not"""
        return self._state

    def set_completed(self, state):
        self._state = state

    def get_tokens_stacked(self):
        return self._tokens_stacked

    def set_tokens_stacked(self, state):
        self._tokens_stacked = state

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_position(self):
        return self._position

    def set_p_position(self, position):
        if position == -1:
            self._p_position = "H"
        elif position == 0:
            self._p_position = "R"
        else:
            self._p_position = position + 1

    def set_q_position(self, position):
        if position == -1:
            self._q_position = "H"
        elif position == 0:
            self._q_position = "R"
        else:
            self._q_position = position + 1

    def get_p_position(self):
        return self._p_position

    def get_q_position(self):
        return self._q_position

    def get_token_p_step_count(self):
        """Takes no parameters and returns the total steps the token p has
        taken on the board. The total step should not be larger than 57. If
        the token is bounced back in the home squares, this bounced part is
        subtracted from the step count."""

        return self._total_steps_p

    def get_token_q_step_count(self):
        """Takes no parameters and returns the total steps the token q has
        taken on the board. The total step should not be larger than 57. If
        the token is bounced back in the home squares, this bounced part is
        subtracted from the step count."""

        return self._total_steps_q

    def set_token_q_step_count(self, count):
        self._total_steps_q = count

    def set_token_p_step_count(self, count):
        self._total_steps_p = count

    def get_space_name(self, total_steps):
        """Takes as a parameter the total steps of the token and returns the name
        of the space the token has landed on the board as a string. It  aldo returns the
        home yard position (‘H’) and the ready to go position (‘R’) as well"""

        if total_steps == self._start - 1:
            return "H"
        elif total_steps == self._start:
            return "R"
        elif total_steps == 51:
            return self._position + "1"
        elif total_steps == 52:
            return self._position + "2"
        elif total_steps == 53:
            return self._position + "3"
        elif total_steps == 54:
            return self._position + "4"
        elif total_steps == 55:
            return self._position + "5"
        elif total_steps == 56:
            return self._position + "6"
        elif total_steps == 57:
            return "E"
        else:
            return str(total_steps)


class LudoGame:

    def __init__(self):
        """Below in self._board, player's tokens will move across the board (from spaces 0-57), in a
        clockwise direction. Start and end parameters determine where a player's position starts and ends.
        Tokens go back to home if they are 'bounced' out of the square they are currently in by an
        opposing player's token (both tokens go back if they are stacked in the same square)."""
        self._players = {}
        self._board = [None] * 57

    def get_player_by_position(self, player_pos):
        """Method takes a parameter representing the player's position as a
        string and returns the player object. An invalid string parameter returns
        'Player not found!'"""
        if player_pos in self._players:
            return self._players[player_pos]
        else:
            return 'Player not found!'

    def move_token(self, player, tokens, turn):
        """This method will take care of one token moving on the board and will
        update the token's total steps. It will also take care of kicking out other
        opponent tokens as needed. The play_game method will use this method."""
        able_to_move = True     # whenever token is moved, set this to False

        if len(tokens) == 2:
            if player.get_token_p_step_count() == 57 and player.get_token_q_step_count() == 57:
                player.set_completed(True)
                return
            elif player.get_token_p_step_count() == -1 and player.get_token_q_step_count() == -1 and turn[1] == 6:
                # Check to see if a token can move
                # if able to move, then set able to move to False
                if able_to_move:
                    player.set_token_p_step_count(0)
                    able_to_move = False
                    self._board[player.get_start()] = (turn[0], "p")
                if self._board[player.get_token_q_step_count() + player.get_start() + turn[1]] is not None:
                    if self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][0] != turn[0]:
                        if self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][1] == 'p':
                            player2 = self.get_player_by_position(
                                self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][0])
                            if able_to_move:
                                player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                                self._board[player.get_token_p_step_count() + player.get_start()] = None
                                player2.set_token_p_step_count(-1)
                                able_to_move = False
                        else:
                            player2 = self.get_player_by_position(
                                self._board[player.get_token_q_step_count() + player.get_start() + turn[1]][0])
                            if able_to_move:
                                player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                                self._board[player.get_token_p_step_count() + player.get_start()] = None
                                player2.set_token_p_step_count(-1)
            else:
                if able_to_move:
                    player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                    able_to_move = False
                if player.get_token_p_step_count() == 0:
                    self._board[player.get_token_p_step_count() + player.get_start()] = None
                else:
                    self._board[player.get_token_p_step_count() + player.get_start()] = None
                    self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "p")
        elif player.get_tokens_stacked() is True:
            self._board[player.get_token_p_step_count() + player.get_start()] = None
            if able_to_move:
                player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "p"), (turn[0], "q")
                able_to_move = False
        elif "p" in tokens:
            if player.get_token_p_step_count() != 57:
                if player.get_token_p_step_count() == -1 and turn[1] == 6:
                    if able_to_move:
                        player.set_token_p_step_count(0)
                        self._board[player.get_start()] = (turn[0], "p")
                        able_to_move = False
                elif player.get_token_p_step_count() >= 0:
                    if self._board[player.get_token_p_step_count() + player.get_start()][1] == "p":
                        self._board[player.get_token_p_step_count() + player.get_start()] = None
                    if self._board[player.get_token_p_step_count() + player.get_start() + turn[1]] is not None:
                        if self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][0] != turn[0]:
                            if self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][1] == 'p':
                                player2 = self.get_player_by_position(self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][0])
                                if able_to_move:
                                    player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                                    self._board[player.get_token_p_step_count() + player.get_start()] = None
                                    player2.set_token_p_step_count(-1)
                                    able_to_move = False
                            else:
                                player2 = self.get_player_by_position(self._board[player.get_token_p_step_count() + player.get_start() + turn[1]][0])
                                if able_to_move:
                                    player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                                    self._board[player.get_token_q_step_count()] = None
                                    player2.set_token_q_step_count(-1)
                                    able_to_move = False
                        else:
                            if able_to_move:
                                player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                                self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "p"), (turn[0], "q")
                                able_to_move = False
                            return
                    if self._board[player.get_token_p_step_count() + player.get_start()] == ((turn[0], "p"), (turn[0], "q")):
                        self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "q")
                        self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "q")
                    if able_to_move:
                        player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                        self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "p")
                        able_to_move = False
                else:
                    # print("here else p p")
                    if self._board[player.get_token_q_step_count() + player.get_start()][1] == "q":
                        self._board[player.get_token_q_step_count() + player.get_start()] = None
                    if able_to_move:
                        player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                        self._board[player.get_token_q_step_count()] = (turn[0], "q")
                        able_to_move = False
        elif "q" in tokens:
            if player.get_token_q_step_count() != 57:
                if player.get_token_q_step_count() == -1 and turn[1] == 6:
                    if able_to_move:
                        player.set_token_q_step_count(0)
                        self._board[player.get_start()] = (turn[0], "q")
                        player.set_q_position(0)
                        able_to_move = False
                elif player.get_token_q_step_count() >= 0:
                    # print("Before all q", self._board)
                    if self._board[player.get_token_q_step_count() + player.get_start()][1] == "q":
                        self._board[player.get_token_q_step_count() + player.get_start()] = None
                    # use logic below for "p" above
                    if self._board[player.get_token_q_step_count() + player.get_start() + turn[1]] is not None:
                        # print(self._board[player.get_token_q_step_count() + turn[1]][0])
                        if self._board[player.get_token_q_step_count() + player.get_start() + turn[1]][0] != turn[0]:
                            if self._board[player.get_token_q_step_count() + player.get_start() + turn[1]][1] == 'q':
                                player2 = self.get_player_by_position(self._board[player.get_token_q_step_count() +
                                                                                  player.get_start() + turn[1]][0])
                                if able_to_move:
                                    player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                                    self._board[player.get_token_q_step_count() + player.get_start()] = None
                                    player2.set_token_q_step_count(-1)
                                    able_to_move = False
                            else:
                                player2 = self.get_player_by_position(self._board[player.get_token_q_step_count() + player.get_start() + turn[1]][0])
                                if able_to_move:
                                    player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                                    self._board[player.get_token_p_step_count() + player.get_start()] = None
                                    player2.set_token_p_step_count(-1)
                                    able_to_move = False
                        else:
                            if able_to_move:
                                player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                                self._board[player.get_token_q_step_count() + player.get_start()] = (turn[0], "p"), (turn[0], "q")
                                player.set_tokens_stacked(True)
                                able_to_move = False
                            return
                    if able_to_move:
                        player.set_token_q_step_count(player.get_token_q_step_count() + turn[1])
                        self._board[player.get_token_q_step_count() + player.get_start()] = (turn[0], "q")
                        able_to_move = False
                else:
                    # print("here else p q")
                    if self._board[player.get_token_p_step_count() + player.get_start()][1] == "p":
                        self._board[player.get_token_p_step_count() + player.get_start()] = None
                    if able_to_move:
                        player.set_token_p_step_count(player.get_token_p_step_count() + turn[1])
                        self._board[player.get_token_p_step_count() + player.get_start()] = (turn[0], "p")
                        able_to_move = False

    def play_game(self, players_list, turns_list):
        """The player's list is the list of positions the players choose. The turns
        list is a list of tuples with each tuple a roll for one player. This method will
        create the player list first using the players list that was passed in. Then the
        tokens will be moved according to the turns list following the priority rule
        and update the tokens position and the player’s game state (whether
        the game is finished or not)."""

        for player in players_list:
            if self._players.get(player) is None:
                if player == 'A':
                    self._players[player] = Player(player, 0, 5)
                elif player == 'B':
                    self._players[player] = Player(player, 14, 8)
                elif player == 'C':
                    self._players[player] = Player(player, 28, 22)
                elif player == 'D':
                    self._players[player] = Player(player, 42, 36)
                else:
                    return "Invalid player position."
            else:
                return "Player already exists."

        for turn in turns_list:
            player = self._players[turn[0]]
            tokens = self.priority_rules(turn, player)
            self.move_token(player, tokens, turn)

        token_positions = []
        for player in self._players.values():
            token_positions.append(player.get_space_name(player.get_token_p_step_count() + player.get_start()))
            token_positions.append(player.get_space_name(player.get_token_q_step_count() + player.get_start()))

        return token_positions

    def priority_rules(self, turn, player):
        """This function is called by play_game. The parameter 'turn' is a tuple passed from the
        turns_list that play_game loops through. It will return the appropriate token according to
        the priority rules test in the if statements below"""
        tokens = []

        if turn[1] == 6:
            if player.get_token_p_step_count() == -1 and player.get_token_q_step_count() == -1:
                tokens.append('p')
                return tokens
            elif player.get_token_p_step_count() == -1:
                tokens.append('p')
                return tokens
            elif player.get_token_q_step_count() == -1:
                tokens.append('q')
                return tokens
            elif player.get_token_q_step_count() < player.get_token_p_step_count():
                tokens.append('q')
                return tokens
            elif player.get_token_p_step_count() < player.get_token_q_step_count():
                tokens.append('p')
            else:
                return tokens

        if player.get_token_p_step_count() > 50 or player.get_token_q_step_count() > 50:
            if player.get_token_p_step_count() + turn[1] == 57 and player.get_token_q_step_count() + turn[1] == 57:
                tokens.append('p')
                tokens.append('q')
            elif player.get_token_p_step_count() + turn[1] == 57:
                tokens.append('p')
            elif player.get_token_q_step_count() + turn[1] == 57:
                tokens.append('q')
            return tokens

        p_player_space = (player.get_token_p_step_count() + player.get_start() + turn[1])
        q_player_space = (player.get_token_q_step_count() + player.get_start() + turn[1])

        if (self._board[p_player_space] and self._board[p_player_space][0] != turn[0]) or \
                (self._board[q_player_space] and self._board[q_player_space][0] != turn[0]):
            if self._board[p_player_space] and self._board[p_player_space][0] != turn[0]:
                tokens.append('p')

            if self._board[q_player_space] and self._board[q_player_space][0] != turn[0]:
                tokens.append('q')
            return tokens

        if (57 - player.get_token_q_step_count()) > (57 - player.get_token_p_step_count()):
            if player.get_token_q_step_count() == -1:
                tokens.append("p")
                return tokens
            tokens.append("q")
            return tokens
        else:
            if player.get_token_p_step_count() == -1:
                tokens.append("q")
                return tokens
            tokens.append("p")
            return tokens
