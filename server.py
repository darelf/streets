from sanic import Sanic
from sanic.response import html, json, redirect
from archive import Archive
import authorization
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html'])
)

archive = Archive()
archive.initialize()

#contacts = Contacts()
#contacts.initialize()

#missions = Missions()
#missions.initialize()

app = Sanic()

app.static('/static/', './static/')
app.static('/favicon.ico', './static/favicon.ico')


@app.get('/')
async def index(request):
    contact_list = archive.get_item_list('contact')
    return html(env.get_template('index.html').render(title="Street Scum", contacts=contact_list))


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
    type = data.get('type', 'contact')
    if 'msg' not in data:
        if 'sequence' in data: cseq = archive.remove_comment(type, name, data['sequence'])
    else:
        cseq = archive.add_comment(type, name, v['username'], data['msg'])

    if cseq > 0:
        return json({'result': 'success'})
    else:
        return json({'result': 'failure'})


@app.get('/contact/<name>')
async def contact(request, name):
    c = archive.get_item('contact', bytes(name, 'utf-8'))
    if c:
        return html(env.get_template('contact.html').render(title="Street Scum", contact=c, key=name, key_type='contact'))
    else:
        # Need a 404 here
        return redirect('/')


@app.get('/team/<name>')
async def team(request, name):
    c = archive.get_item('team', bytes(name, 'utf-8'))
    if c:
        return html(env.get_template('contact.html').render(title="Street Scum", contact=c, key=name, key_type='contact'))
    else:
        # Need a 404 here
        return redirect('/')


@app.get('/mission/<name>')
async def mission(request, name):
    c = archive.get_item('mission', bytes(name, 'utf-8'))
    if c:
        return html(env.get_template('mission.html').render(title="Street Scum", mission=c, key=name, key_type='mission'))
    else:
        # Need a 404 here
        return redirect('/')


@app.get('/list/<txt>')
async def list_contacts(request, txt):
    c = archive.get_item_list('contact', txt)
    if c:
        return json(c)
    else:
        return ({'result': 'failure'})


def run(p=8888):
    app.run("0.0.0.0", port=p)

if __name__ == '__main__':
    run()
