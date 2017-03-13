from sanic import Sanic
from sanic.response import html, json, text
from contacts import Contacts
import authorization
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

contacts = Contacts()
contacts.initialize()

app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.get('/')
async def index(request):
    return html(env.get_template('index.html').render(title="Street Scum"))


@app.post('/verify')
async def verify(request):
    t = request.cookies.get('streetnode')
    if isinstance(t, str): t = bytes(t, encoding='utf-8')
    v = authorization.validate(t)
    if v:
        return json(v)
    else:
        return json({'result': 'failure'})


@app.post('/login')
async def login(request):
    username = request.json['username']
    pword = request.json['password']
    token = authorization.authorize(username, pword)
    if token:
        response = json({'result': 'success'})
        response.cookies['streetnode'] = token.decode('utf-8')
        return response
    else:
        return json({'result': 'failure'})


@app.post('/comment')
async def comment(request):
    t = request.cookies.get('streetnode')
    if isinstance(t, str): t = bytes(t, encoding='utf-8')
    v = authorization.validate(t)
    if not v: return json({'result': 'failure'})
    data = request.json
    name = bytes(data['name'], 'utf-8')
    cseq = 0
    if 'msg' not in data:
        if 'sequence' in data: cseq = contacts.remove_comment(name, data['sequence'])
    else:
        cseq = contacts.add_comment(name, v['username'], data['msg'])

    if cseq > 0:
        return json({'result': 'success'})
    else:
        return json({'result': 'failure'})


@app.get('/contact/<name>')
async def contact(request, name):
    c = contacts.get_contact(bytes(name,'utf-8'))
    if c:
        return html(env.get_template('contact.html').render(title="Street Scum", contact=c, key=name))
    else:
        # Need a 404 here
        return html(env.get_template('index.html').render(title="Street Scum"))


@app.post('/addcontact/<key>')
async def addcontact(request, key):
    v = request.json
    k = key
    if isinstance(k, str): k = bytes(k, encoding='utf-8')
    contacts.add_contact(k, v)
    return json({'result': 'success'})


def run():
    app.run("0.0.0.0", port=8888)

if __name__ == '__main__':
    run()
