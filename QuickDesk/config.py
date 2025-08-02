class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quickdesk.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'your_email@gmail.com'
    MAIL_PASSWORD = 'your_app_password'
    MAIL_DEFAULT_SENDER = 'your_email@gmail.com'
