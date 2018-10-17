'''Run the app.'''
import os

from instance import create_app

configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)
port=os.getenv("PORT",5000)
app.run(host='0.0.0.0', port=port)



