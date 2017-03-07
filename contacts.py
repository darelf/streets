import plyvel, time, json, markdown, os

class Contacts:
    def __init__(self):
        self.db = None

    def get_contact(self, name):
        item = self.db.get(name)
        if item:
            c = json.loads(item)
            path = 'assets/' + name.decode() + '.md'
            if os.path.isfile(path):
                with open(path, 'r') as myfile:
                    text = myfile.read()
                    c['background'] = markdown.markdown(text, output_format='html5')
            return c
        else:
            return None

    def add_comment(self, name, commenter, msg):
        item = self.db.get(name)
        if item:
            c = json.loads(item)
            s = time.time()
            comment = {
                'commenter': commenter,
                'msg': msg,
                'sequence': s
            }
            c['comments'].append(comment)
            self.db.put(name, bytes(json.dumps(c), 'utf-8'))
            return s
        return 0

    def remove_comment(self, name, sequence):
        item = self.db.get(name)
        if item:
            c = json.loads(item)
            comments = c['comments']
            for x in comments:
                if x['sequence'] == sequence:
                    comments.remove(x)
                    break
            self.db.put(name, bytes(json.dumps(c), 'utf-8'))

    def initialize(self):
        jade = {
            'title_name': 'Jade',
            'name': 'Jane Worth',
            'species': 'Human',
            'alterations': 'Skilljack',
            'comments': [{'commenter':'club0',
                          'sequence': time.time(),
                          'msg': 'Jade is a real party girl. Best source for Jazz in south Redmond. Never overcharges, and always has quality goods.'
                          }]
        }

        self.db = plyvel.DB('contactDB', create_if_missing=True)
        item = self.db.get(b'jade')
        if not item:
            self.db.put(b'jade', bytes(json.dumps(jade), 'utf-8'))
