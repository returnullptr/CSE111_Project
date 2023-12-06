import sqlite3


# Function to connect to the SQLite database
def connect_db():
    try:
        conn = sqlite3.connect('recipe.sqlite')
        return conn
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None


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
                      ri_recipekey INTEGER, 
                      ri_ingredientkey INTEGER,
                      PRIMARY KEY (ri_recipekey, ri_ingredientkey))''')

    cursor.execute('''
        -- Inserting Techniques
        INSERT INTO technique (t_name)
        SELECT 'Slicing'
        WHERE NOT EXISTS (SELECT 1 FROM technique WHERE t_name = 'Slicing');
    ''')

    cursor.execute('''
        INSERT INTO technique (t_name)
        SELECT 'Frying'
        WHERE NOT EXISTS (SELECT 1 FROM technique WHERE t_name = 'Frying');
    ''')

    cursor.execute('''
        INSERT INTO technique (t_name)
        SELECT 'Grilling'
        WHERE NOT EXISTS (SELECT 1 FROM technique WHERE t_name = 'Grilling');
    ''')

    cursor.execute('''
        INSERT INTO technique (t_name)
        SELECT 'Boiling'
        WHERE NOT EXISTS (SELECT 1 FROM technique WHERE t_name = 'Boiling');
    ''')

    cursor.execute('''
        -- Inserting Cuisines
        INSERT INTO cuisine (c_name)
        SELECT 'Japanese'
        WHERE NOT EXISTS (SELECT 1 FROM cuisine WHERE c_name = 'Japanese');
    ''')

    cursor.execute('''
        INSERT INTO cuisine (c_name)
        SELECT 'Indian'
        WHERE NOT EXISTS (SELECT 1 FROM cuisine WHERE c_name = 'Indian');
    ''')

    cursor.execute('''
        INSERT INTO cuisine (c_name)
        SELECT 'Italian'
        WHERE NOT EXISTS (SELECT 1 FROM cuisine WHERE c_name = 'Italian');
    ''')

    cursor.execute('''
        INSERT INTO cuisine (c_name)
        SELECT 'American'
        WHERE NOT EXISTS (SELECT 1 FROM cuisine WHERE c_name = 'American');
    ''')

    cursor.execute('''
        -- Inserting Mealcourses
        INSERT INTO mealcourse (m_name)
        SELECT 'Dinner'
        WHERE NOT EXISTS (SELECT 1 FROM mealcourse WHERE m_name = 'Dinner');
    ''')

    cursor.execute('''
        INSERT INTO mealcourse (m_name)
        SELECT 'Lunch'
        WHERE NOT EXISTS (SELECT 1 FROM mealcourse WHERE m_name = 'Lunch');
    ''')

    cursor.execute('''
        -- Inserting Ingredients, Nutrition, and Allergens
        INSERT INTO nutrition (n_name)
        SELECT 'Protein'
        WHERE NOT EXISTS (SELECT 1 FROM nutrition WHERE n_name = 'Protein');
    ''')

    cursor.execute('''
        INSERT INTO nutrition (n_name)
        SELECT 'Carb'
        WHERE NOT EXISTS (SELECT 1 FROM nutrition WHERE n_name = 'Carb');
    ''')

    cursor.execute('''
        INSERT INTO nutrition (n_name)
        SELECT 'Fat'
        WHERE NOT EXISTS (SELECT 1 FROM nutrition WHERE n_name = 'Fat');
    ''')

    cursor.execute('''
        INSERT INTO allergen (a_name)
        SELECT 'Seafood'
        WHERE NOT EXISTS (SELECT 1 FROM allergen WHERE a_name = 'Seafood');
    ''')

    cursor.execute('''
        INSERT INTO allergen (a_name)
        SELECT 'Gluten'
        WHERE NOT EXISTS (SELECT 1 FROM allergen WHERE a_name = 'Gluten');
    ''')

    cursor.execute('''
        INSERT INTO allergen (a_name)
        SELECT 'Nuts'
        WHERE NOT EXISTS (SELECT 1 FROM allergen WHERE a_name = 'Nuts');
    ''')

    cursor.execute('''
        INSERT INTO allergen (a_name)
        SELECT 'Dairy'
        WHERE NOT EXISTS (SELECT 1 FROM allergen WHERE a_name = 'Dairy');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey) 
        SELECT 'Fish', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Protein'), 
        (SELECT a_allergenkey FROM allergen WHERE a_name = 'Seafood')
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Fish');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey) 
        SELECT 'Rice', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Carb'), 
        (SELECT a_allergenkey FROM allergen WHERE a_name = 'Gluten')
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Rice');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey)
        SELECT 'Chicken', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Protein'), 
        NULL
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Chicken');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey)
        SELECT 'Beef', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Protein'), 
        NULL
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Beef');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey)
        SELECT 'Veggies', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Carb'), 
        NULL
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Veggies');
    ''')

    cursor.execute('''
        INSERT INTO ingredient (i_name, i_nutritionkey, i_allergenkey)
        SELECT 'Butter', 
        (SELECT n_nutritionkey FROM nutrition WHERE n_name = 'Fat'), 
        (SELECT a_allergenkey FROM allergen WHERE a_name = 'Dairy')
        WHERE NOT EXISTS (SELECT 1 FROM ingredient WHERE i_name = 'Butter');
    ''')

    cursor.execute('''
        -- Inserting Recipes
        INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
        SELECT 'Chicken Katsu Rice', 
        (SELECT t_techniquekey FROM Technique WHERE t_name = 'Frying'), 
        (SELECT c_cuisinekey FROM Cuisine WHERE c_name = 'Japanese'), 
        (SELECT m_mealcoursekey FROM Mealcourse WHERE m_name = 'Lunch'), 
        'Fried chicken over rice'
        WHERE NOT EXISTS (SELECT 1 FROM Recipe WHERE r_name = 'Sushi');
    ''')

    cursor.execute('''
        INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
        SELECT 'Sushi', 
        (SELECT t_techniquekey FROM Technique WHERE t_name = 'Slicing'), 
        (SELECT c_cuisinekey FROM Cuisine WHERE c_name = 'Japanese'), 
        (SELECT m_mealcoursekey FROM Mealcourse WHERE m_name = 'Dinner'), 
        'Put the fish on rice'
        WHERE NOT EXISTS (SELECT 1 FROM Recipe WHERE r_name = 'Sushi');
    ''')

    cursor.execute('''
        INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
        SELECT 'Beef Curry', 
       (SELECT t_techniquekey FROM technique WHERE t_name = 'Boiling'), 
       (SELECT c_cuisinekey FROM cuisine WHERE c_name = 'Indian'), 
       (SELECT m_mealcoursekey FROM mealcourse WHERE m_name = 'Lunch'), 
       'Boil beef with veggies'
        WHERE NOT EXISTS (SELECT 1 FROM Recipe WHERE r_name = 'Beef Curry');
    ''')

    cursor.execute('''
        INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
        SELECT 'Grilled Steak', 
       (SELECT t_techniquekey FROM technique WHERE t_name = 'Grilling'), 
       (SELECT c_cuisinekey FROM cuisine WHERE c_name = 'American'), 
       (SELECT m_mealcoursekey FROM mealcourse WHERE m_name = 'Dinner'), 
       'Cook steak on a grill'
        WHERE NOT EXISTS (SELECT 1 FROM Recipe WHERE r_name = 'Grilled Steak');
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM Recipe WHERE r_name = 'Sushi'), 
            (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Fish')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Sushi')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Fish')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM Recipe WHERE r_name = 'Sushi'), 
            (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Rice')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Sushi')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Rice')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM Recipe WHERE r_name = 'Chicken Katsu Rice'), 
            (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Chicken')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Chicken Katsu Rice')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Chicken')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM Recipe WHERE r_name = 'Chicken Katsu Rice'), 
            (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Rice')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Chicken Katsu Rice')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Rice')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM recipe WHERE r_name = 'Beef Curry'),
            (SELECT i_ingredientkey FROM ingredient WHERE i_name = 'Beef')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Beef Curry')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Beef')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM recipe WHERE r_name = 'Beef Curry'),
            (SELECT i_ingredientkey FROM ingredient WHERE i_name = 'Veggies')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Beef Curry')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Veggies')
        );
    ''')

    cursor.execute('''
        INSERT INTO rein (ri_recipekey, ri_ingredientkey)
        SELECT 
            (SELECT r_recipekey FROM recipe WHERE r_name = 'Grilled Steak'),
            (SELECT i_ingredientkey FROM ingredient WHERE i_name = 'Beef')
        WHERE NOT EXISTS (
            SELECT 1 FROM rein 
            WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Grilled Steak')
            AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Beef')
        );
    ''')

    cursor.execute('''
            INSERT INTO rein (ri_recipekey, ri_ingredientkey)
            SELECT 
                (SELECT r_recipekey FROM recipe WHERE r_name = 'Grilled Steak'),
                (SELECT i_ingredientkey FROM ingredient WHERE i_name = 'Butter')
            WHERE NOT EXISTS (
                SELECT 1 FROM rein 
                WHERE ri_recipekey = (SELECT r_recipekey FROM Recipe WHERE r_name = 'Grilled Steak')
                AND ri_ingredientkey = (SELECT i_ingredientkey FROM Ingredient WHERE i_name = 'Butter')
            );
        ''')

    conn.commit()
    conn.close()


def show_all_tables():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Function to drop a table
def drop_table(table_name):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone():
        cursor.execute(f"DROP TABLE {table_name}")
        print(f"Table '{table_name}' dropped successfully.")
    else:
        print(f"Table '{table_name}' does not exist.")

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
        cursor.execute('''INSERT INTO rein (ri_recipekey, ri_ingredientkey) 
                          VALUES (?, ?)''', (recipe_key, ingredient_key))

    conn.commit()
    conn.close()


# Function to view all recipes (Example of a select operation)
def view_all_recipes():
    conn = connect_db()
    cursor = conn.cursor()

    # Correct the SQL query
    try:
        cursor.execute("""
            SELECT r_recipekey, r_name AS recipe, r_instruction AS instruction, 
                   c_name AS cuisine, t_name AS technique, m_name AS mealcourse
            FROM recipe
            JOIN cuisine ON recipe.r_cuisinekey = cuisine.c_cuisinekey
            JOIN technique ON recipe.r_techniquekey = technique.t_techniquekey
            JOIN mealcourse ON recipe.r_mealcoursekey = mealcourse.m_mealcoursekey
            ORDER BY r_recipekey
        """)
        recipes = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None

    for recipe in recipes:
        print(recipe[0], "Recipe:", recipe[1], " | Instructions:", recipe[2], " | Cuisine:", recipe[3],
              " | Technique:", recipe[4], " | Meal Course:", recipe[5])

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
    recipe_name = input("Enter recipe name: ")

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

    # # nutrition and allergen are linked with ingredients
    # print("Select a Nutrition Type:")
    # display_choices('nutrition')
    # nutrition_key = input("Enter nutrition type key: ")
    #
    # print("Select a Allergen:")
    # display_choices('allergen')
    # allergen_key = input("Enter allergen key: ")

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

    instructions = input("Enter instructions: ")

    insert_recipe((recipe_name, technique_key, cuisine_key, mealcourse_key, instructions), ingredient_keys)


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

    # Check if ingredient exists
    if identifier.isdigit():
        cursor.execute("SELECT * FROM ingredient WHERE i_ingredientkey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM ingredient WHERE i_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print("Ingredient not found. Please enter a valid key or name.")
    else:
        if identifier.isdigit():
            cursor.execute("DELETE FROM ingredient WHERE i_ingredientkey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM ingredient WHERE i_name = ?", (identifier,))

        conn.commit()
        print("Ingredient deleted successfully.")

    conn.close()


def edit_ingredient():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Ingredients")
    # Give options to edit
    print("1. Add Ingredient")
    print("2. Delete Ingredient")
    print("3. Edit Ingredient Name")
    print("4. Edit Nutrition Type")
    print("5. Edit Allergen Type")
    print("6. Return to Previous Menu")

    choice = input("Choose an option: ")

    if choice == '1':
        add_ingredient()
    elif choice == '2':
        delete_ingredient()
    elif choice == '6':
        conn.close()
        return
    else:
        # Display all ingredients
        display_choices('ingredient')
        ingredient_key = input("Enter the key of the ingredient to edit: ")

        # Validate the ingredient key
        cursor.execute("SELECT * FROM ingredient WHERE i_ingredientkey = ?", (ingredient_key,))
        if cursor.fetchone() is None:
            print("Invalid ingredient key. Please enter a valid key.")
            conn.close()
            return

        if choice == '3':
            new_name = input("Enter the new name for the ingredient: ")
            cursor.execute("UPDATE ingredient SET i_name = ? WHERE i_ingredientkey = ?", (new_name, ingredient_key))
            print("Ingredient name updated successfully.")
        elif choice in ['4', '5']:
            if choice == '4':
                # display_choices('nutrition')
                table_name = 'nutrition'
                column_name = 'i_nutritionkey'
            else:
                # display_choices('allergen')
                table_name = 'allergen'
                column_name = 'i_allergenkey'

            # Fetch and display the current nutrition/allergen of the ingredient
            cursor.execute(f"SELECT {column_name} FROM ingredient WHERE i_ingredientkey = ?", (ingredient_key,))
            current_attr = cursor.fetchone()
            if current_attr:
                cursor.execute(f"SELECT {table_name[0]}_name FROM {table_name} WHERE {table_name[0]}_{table_name}key = ?",
                               (current_attr[0],))
                current_attr_name = cursor.fetchone()
                print(
                    f"Current {table_name} for this ingredient: {current_attr_name[0] if current_attr_name else 'None'}")
            else:
                print(f"Ingredient does not have a current {table_name}.")

            # Display available options
            display_choices(table_name)

            new_key = input(f"Enter the new {table_name} key (enter 0 for none): ")

            # Validate the new key if it's not '0'
            if new_key != '0':
                cursor.execute(f"SELECT * FROM {table_name} WHERE {table_name[0]}_{table_name}key = ?", (new_key,))
                if cursor.fetchone() is None:
                    print(f"Invalid {table_name} key. Please enter a valid key.")
                    conn.close()
                    return

            column_name = f"i_{table_name}key"
            cursor.execute(f"UPDATE ingredient SET {column_name} = ? WHERE i_ingredientkey = ?",
                           (new_key if new_key != '0' else None, ingredient_key))
            print(f"{table_name.capitalize()} type updated successfully.")
        else:
            print("Invalid option selected.")

    conn.commit()
    conn.close()
    # print("Ingredient updated successfully.")


def add_ingredient_to_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Insert the ingredient into the rein table linked with the recipe
    cursor.execute("INSERT INTO rein (ri_recipekey, ri_ingredientkey) VALUES (?, ?)", (recipe_key, ingredient_key))

    conn.commit()
    conn.close()
    print("Ingredient added to recipe successfully.")


def delete_ingredient_from_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the ingredient exists in the recipe
    cursor.execute("SELECT * FROM rein WHERE ri_recipekey = ? AND ri_ingredientkey = ?", (recipe_key, ingredient_key))
    if cursor.fetchone() is None:
        print("No such ingredient found in the specified recipe.")
    else:
        # If the ingredient exists, delete it
        cursor.execute("DELETE FROM rein WHERE ri_recipekey = ? AND ri_ingredientkey = ?", (recipe_key, ingredient_key))
        conn.commit()
        print("Ingredient removed from recipe successfully.")

    conn.commit()
    conn.close()


def edit_ingredients_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the recipe exists
    cursor.execute("SELECT * FROM recipe WHERE r_recipekey = ?", (recipe_key,))
    if cursor.fetchone() is None:
        print(f"No recipe found with key {recipe_key}.")
        conn.close()
        return

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

        # Check if the ingredient exists
        cursor.execute("SELECT * FROM ingredient WHERE i_ingredientkey = ?", (ingredient_key,))
        if cursor.fetchone() is None:
            # print(f"No ingredient found with key {ingredient_key}.")
            print("Please try again!")
        else:
            add_ingredient_to_recipe(recipe_key, ingredient_key)
            print("Ingredient added to recipe successfully.")
    elif choice == '2':
        ingredient_key = input("Enter the ingredient key to remove: ")

        # Check if the ingredient is part of the recipe
        cursor.execute("SELECT * FROM rein WHERE ri_recipekey = ? AND ri_ingredientkey = ?", (recipe_key, ingredient_key))
        if cursor.fetchone() is None:
            print(f"No ingredient found with key {ingredient_key} in recipe {recipe_key}.")
            print("Please try again!")
        else:
            delete_ingredient_from_recipe(recipe_key, ingredient_key)
            # print("Ingredient removed from recipe successfully.")
    else:
        print("Invalid option selected.")

    conn.close()


def add_nutrition():
    conn = connect_db()
    cursor = conn.cursor()

    # Prompt user to enter ingredient name
    nutrition_name = input("Enter the name of the new nutrition: ")
    cursor.execute("INSERT INTO nutrition (n_name) VALUES (?)", (nutrition_name,))

    conn.commit()
    conn.close()

    print("Nutrition added successfully.")


def delete_nutrition():
    conn = connect_db()
    cursor = conn.cursor()

    # Display all nutritions
    display_choices('nutrition')

    # Prompt user to enter nutrition key or name to be deleted
    identifier = input("Enter the nutrition key or name to delete: ")

    # Check if the nutrition item exists before attempting deletion
    if identifier.isdigit():
        cursor.execute("SELECT * FROM nutrition WHERE n_nutritionkey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM nutrition WHERE n_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print(f"No nutrition found with identifier '{identifier}'. Please enter a valid key or name.")
    else:
        # If the nutrition item exists, proceed with deletion
        if identifier.isdigit():
            cursor.execute("DELETE FROM nutrition WHERE n_nutritionkey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM nutrition WHERE n_name = ?", (identifier,))
        conn.commit()
        print(f"Nutrition '{identifier}' deleted successfully.")

    conn.close()


def edit_nutrition():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Nutritions")
    # Give options to edit
    print("1. Add Nutrition")
    print("2. Delete Nutrition")
    print("3. Edit Nutrition Name")
    print("4. Return to Previous Menu")
    choice = input("Choose an option: ")

    if choice == '1':
        add_nutrition()
    elif choice == '2':
        delete_nutrition()
    elif choice == '3':
        # Display all nutrition types
        display_choices('nutrition')

        # Let user choose which nutrition to edit
        nutrition_key = input("Enter the key of the nutrition to edit: ")

        # Check if the nutrition exists
        cursor.execute("SELECT * FROM nutrition WHERE n_nutritionkey = ?", (nutrition_key,))
        if cursor.fetchone() is None:
            print(f"No nutrition found with key {nutrition_key}. Please enter a valid key.")
        else:
            new_name = input("Enter the new name for the nutrition type: ")
            cursor.execute("UPDATE nutrition SET n_name = ? WHERE n_nutritionkey = ?", (new_name, nutrition_key))
            print("Nutrition name updated successfully.")
    elif choice == '4':
        conn.close()
        return
    else:
        print("Invalid choice. Please try again.")

    conn.commit()
    conn.close()


# def edit_nutrition_of_ingredient(recipe_key, new_nutrition_key):
#     # This assumes that the recipe table has a direct link to nutrition,
#     # Modify as per your schema
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE Recipe SET n_nutritionkey = ? WHERE r_recipekey = ?", (new_nutrition_key, recipe_key))
#     conn.commit()
#     conn.close()


# def view_nutrition():
#     display_choices('nutrition')


def add_allergen():
    conn = connect_db()
    cursor = conn.cursor()

    # Prompt user to enter allergen name
    allergen_name = input("Enter the name of the new allergen: ")
    cursor.execute("INSERT INTO allergen (a_name) VALUES (?)", (allergen_name,))

    conn.commit()
    conn.close()

    print("Allergen added successfully.")


def delete_allergen():
    conn = connect_db()
    cursor = conn.cursor()

    # Display all allergens
    display_choices('allergen')

    # Prompt user to enter allergen key or name to be deleted
    identifier = input("Enter the allergen key or name to delete: ")

    # Check if the allergen item exists before attempting deletion
    if identifier.isdigit():
        cursor.execute("SELECT * FROM allergen WHERE a_allergenkey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM allergen WHERE a_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print(f"No allergen found with identifier '{identifier}'. Please enter a valid key or name.")
    else:
        # Check if the identifier is an integer (key) or string (name)
        if identifier.isdigit():
            cursor.execute("DELETE FROM allergen WHERE a_allergenkey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM allergen WHERE a_name = ?", (identifier,))
        conn.commit()
        print(f"Allergen '{identifier}' deleted successfully.")

    conn.close()


def edit_allergen():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Allergens")
    print("1. Add New Allergens")
    print("2. Delete Allergens")
    print("3. Edit Allergen Name")
    print("4. Return to Previous Menu")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_allergen()
    elif choice == '2':
        delete_allergen()
    elif choice == '3':
        # Display all nutrition types
        display_choices('allergen')

        # Let user choose which nutrition to edit
        allergen_key = input("Enter the key of the allergen to edit: ")

        # Check if the nutrition exists
        cursor.execute("SELECT * FROM allergen WHERE a_allergenkey = ?", (allergen_key,))
        if cursor.fetchone() is None:
            print(f"No allergen found with key {allergen_key}. Please enter a valid key.")
        else:
            new_name = input("Enter the new name for the allergen: ")
            cursor.execute("UPDATE allergen SET a_name = ? WHERE a_allergenkey = ?", (new_name, allergen_key))
            print("Allergen name updated successfully.")
    elif choice == '4':
        return
    else:
        print("Invalid choice. Please try again.")

    conn.commit()
    conn.close()


# # this should not be editable as allergen and nutrition are linked to ingredient
# def edit_allergen_of_ingredient(recipe_key):
#     return


def add_technique():
    conn = connect_db()
    cursor = conn.cursor()

    new_name = input("Enter the name of the new technique: ")
    cursor.execute("INSERT INTO technique (t_name) VALUES (?)", (new_name,))

    conn.commit()
    conn.close()

    print("Technique added successfully.")


def delete_technique():
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('technique')
    identifier = input("Enter technique key or name to delete: ")

    if identifier.isdigit():
        cursor.execute("SELECT * FROM technique WHERE t_techniquekey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM technique WHERE t_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print(f"No technique found with identifier '{identifier}'.")
    else:
        if identifier.isdigit():
            cursor.execute("DELETE FROM technique WHERE t_techniquekey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM technique WHERE t_name = ?", (identifier,))
        conn.commit()
        print("Technique deleted successfully.")

    conn.close()


def edit_technique():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Techniques")
    print("1. Add New Technique")
    print("2. Delete Technique")
    print("3. Edit Technique Name")
    print("4. Return to Previous Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_technique()
    elif choice == '2':
        delete_technique()
    elif choice == '3':
        display_choices('technique')
        technique_key = input("Enter the key of the technique to edit: ")

        cursor.execute("SELECT * FROM technique WHERE t_techniquekey = ?", (technique_key,))
        if cursor.fetchone() is None:
            print(f"No technique found with key {technique_key}.")
        else:
            new_name = input("Enter the new name for the technique: ")
            cursor.execute("UPDATE technique SET t_name = ? WHERE t_techniquekey = ?", (new_name, technique_key))
            conn.commit()
            print("Technique name updated successfully.")
    elif choice == '4':
        conn.close()
        return
    else:
        print("Invalid choice. Please try again.")

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
        # return

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
        # Check if the entered technique key exists
        cursor.execute("SELECT * FROM technique WHERE t_techniquekey = ?", (new_technique_key,))
        if cursor.fetchone() is None:
            print(f"No technique found with key {new_technique_key}. Please enter a valid technique key.")
        else:
            # Update the recipe with the new technique
            cursor.execute("UPDATE recipe SET r_techniquekey = ? WHERE r_recipekey = ?",
                           (new_technique_key, recipe_key))
            conn.commit()
            print("Technique updated successfully.")
    else:
        print("Invalid technique. Please try again.")

    conn.close()


def add_mealcourse():
    conn = connect_db()
    cursor = conn.cursor()

    new_name = input("Enter the name of the new mealcourse: ")
    cursor.execute("INSERT INTO Mealcourse (m_name) VALUES (?)", (new_name,))

    conn.commit()
    conn.close()

    print("Meal course added successfully.")


def delete_mealcourse():
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('mealcourse')
    identifier = input("Enter mealcourse key or name to delete: ")

    if identifier.isdigit():
        cursor.execute("SELECT * FROM mealcourse WHERE m_mealcoursekey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM mealcourse WHERE m_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print(f"No meal course found with identifier '{identifier}'.")
    else:
        if identifier.isdigit():
            cursor.execute("DELETE FROM mealcourse WHERE m_mealcoursekey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM mealcourse WHERE m_name = ?", (identifier,))
        conn.commit()
        print("Meal course deleted successfully.")

    conn.close()


def edit_mealcourse():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Meal Course")
    print("1. Add New Meal Course")
    print("2. Delete Meal Course")
    print("3. Edit Meal Course Name")
    print("4. Return to Previous Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_mealcourse()
    elif choice == '2':
        delete_mealcourse()
    elif choice == '3':
        display_choices('mealcourse')
        mealcourse_key = input("Enter the key of the meal course to edit: ")

        # Check if the meal course exists
        cursor.execute("SELECT * FROM mealcourse WHERE m_mealcoursekey = ?", (mealcourse_key,))
        if cursor.fetchone() is None:
            print(f"No meal course found with key {mealcourse_key}.")
        else:
            new_name = input("Enter the new name for the meal course: ")
            cursor.execute("UPDATE mealcourse SET m_name = ? WHERE m_mealcoursekey = ?", (new_name, mealcourse_key))
            conn.commit()
            print("Meal course name updated successfully.")
    elif choice == '4':
        conn.close()
        return
    else:
        print("Invalid choice. Please try again.")

    conn.close()


def edit_mealcourse_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch and display the current technique for the recipe
    cursor.execute(
        "SELECT m_name FROM recipe JOIN mealcourse ON r_mealcoursekey = m_mealcoursekey WHERE r_recipekey = ?",
        (recipe_key,))
    current_mealcourse = cursor.fetchone()
    if current_mealcourse:
        print(f"Current meal course for Recipe {recipe_key}: {current_mealcourse[0]}")
    else:
        print(f"No meal course found for Recipe {recipe_key}")
        # return

    # Display all available meal courses
    print("\nAvailable meal courses:")
    cursor.execute("SELECT m_mealcoursekey, m_name FROM mealcourse")
    available_mealcourses = cursor.fetchall()
    for mealcourse in available_mealcourses:
        print(f"{mealcourse[0]}: {mealcourse[1]}")

    # User input for new technique
    new_mealcourse = input("Enter new meal course name or key: ")

    # Determine if the input is a name or a key
    new_mealcourse_key = None
    if new_mealcourse.isdigit():
        new_mealcourse_key = int(new_mealcourse)
    else:
        for key, name in available_mealcourses:
            if name.lower() == new_mealcourse.lower():
                new_mealcourse_key = key
                break

    if new_mealcourse_key is not None:
        # Check if the entered mealcourse key exists
        cursor.execute("SELECT * FROM mealcourse WHERE m_mealcoursekey = ?", (new_mealcourse_key,))
        if cursor.fetchone() is None:
            print(f"No meal course found with key {new_mealcourse_key}. Please enter a valid meal course key.")
        else:
            # Update the recipe with the new meal course
            cursor.execute("UPDATE recipe SET r_mealcoursekey = ? WHERE r_recipekey = ?",
                           (new_mealcourse_key, recipe_key))
            conn.commit()
            print("Meal course updated successfully.")
    else:
        print("Invalid meal course. Please try again.")

    conn.close()


def add_cuisine():
    conn = connect_db()
    cursor = conn.cursor()

    new_name = input("Enter the name of the new cuisine: ")
    cursor.execute("INSERT INTO cuisine (c_name) VALUES (?)", (new_name,))

    conn.commit()
    conn.close()
    print("Cuisine added successfully.")


def delete_cuisine():
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('cuisine')
    identifier = input("Enter cuisine key or name to delete: ")

    if identifier.isdigit():
        cursor.execute("SELECT * FROM cuisine WHERE c_cuisinekey = ?", (int(identifier),))
    else:
        cursor.execute("SELECT * FROM cuisine WHERE c_name = ?", (identifier,))

    if cursor.fetchone() is None:
        print(f"No cuisine found with identifier '{identifier}'.")
    else:
        if identifier.isdigit():
            cursor.execute("DELETE FROM cuisine WHERE c_cuisinekey = ?", (int(identifier),))
        else:
            cursor.execute("DELETE FROM cuisine WHERE c_name = ?", (identifier,))
        conn.commit()
        print("Cuisine deleted successfully.")

    conn.close()


def edit_cuisine():
    conn = connect_db()
    cursor = conn.cursor()

    print("\nEdit Cuisine")
    print("1. Add New Cuisine")
    print("2. Delete Cuisine")
    print("3. Edit Cuisine Name")
    print("4. Return to Previous Menu")
    choice = input("Enter your choice: ")

    if choice == '1':
        add_cuisine()
    elif choice == '2':
        delete_cuisine()
    elif choice == '3':
        display_choices('cuisine')
        cuisine_key = input("Enter the key of the cuisine to edit: ")

        cursor.execute("SELECT * FROM cuisine WHERE c_cuisinekey = ?", (cuisine_key,))
        if cursor.fetchone() is None:
            print(f"No cuisine found with key {cuisine_key}.")
        else:
            new_name = input("Enter the new name for the cuisine: ")
            cursor.execute("UPDATE cuisine SET c_name = ? WHERE c_cuisinekey = ?", (new_name, cuisine_key))
            conn.commit()
            print("Cuisine name updated successfully.")
    elif choice == '4':
        conn.close()
        return
    else:
        print("Invalid choice. Please try again.")

    conn.close()


def edit_cuisine_of_recipe(recipe_key):
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch and display the current cuisine for the recipe
    cursor.execute("SELECT c_name FROM recipe JOIN cuisine ON r_cuisinekey = c_cuisinekey WHERE r_recipekey = ?", (recipe_key,))
    current_cuisine = cursor.fetchone()

    if current_cuisine:
        print(f"Current cuisine for Recipe {recipe_key}: {current_cuisine[0]}")
    else:
        print(f"No cuisine found for Recipe {recipe_key}")
        # return

    # Display all available cuisines
    print("\nAvailable cuisines:")
    cursor.execute("SELECT c_cuisinekey, c_name FROM cuisine")
    available_cuisines = cursor.fetchall()

    for cuisine in available_cuisines:
        print(f"{cuisine[0]}: {cuisine[1]}")

    # User input for new cuisine
    new_cuisine = input("Enter new cuisine name or key: ")

    # Determine if the input is a name or a key
    new_cuisine_key = None
    if new_cuisine.isdigit():
        new_cuisine_key = int(new_cuisine)
    else:
        for key, name in available_cuisines:
            if name.lower() == new_cuisine.lower():
                new_cuisine_key = key
                break

    if new_cuisine_key is not None:
        # Check if the entered cuisine key exists
        cursor.execute("SELECT * FROM cuisine WHERE c_cuisinekey = ?", (new_cuisine_key,))
        if cursor.fetchone() is None:
            print(f"No cuisine found with key {new_cuisine_key}. Please enter a valid cuisine key.")
        else:
            # Update the recipe with the new cuisine
            cursor.execute("UPDATE recipe SET r_cuisinekey = ? WHERE r_recipekey = ?", (new_cuisine_key, recipe_key))
            conn.commit()
            print("Cuisine updated successfully.")
    else:
        print("Invalid cuisine. Please try again.")

    conn.close()


def find_recipes_by_ingredient():
    conn = connect_db()
    cursor = conn.cursor()

    print('Available ingredients:\n')
    display_choices('ingredient')

    identifier = input("Enter the ingredient key or name to search for recipes: ")

    if identifier.isdigit():
        cursor.execute("""
            SELECT r_name
            FROM recipe
            JOIN rein ON r_recipekey = ri_recipekey
            WHERE ri_ingredientkey = ?
        """, (int(identifier),))
    else:
        cursor.execute("""
            SELECT r_name
            FROM recipe
            JOIN rein ON r_recipekey = ri_recipekey
            JOIN ingredient ON ri_ingredientkey = i_ingredientkey
            WHERE i_name = ?
        """, (identifier,))

    recipes = cursor.fetchall()
    if recipes:
        print(f"Recipes containing '{identifier}':")
        for recipe in recipes:
            print(recipe[0])
    else:
        print(f"No recipes found containing '{identifier}'")

    conn.close()


def total_recipes_per_cuisine():
    conn = connect_db()
    cursor = conn.cursor()

    print('available cuisines\n')
    display_choices('cuisine')

    cursor.execute("""
        SELECT c_name, Count(*) AS NumberOfRecipes
        FROM recipe
        JOIN cuisine ON r_cuisinekey = c_cuisinekey
        GROUP BY c_name
    """)

    cuisine_counts = cursor.fetchall()
    print("Number of Recipes per Cuisine:")
    for cuisine, count in cuisine_counts:
        print(f"{cuisine}: {count}")

    conn.close()


def display_nutrition_allergen_info():
    conn = connect_db()
    cursor = conn.cursor()

    display_choices('recipe')

    identifier = input("Enter the recipe key or name: ")
    recipe_key = None

    # Check if the identifier is a key (integer) or a name (string)
    if identifier.isdigit():
        cursor.execute("SELECT r_recipekey FROM recipe WHERE r_recipekey = ?", (int(identifier),))
        recipe = cursor.fetchone()
        if recipe:
            recipe_key = recipe[0]
    else:
        cursor.execute("SELECT r_recipekey FROM recipe WHERE r_name = ?", (identifier,))
        recipe = cursor.fetchone()
        if recipe:
            recipe_key = recipe[0]

    if not recipe_key:
        print(f"No recipe found with identifier '{identifier}'.")
        conn.close()
        return

    # Fetch and display nutrition and allergen info
    cursor.execute("""
        SELECT ingredient.i_name, nutrition.n_name, allergen.a_name
        FROM rein 
        JOIN ingredient ON ri_ingredientkey = i_ingredientkey
        LEFT JOIN nutrition ON i_nutritionkey = n_nutritionkey
        LEFT JOIN allergen ON i_allergenkey = a_allergenkey
        WHERE ri_recipekey = ?
    """, (recipe_key,))

    print(f"\nNutrition and Allergen Information for Recipe {identifier}:")
    for ingredient, nutrition, allergen in cursor.fetchall():
        allergen_info = allergen if allergen else "None"
        nutrition_info = nutrition if nutrition else "None"
        print(f"Ingredient: {ingredient}, Nutrition: {nutrition_info}, Allergen: {allergen_info}")

    conn.close()


def ingredients_per_technique():
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT t_name AS technique, GROUP_CONCAT(DISTINCT(i_name)) AS ingredients
            FROM technique
            JOIN recipe ON technique.t_techniquekey = recipe.r_techniquekey
            JOIN rein ON recipe.r_recipekey = rein.ri_recipekey
            JOIN ingredient ON rein.ri_ingredientkey = ingredient.i_ingredientkey
            GROUP BY t_name
        """)
        results = cursor.fetchall()
        for technique, ingredients in results:
            print(f"Technique: {technique}, Ingredients: {ingredients}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def edit_recipe():
    display_choices('recipe')
    recipe_key = input("Enter the key of the recipe you want to edit: ")

    while True:
        print("\nEdit Recipe Options")
        print("1. Edit Recipe's Ingredients")
        print("2. Edit Recipe's Technique")
        print("3. Edit Recipe's Cuisine")
        print("4. Edit Recipe's Meal Course")
        print("5. Return to Previous Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            edit_ingredients_of_recipe(recipe_key)
        elif choice == '2':
            edit_technique_of_recipe(recipe_key)
        elif choice == '3':
            edit_cuisine_of_recipe(recipe_key)
        elif choice == '4':
            edit_mealcourse_of_recipe(recipe_key)
        elif choice == '5':
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
            edit_recipe()
        elif choice == '2':
            edit_ingredient()
        elif choice == '3':
            edit_nutrition()
        elif choice == '4':
            edit_allergen()
        elif choice == '5':
            edit_technique()
        elif choice == '6':
            edit_mealcourse()
        elif choice == '7':
            edit_cuisine()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")


# Interactive menu
def main_menu():
    while True:
        print("\nRecipeBook Database Management")
        print("1. Display Tables")
        print("2. Create Tables")
        print("3. Drop Table")
        # insert new recipe should add other necessary table info cuisine, mealcourse, technique, ingredients via rein
        print("4. Insert New Recipe")
        print("5. View All Recipes")
        print("6. Find Recipes by Ingredient")
        print("7. Display Total Recipes Per Cuisine")
        print("8. Display Nutrition and Allergen by Recipe")
        print("9. Display Ingredients Used Per Technique")
        print("10. Edit Menu")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting the program.")
            break

        if choice == '1':
            show_all_tables()
        elif choice == '2':
            create_tables()
            print("Tables created successfully.")
        elif choice == '3':
            show_all_tables()
            table_name = input("Enter table name to drop: ")
            drop_table(table_name)
            # print(f"Table {table_name} dropped successfully.")
        elif choice == '4':
            # Example data input
            # recipe_data = (input("Enter recipe name: "),
            #                int(input("Enter technique key: ")),
            #                int(input("Enter cuisine key: ")),
            #                int(input("Enter mealcourse key: ")),
            #                input("Enter instructions: "))
            insert_recipe_interactive()
            print("New recipe inserted successfully.")
        elif choice == '5':
            view_all_recipes()
        elif choice == '6':
            find_recipes_by_ingredient()
        elif choice == '7':
            total_recipes_per_cuisine()
        elif choice == '8':
            display_nutrition_allergen_info()
        elif choice == '9':
            ingredients_per_technique()
        elif choice =='10':
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
    # error handling: valid choice and feedback
    # handle redundant table info
    # new: generate real life recipes load into database using sql statements when create table