import sqlite3


# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect('recipe.sqlite')


# Function to create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Creating tables with the given schema
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipe (
                      r_recipekey INTEGER PRIMARY KEY, 
                      r_name TEXT, 
                      r_techniquekey INTEGER, 
                      r_cuisinekey INTEGER, 
                      r_mealcoursekey INTEGER, 
                      r_instruction TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS technique (
                      t_techniquekey INTEGER PRIMARY KEY, 
                      t_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cuisine (
                          c_cuisinekey INTEGER PRIMARY KEY, 
                          c_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredient (
                          i_ingredientkey INTEGER PRIMARY KEY, 
                          i_name TEXT,
                          i_allergenkey INTEGER,
                          i_nutritionkey INTEGER)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS allergen (
                          a_allergenkey INTEGER PRIMARY KEY, 
                          a_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS nutrition (
                          n_nutritionkey INTEGER PRIMARY KEY, 
                          n_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS mealcourse (
                          m_mealcoursekey INTEGER PRIMARY KEY, 
                          m_name TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS rein (
                          ri_recipekey INTEGER PRIMARY KEY, 
                          ri_ingredientkey INTEGER)''')


    conn.commit()
    conn.close()


# Function to drop a table
def drop_table(table_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    conn.commit()
    conn.close()


# Function to insert a new recipe (Example of an insert operation)
def insert_recipe(recipe_data, ingredient_keys):
    conn = connect_db()
    cursor = conn.cursor()

    # Inserting the recipe data
    cursor.execute('''INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
                      VALUES (?, ?, ?, ?, ?)''', recipe_data)

    # Getting the last inserted recipe's key
    recipe_key = cursor.lastrowid

    # Inserting ingredient keys into rein table
    for ingredient_key in ingredient_keys:
        cursor.execute('''INSERT INTO rein (ri_recipekey, r_ingredientkey) 
                          VALUES (?, ?)''', (recipe_key, ingredient_key))

    conn.commit()
    conn.close()


# Function to view all recipes (Example of a select operation)
def view_all_recipes():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT r_name AS recipe AND SELECT r_instruction AS instruction FROM Recipe ORDER BY r_recipekey")
    recipes = cursor.fetchall()

    for recipe in recipes:
        print(recipe)

    conn.close()


def display_choices(table_name):
    conn = connect_db()
    cursor = conn.cursor()

    # Assuming the first column is the key and the second column is the name
    cursor.execute(f"SELECT * FROM {table_name}")
    items = cursor.fetchall()

    for item in items:
        key, name = item[0], item[1]  # Adjust these indices based on your table structure
        print(f"{key}: {name}")

    conn.close()


def insert_recipe_interactive():
    # Display choices from each category and get user input
    print("Select a Technique:")
    display_choices('technique')
    technique_key = input("Enter technique key: ")

    print("Select a Cuisine:")
    display_choices('cuisine')
    cuisine_key = input("Enter cuisine key: ")

    print("Select a Meal Course:")
    display_choices('mealcourse')
    mealcourse_key = input("Enter meal course key: ")

    print("Select a Nutrition Type:")
    display_choices('nutrition')
    nutrition_key = input("Enter nutrition type key: ")

    print("Select a Allergen:")
    display_choices('allergen')
    allergen_key = input("Enter allergen key: ")

    print("Select a Ingredient(s):")
    display_choices('ingredient')

    ingredient_keys = []
    while True:
        ingredient_key = input("Enter ingredient key (Enter 0 to finish): ")

        if ingredient_key == '0':  # Break the loop if the user enters 0
            break
        else:
            try:
                # Adding the key to the list if it's a valid number
                ingredient_key = int(ingredient_key)
                ingredient_keys.append(ingredient_key)
            except ValueError:
                # Handle non-integer input
                print("Please enter a valid ingredient key.")

    recipe_name = input("Enter recipe name: ")
    instructions = input("Enter instructions: ")

    insert_recipe((recipe_name, technique_key, cuisine_key, mealcourse_key, instructions))


def add_ingredient():
    conn = connect_db()
    cursor = conn.cursor()

    # Prompt user to enter ingredient name
    ingredient_name = input("Enter the name of the new ingredient: ")
    cursor.execute("INSERT INTO ingredient (i_name) VALUES (?)", (ingredient_name,))

    # Fetch the auto-generated ingredient key
    ingredient_key = cursor.lastrowid

    # Prompt user to add allergen and nutrition type
    display_choices('allergen')
    allergen_key = input("Enter the allergen key (enter 0 for none): ")
    display_choices('nutrition')
    nutrition_key = input("Enter the nutrition type key: ")

    # Update the ingredient with allergen and nutrition keys
    cursor.execute("UPDATE ingredient SET i_allergenkey = ?, i_nutritionkey = ? WHERE i_ingredientkey = ?",
                   (allergen_key if allergen_key != '0' else None, nutrition_key, ingredient_key))

    conn.commit()
    conn.close()
    print("Ingredient added successfully.")


def delete_ingredient():
    conn = connect_db()
    cursor = conn.cursor()

    # Display all ingredients
    display_choices('ingredient')

    # Prompt user to enter ingredient key or name to be deleted
    identifier = input("Enter the ingredient key or name to delete: ")

    # Determine if identifier is key (integer) or name (string)
    if identifier.isdigit():
        cursor.execute("DELETE FROM ingredient WHERE i_ingredientkey = ?", (int(identifier),))
    elif isinstance(identifier, str):
        cursor.execute("DELETE FROM ingredient WHERE i_name = ?", (identifier,))
    else:
        print("Invalid identifier type. Please provide an integer key or a string name.")

    conn.commit()
    conn.close()
    print("Ingredient deleted successfully.")


def edit_ingredient():
    conn = connect_db()
    cursor = conn.cursor()

    # Display all ingredients
    display_choices('ingredient')

    # Let user choose which ingredient to edit
    ingredient_key = input("Enter the key of the ingredient to edit: ")

    # Give options to edit
    print("1. Edit Ingredient Name")
    print("2. Edit Nutrition Type")
    print("3. Edit Allergen Type")
    choice = input("Choose an option: ")

    if choice == '1':
        new_name = input("Enter the new name for the ingredient: ")
        cursor.execute("UPDATE ingredient SET i_name = ? WHERE i_ingredientkey = ?", (new_name, ingredient_key))
    elif choice == '2':
        display_choices('nutrition')
        new_nutrition_key = input("Enter the new nutrition type key: ")
        cursor.execute("UPDATE ingredient SET i_nutritionkey = ? WHERE i_ingredientkey = ?", (new_nutrition_key, ingredient_key))
    elif choice == '3':
        display_choices('allergen')
        new_allergen_key = input("Enter the new allergen key (enter 0 for none): ")
        cursor.execute("UPDATE ingredient SET i_allergenkey = ? WHERE i_ingredientkey = ?",
                       (new_allergen_key if new_allergen_key != '0' else None, ingredient_key))
    else:
        print("Invalid option selected.")

    conn.commit()
    conn.close()
    print("Ingredient updated successfully.")


def add_ingredient_to_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert the ingredient into the rein table linked with the recipe
    cursor.execute("INSERT INTO rein (ri_recipekey, r_ingredientkey) VALUES (?, ?)", (recipe_key, ingredient_key))

    conn.commit()
    conn.close()
    print("Ingredient added to recipe successfully.")


def delete_ingredient_from_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete the ingredient from the rein table for the given recipe
    cursor.execute("DELETE FROM rein WHERE ri_recipekey = ? AND r_ingredientkey = ?", (recipe_key, ingredient_key))

    conn.commit()
    conn.close()
    print("Ingredient removed from recipe successfully.")


def edit_ingredients_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Display ingredients currently used by the recipe
    print(f"Current ingredients for recipe {recipe_key}:")
    cursor.execute("SELECT i_ingredientkey, i_name FROM rein JOIN ingredient ON ri_ingredientkey = i_ingredientkey WHERE ri_recipekey = ?", (recipe_key,))
    current_ingredients = cursor.fetchall()
    for current_ingredient in current_ingredients:
        print(f"{current_ingredient[0]}: {current_ingredient[1]}")

    # Options to add or remove ingredients
    print("\nOptions:")
    print("1. Add an ingredient to the recipe")
    print("2. Remove an ingredient from the recipe")
    choice = input("Choose an option: ")

    if choice == '1':
        # Show available ingredients
        display_choices('ingredient')
        ingredient_key = input("Enter the ingredient key to add: ")
        add_ingredient_to_recipe(recipe_key, ingredient_key)
    elif choice == '2':
        ingredient_key = input("Enter the ingredient key to remove: ")
        delete_ingredient_from_recipe(recipe_key, ingredient_key)
    else:
        print("Invalid option selected.")

    conn.close()



def add_nutrition(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO nutrition (n_name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def delete_nutrition(identifier):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the identifier is an integer (key) or string (name)
    if identifier.isdigit():
        cursor.execute("DELETE FROM nutrition WHERE n_nutritionkey = ?", (int(identifier),))
    elif isinstance(identifier, str):
        cursor.execute("DELETE FROM nutrition WHERE n_name = ?", (identifier,))
    else:
        print("Invalid identifier type. Please provide an integer key or a string name.")

    conn.commit()
    conn.close()


def edit_nutrition(key, new_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE nutrition SET n_name = ? WHERE n_nutritionkey = ?", (new_name, key))

    conn.commit()
    conn.close()


def edit_nutrition_of_ingredient(recipe_key, new_nutrition_key):
    # This assumes that the recipe table has a direct link to nutrition,
    # Modify as per your schema
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Recipe SET n_nutritionkey = ? WHERE r_recipekey = ?", (new_nutrition_key, recipe_key))
    conn.commit()
    conn.close()


def view_nutrition():
    display_choices('nutrition')


def add_allergen(allergen_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Allergen (a_name) VALUES (?)", (allergen_name,))
    conn.commit()
    conn.close()


def delete_allergen(identifier):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the identifier is an integer (key) or string (name)
    if isinstance(identifier, int):
        cursor.execute("DELETE FROM allergen WHERE a_allergenkey = ?", (identifier,))
    elif isinstance(identifier, str):
        cursor.execute("DELETE FROM allergen WHERE a_name = ?", (identifier,))
    else:
        print("Invalid identifier type. Please provide an integer key or a string name.")

    conn.commit()
    conn.close()

# this should not be editable as allergen and nutrition are linked to ingredient
def edit_allergen_of_ingredient(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch and display the current technique for the recipe
    cursor.execute(
        "SELECT a_name "
        "FROM allergen "
        "JOIN ingredient ON a_allergenkey = i_allergenkey"
        "JOIN rein ON i_ingredientkey = ri_ingredientkey"
        "JOIN recipe ON ri_recipekey = r_recipekey WHERE r_recipekey = ?",
        (recipe_key,))
    current_allergens = cursor.fetchall()
    if current_techniques:
        for current_allergen in current_allergens:
            print(f"Current allergen for Recipe {recipe_key}: {current_allergen}")
    else:
        print(f"No technique found for Recipe {recipe_key}")
        return

    # Display all available techniques
    print("\nAvailable Techniques:")
    cursor.execute("SELECT a_allergenkey, a_name FROM allergen")
    available_allergens = cursor.fetchall()
    for available_allergen in available_allergens:
        print(f"{available_allergen[0]}: {available_allergen[1]}")

    # User input for new technique
    new_allergen = input("Enter new allergen name or key: ")

    # Determine if the input is a name or a key
    new_allergen_key = None
    if new_allergen.isdigit():
        new_allergen_key = int(new_technique)
    else:
        for key, name in available_allergens:
            if name.lower() == new_allergen.lower():
                new_allergen_key = key
                break

    if new_allergen_key is not None:
        # Update the recipe with the new technique

        conn.commit()
        print("Technique updated successfully.")
    else:
        print("Invalid technique. Please try again.")

    conn.close()


def edit_allergen():
    print("\nEdit Allergens")
    print("1. Add New Allergens")
    print("2. Delete Allergens")
    print("3. Return to Previous Menu")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_allergen()
    elif choice == '2':
        delete_allergen()
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")


def add_technique():
    conn = connect_db()
    cursor = conn.cursor()

    new_name = input("Enter technique name to be added: ")
    cursor.execute("INSERT INTO Technique (t_name) VALUES (?)", (new_name,))

    conn.commit()
    conn.close()


def delete_technique():
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('technique')
    identifier = input("Enter technique key/name to be deleted: ")

    # Check if the identifier is an integer (key) or string (name)
    if isinstance(identifier, int):
        cursor.execute("DELETE FROM technique WHERE t_techniquekey = ?", (identifier,))
    elif isinstance(identifier, str):
        cursor.execute("DELETE FROM technique WHERE t_name = ?", (identifier,))
    else:
        print("Invalid identifier type. Please provide an integer key or a string name.")

    conn.commit()
    conn.close()


def edit_technique_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch and display the current technique for the recipe
    cursor.execute(
        "SELECT t_name FROM recipe JOIN technique ON r_techniquekey = t_techniquekey WHERE r_recipekey = ?",
        (recipe_key,))
    current_technique = cursor.fetchone()
    if current_technique:
        print(f"Current technique for Recipe {recipe_key}: {current_technique[0]}")
    else:
        print(f"No technique found for Recipe {recipe_key}")
        return

    # Display all available techniques
    print("\nAvailable Techniques:")
    cursor.execute("SELECT t_techniquekey, t_name FROM technique")
    available_techniques = cursor.fetchall()
    for technique in available_techniques:
        print(f"{technique[0]}: {technique[1]}")

    # User input for new technique
    new_technique = input("Enter new technique name or key: ")

    # Determine if the input is a name or a key
    new_technique_key = None
    if new_technique.isdigit():
        new_technique_key = int(new_technique)
    else:
        for key, name in available_techniques:
            if name.lower() == new_technique.lower():
                new_technique_key = key
                break

    if new_technique_key is not None:
        # Update the recipe with the new technique
        cursor.execute("UPDATE recipe SET r_techniquekey = ? WHERE r_recipekey = ?", (new_technique_key, recipe_key))
        conn.commit()
        print("Technique updated successfully.")
    else:
        print("Invalid technique. Please try again.")

    conn.close()


def edit_technique():
    print("\nEdit Techniques")
    print("1. Add New Technique")
    print("2. Delete Technique")
    print("3. Return to Previous Menu")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_technique()
    elif choice == '2':
        delete_technique()
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please try again.")


def add_mealcourse(mealcourse_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Mealcourse (m_name) VALUES (?)", (mealcourse_name,))
    conn.commit()
    conn.close()

def delete_mealcourse(mealcourse_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the identifier is an integer (key) or string (name)
    if isinstance(identifier, int):
        cursor.execute("DELETE FROM mealcourse WHERE m_mealcoursekey = ?", (identifier,))
    elif isinstance(identifier, str):
        cursor.execute("DELETE FROM mealcourse WHERE m_name = ?", (identifier,))
    else:
        print("Invalid identifier type. Please provide an integer key or a string name.")

    conn.commit()
    conn.close()

def edit_mealcourse_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('mealcourse')
    new_mealcourse_key = input("Enter new mealcourse key: ")
    cursor.execute("UPDATE recipe SET r_mealcoursekey = ? WHERE r_recipekey = ?", (new_mealcourse_key, recipe_key))

    conn.commit()
    conn.close()


def edit_mealcourse():
    return


def add_cuisine():
    return


def delete_cuisine():
    return


def edit_cuisine():
    return


def edit_cuisine_of_recipe():
    return




def edit_recipe():
    display_choices('recipe')
    recipe_key = input("Enter the key of the recipe you want to edit: ")

    while True:
        print("\nEdit Recipe Options")
        print("1. Edit Recipe's Ingredients")
        # print("2. Edit Recipe's Allergens")
        # print("3. Edit Recipe's Nutrition Type")
        print("2. Edit Recipe's Technique")
        print("3. Edit Recipe's Cuisine")
        print("4. Edit Recipe's Meal Course")
        print("5. Return to Previous Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            edit_ingredients_of_recipe(recipe_key)
        elif choice == '2':
            edit_allergens_of_recipe(recipe_key)
        elif choice == '3':
            edit_nutrition_of_recipe(recipe_key)
        elif choice == '4':
            edit_technique_of_recipe(recipe_key)
        elif choice == '5':
            edit_cuisine_of_recipe(recipe_key)
        elif choice == '6':
            edit_meal_course_of_recipe(recipe_key)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")


def edit_menu():
    # each edit function should display its list of options to choose from to edit
    # then keys parameter will be passed in
    while True:
        print("\nEdit Menu")
        print("1. Edit Recipe")
        # edit ingredient provides options to also edit its corresponding nutrition and allergen
        print("2. Edit Ingredients")
        print("3. Edit Nutrition Types")
        print("4. Edit Allergens")
        print("5. Edit Techniques")
        print("6. Edit Meal Courses")
        print("7. Edit Cuisine")
        print("8. Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            recipe_key = input("Enter the recipe key to edit: ")
            edit_recipe()
        elif choice == '2':
            edit_ingredients()
        elif choice == '3':
            edit_ingredients()
        elif choice == '4':
            edit_ingredients()
        elif choice == '5':
            recipe_key = input("Enter the recipe key to edit: ")
            new_technique_key = input("Enter the new technique key: ")
            try:
                # Convert keys to integer and call the edit function
                edit_technique_of_recipe(int(recipe_key), int(new_technique_key))
                print("Recipe technique updated successfully.")
            except ValueError:
                print("Invalid input. Please enter valid numeric keys.")
        elif choice == '6':
            edit_ingredients()
        elif choice == '7':
            edit_ingredients()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")


# Interactive menu
def main_menu():
    while True:
        print("\nRecipeBook Database Management")
        print("1. Create Tables")
        print("2. Drop Table")
        # insert new recipe should add other necessary table info cuisine, mealcourse, technique, ingredients via rein
        print("3. Insert New Recipe")
        print("4. View All Recipes")
        print("5. Edit")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting the program.")
            break
        if choice == '1':
            create_tables()
            print("Tables created successfully.")
        elif choice == '2':
            table_name = input("Enter table name to drop: ")
            drop_table(table_name)
            print(f"Table {table_name} dropped successfully.")
        elif choice == '3':
            # Example data input
            recipe_data = (input("Enter recipe name: "),
                           int(input("Enter technique key: ")),
                           int(input("Enter cuisine key: ")),
                           int(input("Enter mealcourse key: ")),
                           input("Enter instructions: "))
            insert_recipe(recipe_data)
            print("New recipe inserted successfully.")
        elif choice == '4':
            view_all_recipes()
        elif choice == '5':
            edit_menu()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()

    # display list of choices available from each table to user for selection
    # insert recipe based on selections

    # add and delete nutrition type such as protein, fat or carb
    # check and edit nutrition type of a recipe

    # add and delete allergen
    # check and edit allergen of a recipe

    # add and delete cooking technique
    # check and edit technique required

    # add and delete meal course
    # check and edit mealcourse the recipe belongs to

    # add and delete cuisine
    # check and edit cuisine the recipe belongs to

    # add and delete ingredients
    # check and edit ingredients used by a recipe

    # the rein table should update correspondingly
    # one ri_recipekey could pair multiple different ingredient key


    # TODO:
    # add, delete, edit to recipe, edit functions for each table
    # get rid of parameter requirement for functions