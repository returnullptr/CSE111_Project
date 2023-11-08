DELETE FROM recipe;
DELETE FROM nutrition;
DELETE FROM cuisine;
DELETE FROM allergen;
DELETE FROM mealcourse;
DELETE FROM technique;
DELETE FROM ingredient;
DELETE FROM rein;



INSERT INTO nutrition(n_nutritionkey, n_name) VALUES ( 1, 'protein');
INSERT INTO nutrition(n_nutritionkey, n_name) VALUES ( 2, 'carbs');
INSERT INTO nutrition(n_nutritionkey, n_name) VALUES ( 3, 'fat');

INSERT INTO cuisine(c_cuisinekey, c_name) VALUES (1, 'japanese');
INSERT INTO cuisine(c_cuisinekey, c_name) VALUES (2, 'Chinese');

INSERT INTO allergen(a_allergenkey, a_name) VALUES (1, 'seafood' );
INSERT INTO allergen(a_allergenkey, a_name) VALUES (2, 'Diary');
INSERT INTO allergen(a_allergenkey, a_name) VALUES (3, 'nut');
INSERT INTO allergen(a_allergenkey, a_name) VALUES (4, 'gluten');


INSERT INTO mealcourse(m_mealcoursekey, m_name) VALUES (1, 'dinner');
INSERT INTO mealcourse(m_mealcoursekey, m_name) VALUES (2, 'lunch');
INSERT INTO mealcourse(m_mealcoursekey, m_name) VALUES (3, 'Dessert');

SELECT * 
FROM mealcourse;

DELETE FROM mealcourse WHERE m_name = 'Dessert';

SELECT * 
FROM mealcourse


INSERT INTO technique(t_techniquekey, t_name) VALUES (1, 'Slicing');
INSERT INTO technique(t_techniquekey, t_name) VALUES (2, 'Grilling');
INSERT INTO technique(t_techniquekey, t_name) VALUES (3, 'Baking');


INSERT INTO recipe (r_recipekey, r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey) VALUES (2, 'chicken curry', 1, 1, 1);
INSERT INTO recipe (r_recipekey, r_name, r_techniquekey, r_cuisinekey, r_mealcoursekey, r_instruction) VALUES (1,'sushi',1,2,1,'put the fish on rice');

SELECT * 
FROM recipe;
UPDATE recipe SET r_cuisinekey = 1 WHERE r_recipekey = 1;
UPDATE recipe SET r_name = 'beef curry' WHERE r_name = 'chicken curry';
SELECT * 
FROM recipe;

INSERT INTO ingredient(i_ingredientkey, i_name, i_allergenkey, i_nutritionkey) VALUES (1, 'almond', 3, 3);
INSERT INTO ingredient(i_ingredientkey, i_name, i_allergenkey, i_nutritionkey) VALUES (2, 'cheese', 2, 1);
INSERT INTO ingredient(i_ingredientkey, i_name, i_allergenkey, i_nutritionkey) VALUES(3, 'fish', 1, 1);
INSERT INTO ingredient(i_ingredientkey, i_name, i_allergenkey,i_nutritionkey) VALUES(4, 'rice', 4, 2);


INSERT INTO rein(ri_recipekey, ri_ingredientkey) VALUES(1, 3);
INSERT INTO rein(ri_recipekey, ri_ingredientkey) VALUES(1, 4);
INSERT INTO rein(ri_recipekey, ri_ingredientkey) VALUES(2, 1);


SELECT *
FROM recipe
JOIN rein ON ri_recipekey = r_recipekey
JOIN ingredient ON i_ingredientkey = ri_ingredientkey

SELECT r_name, i_name
FROM recipe
JOIN rein ON ri_recipekey = r_recipekey
JOIN ingredient ON i_ingredientkey = ri_ingredientkey
JOIN nutrition ON n_nutritionkey = i_nutritionkey
WHERE n_name = 'carbs'
INTERSECT
SELECT r_name, i_name
FROM recipe
JOIN rein ON ri_recipekey = r_recipekey
JOIN ingredient ON i_ingredientkey = ri_ingredientkey
JOIN nutrition ON n_nutritionkey = i_nutritionkey
WHERE n_name = 'fat';
