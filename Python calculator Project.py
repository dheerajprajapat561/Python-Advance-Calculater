from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_wtf.csrf import CSRFProtect
import os
import math
import re
from datetime import datetime
from functools import wraps
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management
csrf = CSRFProtect(app)

# Maximum number of history items to keep
MAX_HISTORY_ITEMS = 20

def handle_math_errors(f):
    """Decorator to handle math-related errors"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except ValueError as e:
            return str(e) or "Invalid input"
        except (TypeError, AttributeError):
            return "Invalid operation"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    return wrapper

@handle_math_errors
def calculate_expression(expression):
    """Safely evaluate a mathematical expression"""
    # Replace common mathematical constants and functions
    expression = expression.replace('^', '**')
    
    # Replace functions with their math module equivalents
    math_functions = {
        'sin': 'math.sin',
        'cos': 'math.cos',
        'tan': 'math.tan',
        'log': 'math.log10',
        'ln': 'math.log',
        'sqrt': 'math.sqrt',
        'π': 'math.pi',
        'e': 'math.e'
    }
    
    for func, math_func in math_functions.items():
        expression = expression.replace(func, math_func)
    
    # Validate the expression to prevent code injection
    if not re.match(r'^[0-9+\-*/.() \^a-zπe]+$', expression):
        raise ValueError("Invalid characters in expression")
    
    # Evaluate the expression
    result = eval(expression, {'__builtins__': None, 'math': math}, {})
    
    # Handle special float values
    if isinstance(result, float):
        # Remove trailing .0 for whole numbers
        if result.is_integer():
            result = int(result)
        else:
            # Round to 10 decimal places to avoid floating point precision issues
            result = round(result, 10)
    
    return result

@handle_math_errors
def calculate_simple(num1, num2, operator):
    """Perform basic calculation based on the operator"""
    num1 = float(num1)
    num2 = float(num2)
    
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
    elif operator == "%":
        result = num1 % num2
    elif operator == "^":
        result = num1 ** num2
    else:
        raise ValueError(f"Unsupported operator: {operator}")
    
    # Convert to int if it's a whole number
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result

@app.route('/')
def index():
    """Render the calculator page"""
    if 'history' not in session:
        session['history'] = []
    return render_template('calculator.html', history=session['history'])

@app.route('/calculate', methods=['POST'])
def calculate_route():
    """Handle calculation requests, both simple and scientific"""
    try:
        print("\n=== New Calculation Request ===")
        
        # Ensure session is properly initialized
        if 'history' not in session:
            print("Initializing new session history")
            session['history'] = []
        
        # Get and validate JSON data
        data = request.get_json(silent=True)
        print(f"Raw request data: {request.data}")
        
        if not data:
            error_msg = 'No JSON data provided or invalid JSON format'
            print(error_msg)
            return jsonify({
                'error': error_msg,
                'received_data': str(request.data)
            }), 400
        
        # Check if this is a scientific calculation or a simple one
        if 'expression' in data:
            # Scientific calculation with expression
            expression = str(data.get('expression', '')).strip()
            if not expression:
                return jsonify({'error': 'No expression provided'}), 400
                
            print(f"Scientific calculation requested for expression: {expression}")
            
            try:
                result = calculate_expression(expression)
                if isinstance(result, str):
                    return jsonify({'error': result}), 400
                
                # Add to history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                calculation = {
                    'expression': expression,
                    'result': result,
                    'timestamp': timestamp
                }
                
                update_history(calculation)
                
                return jsonify({
                    'result': result,
                    'history': session.get('history', [])
                })
                
            except Exception as e:
                print(f"Error in scientific calculation: {str(e)}")
                return jsonify({
                    'error': f'Calculation error: {str(e)}',
                    'expression': expression
                }), 400
                
        else:
            # Simple calculation with two operands and an operator
            num1_str = str(data.get('num1', '')).strip()
            num2_str = str(data.get('num2', '')).strip()
            operator = str(data.get('operator', '')).strip()
            
            print(f"Simple calculation: {num1_str} {operator} {num2_str}")
            
            # Validate input
            if not all([num1_str, num2_str, operator]):
                return jsonify({
                    'error': 'Missing required fields. Need num1, num2, and operator.'
                }), 400
            
            try:
                result = calculate_simple(num1_str, num2_str, operator)
                if isinstance(result, str):
                    return jsonify({'error': result}), 400
                
                # Add to history
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                calculation = {
                    'expression': f"{num1_str} {operator} {num2_str}",
                    'result': result,
                    'timestamp': timestamp
                }
                
                update_history(calculation)
                
                return jsonify({
                    'result': result,
                    'history': session.get('history', [])
                })
                
            except Exception as e:
                print(f"Error in simple calculation: {str(e)}")
                return jsonify({
                    'error': f'Calculation error: {str(e)}',
                    'expression': f"{num1_str} {operator} {num2_str}"
                }), 400
                
    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500

def update_history(calculation):
    """Update the calculation history in the session"""
    history = session.get('history', []).copy()
    history.insert(0, calculation)
    # Keep only the last MAX_HISTORY_ITEMS calculations
    session['history'] = history[:MAX_HISTORY_ITEMS]
    session.modified = True

@app.route('/favicon.ico')
def favicon():
    """Serve the favicon.ico file"""
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors by returning a JSON response"""
    if request.path.startswith('/api/'):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    return render_template('404.html'), 404

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear calculation history"""
    try:
        # Check if user is logged in (basic protection)
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
            
        # Ensure session is properly initialized
        if 'history' not in session:
            session['history'] = []
        
        # Get the current history count before clearing
        history_count = len(session['history'])
        
        # Clear the history
        session['history'] = []
        session.modified = True
        
        print(f"History cleared successfully. Removed {history_count} items.")
        
        return jsonify({
            'status': 'success',
            'message': f'Cleared {history_count} history items',
            'history': []
        })
        
    except Exception as e:
        error_msg = f"Error clearing history: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Failed to clear history',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
