import argparse

from src.app  import parse_arguments

version = "0.1.0"

parser = argparse.ArgumentParser()


parser.add_argument("-st",
					"--start",
					help="Start the application",
					action="store_true")

parser.add_argument("-gr",
					"--getrules",
					help="Get the current rules",
					action="store_true")

parser.add_argument("-da",               
		    			"--del_all_rules",
		    			help="Delete all the rules",
		    			action="store_true")

parser.add_argument("-di",
					"--del_id",
					help ="delete by ID")

parser.add_argument("-dv",
					"--del_val",
					help ="delete by value")

parser.add_argument("-add",
                    "--add_rule",
                    help="Adds the rules",
					action = "store_true")

ARGV = parser.parse_args()
parse_arguments(ARGV)
