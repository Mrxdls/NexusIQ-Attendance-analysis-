from APP import create_app
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'APP'))
# Create the Flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)