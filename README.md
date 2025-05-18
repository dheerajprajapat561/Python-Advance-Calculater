# Advanced Scientific Calculator

A feature-rich scientific calculator with a modern web interface, supporting both basic and advanced mathematical operations.

## Features

- **Basic Operations**: Addition (+), Subtraction (-), Multiplication (*), Division (/), Modulus (%)
- **Scientific Functions**:
  - Trigonometric: sin, cos, tan (in radians)
  - Logarithmic: log (base 10), ln (natural log)
  - Square root (√), Power (x^y)
  - Constants: π (pi), e (Euler's number)
- **Memory Functions**: M+, M-, MR, MC
- **History**: View and reuse previous calculations
- **Themes**: Toggle between light and dark mode
- **Responsive Design**: Works on desktop and mobile devices
- **Keyboard Support**: Use your keyboard for faster calculations
- Keyboard support for faster input
- Session-based history storage
- Error handling for invalid operations

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

1. Run the Flask development server:

```bash
python "Python calculator Project.py"
```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`

## Usage

- Click the number buttons or use your keyboard to input numbers
- Use the operator buttons (+, -, *, /, %) to perform calculations
- Press `=` or hit Enter to calculate the result
- Press `C` or Escape to clear the current input
- Press the backspace button or Backspace key to delete the last digit
- View your calculation history below the calculator
- Click the trash icon to clear the history

## Project Structure

```
Python Calculator/
├── templates/
│   ├── base.html         # Base template with common HTML structure
│   └── calculator.html   # Calculator interface template
├── Python calculator Project.py  # Main Flask application
└── requirements.txt      # Python dependencies
```

## Dependencies

- Flask - Web framework
- Flask-WTF - Form handling and CSRF protection
- Bootstrap 5 - CSS framework for styling
- jQuery - JavaScript library for DOM manipulation

## Future Enhancements

- Add more advanced mathematical functions (sin, cos, tan, etc.)
- Support for complex expressions with multiple operations
- User authentication to save calculation history
- Export/import history
- Dark mode support
- Unit tests

## License

This project is open source and available under the MIT License.
