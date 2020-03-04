#project3 
from word_transformations import Transformer

# From piazza post @53: 
#Each transformation should produce an output. Imagine the following sequence of interactions:


# 1. Program asks for a recipe URL;
# 2. User enters said URL;
# 3. Program displays the parsed recipe;
def search_url_input():
	url_or_keywords = input("Please enter a recipe url or search keywords: \n")
	return url_or_keywords.strip()


# 4. Program shows a predefined set of transformations as a numbered list;
def set_transformations():
	print("Please enter the number of the transformation you want")
	# To and from vegetarian (REQUIRED)
	print("1 - From vegetarian to non-vegetarian")
	print("2 - From non-vegetarian to vegetarian")
	# To and from healthy (REQUIRED)
	print("3 - From healthy to non-healthy")
	print("4 - From non-healthy to healthy")
	# Style of cuisine (AT LEAST ONE REQUIRED)
	print("5 - Transform to Asian cuisine")
	# Additional Style of cuisine (OPTIONAL)
	print("6 - Transform to Y cuisine")
	# DIY to easy (OPTIONAL)
	print("7 - DIY to easy")
	# Double the amount or cut it by half (OPTIONAL)
	print("8 - Double the amount")
	print("9 - Reduce the amount by half")
	# Cooking method (from bake to stir fry, for example) (OPTIONAL)
	print("10 - Change cooking method")

# 5. User enters a number within said list;


# 6. Program displays the output of the selected transformation
def transformation():
	selected_transformation = input()
	print("\n")
	if selected_transformation == "1":
		print("~Transformed recipe to non-vegetarian~")
	elif selected_transformation == "2":
		print("~Transformed recipe to vegetarian~")
	elif selected_transformation == "3":
		print("~Transformed recipe to non-healthy~")
	elif selected_transformation == "4":
		print("~Transformed recipe to healthy~")
	elif selected_transformation == "5":
		print("~Transformed to Asian cuisine~")
	elif selected_transformation == "6":
		print("~Transformed to Y cuisine~")
	elif selected_transformation == "7":
		print("~Transformed to easy~")
	elif selected_transformation == "8":
		print("~Doubled the amount~")
	elif selected_transformation == "9":
		print("~Reduced the amount by half~")
	elif selected_transformation == "10":
		print("~Changed cooking method~")
	else:
		print("Please enter a number 1-10")
		transformation()

	return int(selected_transformation)

# 7. Program asks if the user would like to continue transforming the recipe or start from scratch with a new recipe;
def continue_startover():
	print("Please enter: ")
	print("1 - If you would like to continue transforming this recipe")
	print("2 - If you would like to start over with a new recipe")
	print("3 - If you would like to exit")

# 8. User enters an option;

# 9. Program goes back to #1 or continues to iterate over the previously transformed recipe.
# todo: abstract this out so we can use oru classes for it
def next_step():
	selected_option = input()
	if selected_option == "1":
		set_transformations()
		transformation()
		continue_startover()
		next_step()
	elif selected_option == "2":
		print("\n")
		url = search_url_input()
		set_transformations()
		transformation()
		continue_startover()
		next_step()
	elif selected_option == "3":
		return
	else:
		print("Please enter 1, 2, or 3")
		next_step()



if __name__ == '__main__':
	search_url_input()
	set_transformations()
	transformation()
	continue_startover()
	next_step()





