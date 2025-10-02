import pandas as pd
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Read the CSV file
df = pd.read_csv('flavor_bible_full.csv')


def clean_df(df):
    filter_keywords = ['techniques', 'cuisine', 'taste', '\+', 'flavor affinities', 'weight:',
                       'warming', 'tips']

    # Create a boolean mask to keep rows that do NOT contain the keywords
    mask = ~(
            df['main'].str.contains('|'.join(filter_keywords), case=False, na=False) |
            df['pairing'].str.contains('|'.join(filter_keywords), case=False, na=False)
    )

    # Apply the mask to filter the DataFrame
    filtered_df = df[mask]

    return filtered_df


df = clean_df(df)


def create_flavor_dictionary():
    """
    Convert the DataFrame to a dictionary of ingredients and their pairings.

    Returns:
    dict: A dictionary where keys are ingredients and values are lists of pairings
    """
    # Group by main ingredient and collect unique pairings
    flavor_dict = {}
    for _, row in df.iterrows():
        main = str(row['main']).lower().strip()
        pairing = str(row['pairing']).lower().strip()

        # Skip if main or pairing is NaN
        if pd.isna(main) or pd.isna(pairing):
            continue

        # Add to dictionary, ensuring unique pairings
        if main not in flavor_dict:
            flavor_dict[main] = []

        # Only add if not already in the list
        if pairing not in flavor_dict[main]:
            flavor_dict[main].append(pairing)

    return flavor_dict


def get_unique_flavor_combination(flavor_dict, num_ingredients, initial_ingredient=None):
    """
    Generate unique ingredient combinations that pair well together.

    Args:
    flavor_dict (dict): Dictionary of ingredients and their pairings
    num_ingredients (int): Number of ingredients to generate
    initial_ingredient (str, optional): Starting ingredient specified by user

    Returns:
    list: A list containing unique ingredients that pair well
    str or None: Error message if any
    """
    # Check if initial ingredient exists in our dictionary
    if initial_ingredient:
        initial_ingredient = initial_ingredient.lower().strip()
        if initial_ingredient not in flavor_dict:
            return [], f"'{initial_ingredient}' not found in our ingredient database. Please try another ingredient."

        # Start with the specified ingredient
        current_combination = [initial_ingredient]
    else:
        # Start with a random ingredient
        current_combination = [random.choice(list(flavor_dict.keys()))]

    attempts = 0
    max_attempts = 200

    while len(current_combination) < num_ingredients and attempts < max_attempts:
        # Find potential next ingredients based on existing combination
        potential_next_ingredients = []

        # Look at pairings of all current ingredients
        for current_ing in current_combination:
            potential_next_ingredients.extend(flavor_dict.get(current_ing, []))

        # Remove duplicates and ingredients already in the combination
        potential_next_ingredients = list(set(potential_next_ingredients) - set(current_combination))

        # If no potential ingredients, try again with a different approach
        if not potential_next_ingredients:
            attempts += 1
            continue

        # Choose a random next ingredient
        next_ingredient = random.choice(potential_next_ingredients)
        current_combination.append(next_ingredient)

    # If we couldn't find enough ingredients
    if len(current_combination) < num_ingredients:
        if initial_ingredient:
            return [], f"Couldn't find enough complementary ingredients for '{initial_ingredient}'. Please try another ingredient."
        else:
            return ["Could not find a suitable combination"], None

    return current_combination, None


# Create flavor dictionary when the app starts
flavor_dictionary = create_flavor_dictionary()


@app.route('/')
def index():
    """
    Render the main page with a default 3-ingredient flavor combination.
    """
    num_ingredients = 3
    ingredients, error = get_unique_flavor_combination(flavor_dictionary, num_ingredients)
    return render_template('index.html',
                           ingredients=ingredients,
                           current_num=num_ingredients,
                           initial_ingredient="",
                           error=error)


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate new flavor combinations based on user selection.
    """
    num_ingredients = int(request.form.get('num_ingredients', 3))
    initial_ingredient = request.form.get('initial_ingredient', '').strip()

    ingredients, error = get_unique_flavor_combination(
        flavor_dictionary,
        num_ingredients,
        initial_ingredient if initial_ingredient else None
    )

    return render_template('index.html',
                           ingredients=ingredients,
                           current_num=num_ingredients,
                           initial_ingredient=initial_ingredient,
                           error=error)


@app.route('/ingredients/autocomplete')
def autocomplete():
    """
    Return a list of ingredients that match the search term.
    """
    search_term = request.args.get('term', '').lower().strip()
    if not search_term:
        return jsonify([])

    # Get all ingredients from our flavor dictionary that contain the search term
    matching_ingredients = [
        ingredient for ingredient in flavor_dictionary.keys()
        if search_term in ingredient
    ]

    # Sort alphabetically and limit to 10 results for better performance
    matching_ingredients = sorted(matching_ingredients)[:10]

    return jsonify(matching_ingredients)


if __name__ == '__main__':
    app.run(debug=True)
