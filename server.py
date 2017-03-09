from sanic import Sanic
from sanic.response import html, json, text
from contacts import Contacts
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


@app.post('/comment')
async def comment(request):
    data = request.json
    name = bytes(data['name'], 'utf-8')
    cseq = 0
    if 'msg' not in data:
        if 'sequence' in data: cseq = contacts.remove_comment(name, data['sequence'])
    elif 'commenter' in data and 'msg' in data:
        cseq = contacts.add_comment(bytes(data['name'], 'utf-8'), data['commenter'], data['msg'])

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


def run():
    app.run("0.0.0.0", port=8888)

if __name__ == '__main__':
    run()
