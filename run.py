'''Run the application.'''
import os

from app import create_app
from app.v2.connect_db import connect_to_db 
from app.v2.models.user_models import User as User2


# create super user with db
user2 = User2(username='Administrator',
              password='pass400&', email='admin@admin.com')
if not User2.get(username='Administrator'):
    user2.add_user()
    super_id = User2.get(username='Administrator')[0]
    user2.assign_user_a_role('superuser', super_id)
else:
    pass

# run application
configuration = os.getenv('APP_SETTINGS')
app = create_app(configuration)

 
if __name__ == '__main__':
	app.run()
