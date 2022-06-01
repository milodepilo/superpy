# Do not modify these lines
__winc_id__ = '71dd124b4a6e4d268f5973db521394ee'
__human_name__ = 'strings'

# Add your code after this line
scorer_name1 = "Ruud Gullit"
scorer_name2 = "Marco van Basten"

goal_0 = 32
goal_1 = 54

scorers = f"{scorer_name1} {goal_0}, {scorer_name2} {goal_1}"

report = f"{scorer_name1} scored in the {str(goal_0)}nd minute\n{scorer_name2} scored in the {str(goal_1)}th minute"



player = "Jan Wouters"
first_name = player[0: player.find("Wouters")-1]
last_name_len = len(player[player.find("Wouters"):])
name_short = f"{first_name[0:1]}. {player[player.find('Wouters'):]}"
chant = f"{first_name + '!'} {first_name + '!'} {first_name + '!'}"

good_chant = chant[-1:] != ""
