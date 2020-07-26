from functions import print_help, print_header, input_validator, print_menu
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean,  desc

import sys, os
import datetime

# Start SQLAlchemy Session and Engine
Base = declarative_base()


# DB Records
class User(Base):
	""""
	Define the User table.
	ID: Primary Key
	Username: Name of the player
	RoundsWon/Lost: Accumulated rounds won or lost
	GamesWon/Lost: Accumulated games won or lost
	RoundStreak/Lost: Accumulated rounds won or lost in a row
	"""""
	__tablename__ = "User"

	id = Column(Integer, primary_key=True)
	username = Column(String(10), unique=True)
	RoundsWon = Column(Integer, default=0)
	RoundsLost = Column(Integer, default=0)
	GamesWon = Column(Integer, default=0)
	GamesLost = Column(Integer, default=0)
	RoundStreak = Column(Integer, default=0)
	RoundLostStreak = Column(Integer, default=0)

class GameMaster(Base):
	""""
	Define the GameMaster table that will be used to store the games played.
	Plus information regarding the game:
	ID: Primary Key
	Player1/2: Tracking ID of Players
	Player1/2_c_points: Tracks accumulated points
	MaxPoints: Max points to play to until the game is ended
	CreatedAt: Stores date and time it was created
	Enabled: Boolean value to see if the game is in play or not
	"""""
	__tablename__ = "GameMaster"

	idGame = Column(Integer, primary_key=True)
	Player1 = Column(Integer)
	Player2 = Column(Integer)
	Player1_c_points = Column(Integer, default=0)
	Player2_c_points = Column(Integer, default=0)
	MaxPoints = Column(Integer)
	Winner = Column(String, default="None")
	CreatedAt = Column(DateTime, default=datetime.datetime.utcnow)
	CompletedAt = Column(DateTime, default=datetime.datetime.utcnow)
	Enabled = Column(Boolean, default=1)

class SubGame(Base):
	""""
	Define the SubGame table, keeps track of rounds played attached to MasterGame.
	ID: Primary Key
	Player1/2_points: Tracks points for the round of each player
	Winner: Winner of the round
	DatePlayed: Date the round was played
	"""""
	__tablename__ = "SubGame"

	id = Column(Integer, primary_key=True)
	Player1_points = Column(Integer)
	Player2_points = Column(Integer)
	winner = Column(String)
	DatePlayed = Column(DateTime, default=datetime.datetime.utcnow)

	idGame = Column(Integer)

