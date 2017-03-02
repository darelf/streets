from sanic import Sanic
from sanic.response import html, text
from oauth2client import client, crypt
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

CLIENT_ID = ""

app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.route("/")
async def index(request):
    return html(env.get_template('index.html').render(title="Street Scum"))


@app.post("/signin")
async def signin(request):
    token = request.form.get('token')
    idinfo = client.verify_id_token(token, CLIENT_ID)
    print("received info")

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        return text("invalid_issuer")

    userid = idinfo['sub']
    response = text("success")
    response.cookies['usertoken'] = token
    response.cookies['userid'] = userid

    return response

app.run("localhost", port=8080)
