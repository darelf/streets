import plyvel, time, json, markdown, os
from glob import glob


class Contacts:
    def __init__(self):
        self.db = None

    def get_contact(self, name):
        item = self.db.get(name)
        if item:
            c = json.loads(item)
            path = 'assets/contacts/' + name.decode() + '.md'
            if os.path.isfile(path):
                with open(path, 'r') as myfile:
                    text = myfile.read()
                    c['background'] = markdown.markdown(text, output_format='html5', extensions=['markdown.extensions.meta'])
            return c
        else:
            return None

    def get_contact_list(self, k=None):
        contact_list = []
        for key, value in self.db:
            if (k and key.startswith(k)) or not k:
                c = json.loads(value)
                contact_list.append(c)
        return contact_list

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
            if 'comments' in c:
                c['comments'].append(comment)
            else:
                c['comments'] = [comment]
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
            return sequence
        return 0

    def add_contact(self, key, c):
        self.db.put(key, bytes(json.dumps(c), 'utf-8'))

    def parse_contact(self, fname):
        md = markdown.Markdown(output_format='html5', extensions=['markdown.extensions.meta'])
        with open(fname, 'r') as myfile:
            text = myfile.read()
            md.convert(text)

        meta = md.Meta
        c = {
            'link': ''.join(meta['link']),
            'title_name': ''.join(meta['title_name']),
            'name': ''.join(meta['name']),
            'species': ''.join(meta['species']),
            'alterations': ''.join(meta['alterations'])
        }
        return c

    def initialize(self):
        self.db = plyvel.DB('contactDB', create_if_missing=True)
        print("calling initialize")
        for x in glob('assets/contacts/*.md'):
            print("looking for", x)
            key = os.path.basename(x).split('.')[0]
            if isinstance(key, str): key = bytes(key, encoding='utf8')
            item = self.db.get(key)
            if not item:
                print("adding", x)
                c = self.parse_contact(x)
                self.db.put(key, bytes(json.dumps(c), 'utf-8'))
            else:
                print("already have", x)

