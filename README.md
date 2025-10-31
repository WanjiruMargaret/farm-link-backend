# farm-link-backend
A farm-link backend is a flask powered rest API. it acts as a server for the farmlink application-connectinf farmers, buyuers, giving them update on the lates weather and the harvesting days , all this is now applied in a simple efficient digital platform that could be accesses any where by any one .

# features 
user authentication with JWT.
secure password hashing using flask-bcyrpt
image uploads using cloudinary.
Database migrations 
Organised blueprint routes for clearner structure 
environment variable protection with dotenv

# Technologies Used 

Flask 
Flask-SQLAlchemy
Flask-migrate 
Flask-Bcrypt
Flask-JWT
FLASK CLOUDINARY


## Project structure 

farmlink-backend/
│
├── app.py
├── extensions.py
├── models/
│   └── user.py
├── routes/
│   ├── auth_routes.py
│   └── upload_routes.py
├── migrations/
├── .env
├── .gitignore
├── requirements.txt
└── README.md

