from flask import Flask, request, render_template
import random

app = Flask(__name__)

def sort_letters(message):
    """Sort the characters of a string in alphabetical order."""
    return ''.join(sorted(list(message or "")))

@app.route('/')
def homepage():
    
    return render_template('home.html')

@app.route('/froyo')
def choose_froyo():
    return """
    <form action="/froyo_results" method="GET">
        What is your favorite Fro-Yo flavor? <br/>
        <input type="text" name="flavor"><br/><br/>
        Choose up to 3 toppings:<br/>
        <input type="checkbox" name="toppings" value="Sprinkles" onclick="limitToppings(this)"> Sprinkles<br/>
        <input type="checkbox" name="toppings" value="Chocolate Chips" onclick="limitToppings(this)"> Chocolate Chips<br/>
        <input type="checkbox" name="toppings" value="Fruit" onclick="limitToppings(this)"> Fruit<br/>
        <input type="checkbox" name="toppings" value="Nuts" onclick="limitToppings(this)"> Nuts<br/>
        <input type="checkbox" name="toppings" value="Whipped Cream" onclick="limitToppings(this)"> Whipped Cream<br/><br/>
        <input type="submit" value="Submit!">
    </form>
    <script>
    function limitToppings(checkbox) {
        var checked = document.querySelectorAll('input[name="toppings"]:checked');
        if (checked.length > 3) {
            checkbox.checked = false;
            alert("You can only select up to 3 toppings.");
        }
    }
    </script>
    """

@app.route('/froyo_results')
def show_froyo_results():
    """Shows the user what they ordered from the previous page."""
    users_froyo_flavor = request.args.get('flavor', 'no flavor')
    toppings = request.args.getlist('toppings')
    toppings_display = ', '.join(toppings) if toppings else 'no toppings'
    return f'You ordered {users_froyo_flavor} flavored Fro-Yo with {toppings_display}!'

@app.route('/favorites')
def favorites():
    """Shows the user a form to choose their favorite color, animal, and city."""
    return """
    <form action="/favorites_results" method="GET">
        Favorite color: <input type="text" name="color"><br/>
        Favorite animal: <input type="text" name="animal"><br/>
        Favorite city: <input type="text" name="city"><br/>
        <input type="submit" value="Submit!">
    </form>
    """

@app.route('/favorites_results')
def favorites_results():
    """Shows the user a nice message using their form results."""
    color = request.args.get('color')
    animal = request.args.get('animal')
    city = request.args.get('city')
    return f'Wow, I didn\'t know {color} {animal}s lived in {city}!'

@app.route('/secret_message')
def secret_message():
    """Shows the user a form to collect a secret message. Sends the result via
    the POST method to keep it a secret!"""
    return """
    <form action="/message_results" method="POST">
        Enter your secret message: <input type="text" name="message"><br/>
        <input type="submit" value="Submit!">
    </form>
    """

@app.route('/message_results', methods=['POST'])
def message_results():
    """Shows the user their message, with the letters in sorted order."""
    message = request.form.get('message')
    sorted_message = sort_letters(message)
    return f'Here is your secret message, sorted: {sorted_message}'

@app.route('/calculator')
def calculator():
    """Shows the user a form to enter 2 numbers and an operation."""
    return """
    <form action="/calculator_results" method="GET">
        Please enter 2 numbers and select an operator.<br/><br/>
        <input type="number" name="operand1">
        <select name="operation">
            <option value="add">+</option>
            <option value="subtract">-</option>
            <option value="multiply">*</option>
            <option value="divide">/</option>
        </select>
        <input type="number" name="operand2">
        <input type="submit" value="Submit!">
    </form>
    """

@app.route('/calculator_results')
def calculator_results():
    """Shows the user the result of their calculation."""
    operand1 = request.args.get('operand1', type=float)
    operand2 = request.args.get('operand2', type=float)
    operation = request.args.get('operation')
    result = None

    if operation == 'add':
        result = operand1 + operand2
    elif operation == 'subtract':
        result = operand1 - operand2
    elif operation == 'multiply':
        result = operand1 * operand2
    elif operation == 'divide':
        if operand2 != 0:
            result = operand1 / operand2
        else:
            return "Error: Cannot divide by zero."
    else:
        return "Invalid operation."

    # Remove decimal if result is whole number
    if result == int(result):
        result = int(result)
    return f'result is: {result}'

HOROSCOPE_PERSONALITIES = {
    'aries': 'Adventurous and energetic',
    'taurus': 'Patient and reliable',
    'gemini': 'Adaptable and versatile',
    'cancer': 'Emotional and loving',
    'leo': 'Generous and warmhearted',
    'virgo': 'Modest and shy',
    'libra': 'Easygoing and sociable',
    'scorpio': 'Determined and forceful',
    'sagittarius': 'Intellectual and philosophical',
    'capricorn': 'Practical and prudent',
    'aquarius': 'Friendly and humanitarian',
    'pisces': 'Imaginative and sensitive'
}

@app.route('/horoscope')
def horoscope_form():
    """Shows the user a form to fill out to select their horoscope."""
    return render_template('horoscope_form.html')

@app.route('/horoscope_results')
def horoscope_results():
    """Shows the user the result for their chosen horoscope, greets by name, and shows lucky number."""
    user_name = request.args.get('user_name', '')
    horoscope_sign = request.args.get('horoscope_sign', '').lower()
    users_personality = HOROSCOPE_PERSONALITIES.get(horoscope_sign, 'Unknown sign')
    lucky_number = random.randint(1, 99)

    context = {
        'user_name': user_name,
        'horoscope_sign': horoscope_sign,
        'personality': users_personality, 
        'lucky_number': lucky_number
    }

    return render_template('horoscope_results.html', **context)

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
