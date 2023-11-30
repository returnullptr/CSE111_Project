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
def insert_recipe(recipe_data):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO Recipe (r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction)
                      VALUES (?, ?, ?, ?, ?)''', recipe_data)

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

    cursor.execute(f"SELECT * FROM {table_name}")
    items = cursor.fetchall()

    for item in items:
        print(item)

    conn.close()


def insert_recipe_interactive():
    # Display choices from each category and get user input
    print("Select a Technique:")
    display_choices('Technique')
    technique_key = input("Enter technique key: ")

    print("Select a Cuisine:")
    display_choices('Cuisine')
    cuisine_key = input("Enter cuisine key: ")

    print("Select a Meal Course:")
    display_choices('Mealcourse')
    mealcourse_key = input("Enter meal course key: ")

    recipe_name = input("Enter recipe name: ")
    instructions = input("Enter instructions: ")

    insert_recipe((recipe_name, technique_key, cuisine_key, mealcourse_key, instructions))


def add_nutrition(name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Nutrition (n_name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def delete_nutrition(key):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Nutrition WHERE n_nutritionkey = ?", (key,))

    conn.commit()
    conn.close()


def edit_nutrition(key, new_name):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE Nutrition SET n_name = ? WHERE n_nutritionkey = ?", (new_name, key))

    conn.commit()
    conn.close()


def view_nutrition():
    display_choices('Nutrition')


def add_ingredient_to_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO rein (ri_recipekey, ri_ingredientkey) VALUES (?, ?)", (recipe_key, ingredient_key))

    conn.commit()
    conn.close()


def delete_ingredient_from_recipe(recipe_key, ingredient_key):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM rein WHERE ri_recipekey = ? AND ri_ingredientkey = ?", (recipe_key, ingredient_key))

    conn.commit()
    conn.close()


def add_nutrition(nutrition_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Nutrition (n_name) VALUES (?)", (nutrition_name,))
    conn.commit()
    conn.close()

def delete_nutrition(nutrition_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Nutrition WHERE n_nutritionkey = ?", (nutrition_key,))
    conn.commit()
    conn.close()

def edit_nutrition_of_recipe(recipe_key, new_nutrition_key):
    # This assumes that the recipe table has a direct link to nutrition,
    # Modify as per your schema
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Recipe SET n_nutritionkey = ? WHERE r_recipekey = ?", (new_nutrition_key, recipe_key))
    conn.commit()
    conn.close()


def add_allergen(allergen_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Allergen (a_name) VALUES (?)", (allergen_name,))
    conn.commit()
    conn.close()

def delete_allergen(allergen_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Allergen WHERE a_allergenkey = ?", (allergen_key,))
    conn.commit()
    conn.close()

def edit_allergen_of_recipe(recipe_key, new_allergen_key):
    # Adjust as per your actual schema
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Ingredient SET i_allergenkey = ? WHERE i_ingredientkey IN (SELECT r_ingridentkey FROM rein WHERE ri_recipekey = ?)", (new_allergen_key, recipe_key))
    conn.commit()
    conn.close()


def add_technique(technique_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Technique (t_name) VALUES (?)", (technique_name,))
    conn.commit()
    conn.close()

def delete_technique(technique_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Technique WHERE t_techniquekey = ?", (technique_key,))
    conn.commit()
    conn.close()

def edit_technique_of_recipe(recipe_key, new_technique_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Recipe SET r_techniquekey = ? WHERE r_recipekey = ?", (new_technique_key, recipe_key))
    conn.commit()
    conn.close()


def add_mealcourse(mealcourse_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Mealcourse (m_name) VALUES (?)", (mealcourse_name,))
    conn.commit()
    conn.close()

def delete_mealcourse(mealcourse_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Mealcourse WHERE m_mealcoursekey = ?", (mealcourse_key,))
    conn.commit()
    conn.close()

def edit_mealcourse_of_recipe(recipe_key, new_mealcourse_key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Recipe SET r_mealcoursekey = ? WHERE r_recipekey = ?", (new_mealcourse_key, recipe_key))
    conn.commit()
    conn.close()


# Interactive menu
def main_menu():
    while True:
        print("\nRecipeBook Database Management")
        print("1. Create Tables")
        print("2. Drop Table")
        print("3. Insert New Recipe")
        print("4. View All Recipes")
        print("5. Exit")

        choice = input("Enter your choice: ")

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
            print("Exiting the program.")
            break
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