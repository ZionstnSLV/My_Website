import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'my_flask_website_app')))

from my_flask_website_app.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
