import os
from dotenv import load_dotenv
from app import create_app

env = os.getenv('FLASK_ENV', 'development')

app = create_app()

if __name__ == '__main__':
    app.run(debug=(env == 'development'),host='0.0.0.0', port=5000)