engine = create_engine('sqlite:///scala.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
# Create the session for connecting to db
session = Session()

# Main Functions
def menu(**kwargs):
	# Clear terminal
	os.system('clear')
	# Show header
	print_header()
	# Show main menu
	print_menu()
	# - Add master game
	# - Add sub game
	# -- Show current master games
	# -- Input game to add to
	# -- Call add sub game function
	# - View current games
	# - View Stats
	# Input selection
	while True:
		menu_select = input_validator("Enter your selection [1-7]", int)
		if menu_select == 1:
			create_game()
		elif menu_select == 2:
			getid = current_games(return_id=1)
			add_subgame(id=getid)
		elif menu_select == 3:
			current_games()
		elif menu_select == 4:
			finished_games()
		elif menu_select == 5:
			view_stats()
		elif menu_select == 6:
			print_help()
		elif menu_select == 7:
			print("Goodbye!")
			exit()
		elif menu_select > 7:
			print("Invalid input, enter [1-7]!")



def create_game(**kwargs):
	# Ask for players names
	Player1 = input("1st players name? ")
	Player2 = input("2nd players name? ")
	# Ask for user names depending on numnber of users if user doesn't exist create user in db
	# If user does exist link them to the game table
	for uName in [Player1, Player2]:
		if not session.query(User).filter_by(username=uName).first():
			new_user = User(username=uName)
			session.add(new_user)
			# Commit new user
	mPoints = input("Max points: ")
	# Find players id's
	id_player1 = session.query(User).filter_by(username=Player1).first()
	id_player2 = session.query(User).filter_by(username=Player2).first()
	# Create game table
	new_game = GameMaster(Player1=id_player1.id, Player2=id_player2.id, MaxPoints=int(mPoints))
	session.add(new_game)
	# Commit new_game
	session.commit()
	print("Game added!")


def add_subgame(id, **kwargs):
	current_game = session.query(GameMaster).filter_by(idGame=id).first()
	player1 = session.query(User).filter_by(id=current_game.Player1).first()
	player2 = session.query(User).filter_by(id=current_game.Player2).first()
	# Enter points for both players
	player1_points = int(input(f"Enter {player1.username} points for this round: "))
	player2_points = int(input(f"Enter {player2.username} points for this round: "))
	# Determine winner with lowest points
	# - Add round won to players id
	# - Add round lost to losing player id
	if player1_points < player2_points:
		round_winner = player1
		round_loser = player2
		player1.RoundsWon += 1
		player2.RoundsLost += 1
	else:
		round_winner = player2
		round_loser = player1
		player2.RoundsWon += 1
		player1.RoundsLost += 1
	# Add both players points to PlayerN_c_points !!
	current_game.Player1_c_points += player1_points
	current_game.Player2_c_points += player2_points
	# Check to see if either players c_points are equal to or above max
	if current_game.Player1_c_points > current_game.MaxPoints or current_game.Player2_c_points > current_game.MaxPoints > current_game.MaxPoints:
		# If they are then end the game (Enabled = 0)
		current_game.Enabled = 0
		current_game.Winner = round_winner.username
		current_game.CompletedAt = datetime.datetime.utcnow
		print("Game Over")
		print(f"{round_winner.username} is the winner!")
		if player1_points < player2_points:
			# - Add +1 to games won by player who won over all
			player1.GamesWon += 1
			player2.GamesLost += 1
		else:
			# - Add +1 to games lost by player that lost over all
			player2.GamesWon += 1
			player1.GamesLost += 1
	#Save all records
	new_game = SubGame(Player1_points=player1_points, Player2_points=player2_points, winner=round_winner.username, idGame=id)
	session.add_all([player1, player2, current_game, new_game])
	# Commit records
	session.commit()
	print("Round added!")


def view_stats(**kwargs):
	# Printout highest wins by player
	HS = session.query(User).order_by(desc(User.GamesWon)).first()
	print("Highest Wins:")
	print(f"{HS.username}: {HS.GamesWon}")
	# Printout highest rounds won
	RW = session.query(User).order_by(desc(User.RoundsWon)).first()
	print("Most Rounds Won:")
	print(f"{RW.username}: {RW.RoundsWon}")
	# Printout rounds won streak
	RS = session.query(User).order_by(desc(User.RoundStreak)).first()
	print("Rounds Won Streak:")
	print(f"{RS.username}: {RS.RoundStreak}")
	# Printout rounds lost streak
	RL = session.query(User).order_by(desc(User.RoundLostStreak)).first()
	print("Biggest Losing Streak:")
	print(f"{RL.username}: {RL.RoundLostStreak}")
	# Printout biggest loser of games
	GL = session.query(User).order_by(desc(User.GamesLost)).first()
	print("Most Games Lost:")
	print(f"{GL.username}: {GL.GamesLost}")
	# Printout biggest point accumulation


def current_games(return_id=0):
	print("Current active games:")
	# Display current enabled games from database
	for index, instance in enumerate(session.query(GameMaster).order_by(GameMaster.idGame)):
		if not instance:
			print("No games are current.")
		if instance.Enabled:
			player1 = session.query(User).filter_by(id=instance.Player1).first()
			player2 = session.query(User).filter_by(id=instance.Player2).first()
			print(f"ID: {instance.idGame} | {player1.username}: {instance.Player1_c_points} | {player2.username}: {instance.Player2_c_points} | Max Points: {instance.MaxPoints} | Started: {instance.CreatedAt.date()}")
			for ix, sub_instance in enumerate(session.query(SubGame).order_by(SubGame.idGame)):
				if sub_instance.idGame == instance.idGame:
					print(f"--->{ix+1}. {player1.username}: {sub_instance.Player1_points} | {player2.username}: {sub_instance.Player2_points} | Winner: {sub_instance.winner} | Played: {sub_instance.DatePlayed.date()}")
	if return_id == 1:
		getid = input_validator("Enter ID of game you wish to add to", int)
		return getid


def finished_games():
	print("Finished Games:")
	for index, instance in enumerate(session.query(GameMaster).order_by(GameMaster.idGame)):
		if not instance:
			print("No games are current.")
		if not instance.Enabled:
			player1 = session.query(User).filter_by(id=instance.Player1).first()
			player2 = session.query(User).filter_by(id=instance.Player2).first()
			print(
				f"ID: {instance.idGame} | "
				f"{player1.username}: {instance.Player1_c_points} | "
				f"{player2.username}: {instance.Player2_c_points} | "
				f"Max Points: {instance.MaxPoints} | "
				f"Winner: {instance.Winner} | "
				f"Started: {instance.CreatedAt.date()} | "
				f"Finished: {instance.CompletedAt.date()}")


# Terminal flag input
if "--help" in sys.argv:
	print_help()
	exit()
elif "--addsub" in sys.argv:
	getid = current_games(return_id=1)
	add_subgame(id=getid)
	exit()
elif "--view" in sys.argv:
	current_games()
	exit()

# Main program logic
menu()