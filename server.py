from sanic import Sanic
from sanic.response import html, text
from contacts import Contacts
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

contacts = Contacts()
contacts.initialize()
cseq = contacts.add_comment(b'jade', 'darel', 'This is an additional comment added dynamically')
contacts.remove_comment(b'jade', cseq)

app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.get('/')
async def index(request):
    return html(env.get_template('index.html').render(title="Street Scum"))


@app.get('/contact/<name>')
async def contact(request, name):
    c = contacts.get_contact(bytes(name,'utf-8'))
    print(c)
    if c:
        return html(env.get_template('contact.html').render(title="Street Scum", contact=c))
    else:
        # Need a 404 here
        return html(env.get_template('index.html').render(title="Street Scum"))


app.run("0.0.0.0", port=8888)
