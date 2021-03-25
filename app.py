from flask import Flask

app = Flask(__name__)


def home():
    return 'Hello World!'


app.add_url_rule('/', '', home)
app.add_url_rule('/home', 'home', home)

if __name__ == '__main__':
    app.run()
