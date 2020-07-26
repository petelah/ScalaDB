def print_header():
	intro = """
  _____           _         _____  ____                       .------.
 / ____|         | |       |  __ \|  _ \   .------.           |A .   |
| (___   ___ __ _| | __ _  | |  | | |_) |  |A_  _ |    .------; / \  |
 \___ \ / __/ _` | |/ _` | | |  | |  _ <   |( \/ )|-----. _   |(_,_) |
 ____) | (_| (_| | | (_| | | |__| | |_) |  | \  / | /\  |( )  |  I  A|
|_____/ \___\__,_|_|\__,_| |_____/|____/   |  \/ A|/  \ |_x_) |------'
                                           `-----+'\  / | Y  A|
                                                 |  \/ A|-----' 
<================================================`------'============>"""
	print(intro)


def print_help():
	HELP = """
╔════════════════════════════════════════════════════════════════════╗
║                           Help Me!                                 ║ 
╚════════════════════════════════════════════════════════════════════╝
╔════════════════════════════════════════════════════════════════════╗
║ Scala DB is a scala quaranta card game tracker.                    ║
║ 1. Start by adding a master game, following the prompts.           ║
║ 2. Once a round is played select add sub game and follow the       ║
║ prompts to add in the scores of the game just played.              ║
║ 3. Once score conditions are met the program will automatically.   ║
║ declare a winner for the whole game.                               ║
║ - You may select menu item 3 to view current games active.         ║
║ - You can also view player stats and highscores selecting item 4.  ║
║ Terminal Flags:                                                    ║
║ --help - Takes you right here                                      ║
║ --addsub - Quick add a sub game to a master game                   ║
║ --view - Allows the user to view current games in progress         ║
╚════════════════════════════════════════════════════════════════════╝"""

	print(HELP)


def print_menu():
	MENU = """╔════════════════════════════════════════════════════════════════════╗
║                           Main Menu                                ║ 
╚════════════════════════════════════════════════════════════════════╝
╔════════════════════════════════════════════════════════════════════╗
║ 1. Add Master Game                                                 ║
║ 2. Add Sub Game                                                    ║
║ 3. View Current Games                                              ║
║ 4. View Finished Games                                             ║
║ 5. View Stats                                                      ║
║ 6. Help Me!                                                        ║
║ 7. Exit                                                            ║
╚════════════════════════════════════════════════════════════════════╝
"""
	print(MENU)


def input_validator(display_text, return_type):
	while True:
		try:
			i = return_type(input(f"{display_text}: "))
			return i
		except ValueError:
			print("Invalid input")
			if return_type == int:
				print("Please enter a whole number")
			elif return_type == str:
				print("Please enter a string")





def test_func():
	create_game()

	add_subgame(id=1)
	test_game = session.query(GameMaster).first()
	print(f"ID: {test_game.idGame}")
	print(f"Player One: {test_game.Player1}")
	print(f"Points: {test_game.Player1_c_points}")
	print(f"Player Two: {test_game.Player2}")
	print(f"Points: {test_game.Player2_c_points}")
	print(f"Points Max: {test_game.MaxPoints}")

	add_subgame(id=1)
	print(f"ID: {test_game.idGame}")
	print(f"Player One: {test_game.Player1}")
	print(f"Points: {test_game.Player1_c_points}")
	print(f"Player Two: {test_game.Player2}")
	print(f"Points: {test_game.Player2_c_points}")
	print(f"Points Max: {test_game.MaxPoints}")
