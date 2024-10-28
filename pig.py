import random
import time

def roll_die(sides=6):
    return random.randint(1, sides)

class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.total_points = 0

    def display(self):
        print(f"{self.name} has {self.total_points} points.")

    def __str__(self) -> str:
        return f"{self.name} has {self.total_points} points."

    def play_turn(self):
        turn_points = 0
        while True:
            roll = roll_die()
            print(f"{self.name} rolled a {roll}")
            
            if roll == 1:
                print(f"{self.name} loses the turn! No points added.")
                turn_points = 0
                break
            else:
                turn_points += roll
                print(f"Current turn total for {self.name}: {turn_points}")

                decision = input("Roll again (r) or Hold (h)? ").lower()
                if decision == 'h':
                    self.total_points += turn_points
                    print(f"{self.name} holds with a total score of {self.total_points} points.")
                    break

    def reset(self):
        
        self.total_points = 0

class HumanPlayer(Player):
    pass  

class ComputerPlayer(Player):
    def play_turn(self):
        turn_points = 0
        while True:
            roll = roll_die()
            print(f"{self.name} (computer) rolled a {roll}")
            
            if roll == 1:
                print(f"{self.name} loses the turn! No points added.")
                turn_points = 0
                break
            else:
                turn_points += roll
                print(f"Current turn total for {self.name}: {turn_points}")

                if turn_points >= min(25, 100 - self.total_points):
                    self.total_points += turn_points
                    print(f"{self.name} holds with a total score of {self.total_points} points.")
                    break

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")

class Game:
    def __init__(self, players, win_points=100) -> None:
        self.players = players  
        self.win_points = win_points
        self.winner = None

    def check_winner(self):
        for player in self.players:
            if player.total_points >= self.win_points:
                self.winner = player
                return True
        return False

    def play(self):
        current_player_idx = 0
        while not self.check_winner():
            current_player = self.players[current_player_idx]
            print(f"\nIt's {current_player.name}'s turn")
            current_player.play_turn()
            current_player_idx = (current_player_idx + 1) % len(self.players)  
            print("----------------- End of Round ----------------")

        print(f"The winner is {self.winner.name}!")
        self.winner.display()

    def reset_game(self):
        
        for player in self.players:
            player.reset()
        self.winner = None

class TimedGameProxy:
    def __init__(self, game, time_limit=60):
        self.game = game
        self.time_limit = time_limit
        self.start_time = None

    def play(self):
        self.start_time = time.time()
        current_player_idx = 0
        while not self.game.check_winner():
            if time.time() - self.start_time > self.time_limit:
                print("Time is up!")
                self.declare_winner()
                return

            current_player = self.game.players[current_player_idx]
            print(f"\nIt's {current_player.name}'s turn")
            current_player.play_turn()
            current_player_idx = (current_player_idx + 1) % len(self.game.players)
            print("----------------- End of Round ----------------")

        print(f"The winner is {self.game.winner.name}!")
        self.game.winner.display()

    def declare_winner(self):
        max_points = max(player.total_points for player in self.game.players)
        winners = [player for player in self.game.players if player.total_points == max_points]
        if len(winners) > 1:
            print("It's a tie!")
        else:
            print(f"The winner is {winners[0].name} with {winners[0].total_points} points!")
        for player in self.game.players:
            player.display()

    def reset_game(self):
        self.game.reset_game()

def main():
    num_players = int(input("Enter the number of players: "))
    
    players = []
    for i in range(1, num_players + 1):
        player_type = input(f"Is Player {i} a 'human' or 'computer'? ").lower()
        player_name = input(f"Enter name for Player {i}: ")
        players.append(PlayerFactory.create_player(player_type, player_name))

    game = Game(players)
    
    use_timed_game = input("Would you like to play a timed game? (y/n): ").lower()
    if use_timed_game == 'y':
        game_proxy = TimedGameProxy(game)
        game_proxy.play()
    else:
        game.play()

    while True:
        play_again = input("\nWould you like to play another game? (y/n): ").lower()
        if play_again == 'y':
            game.reset_game()
            game.play()
        else:
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()
