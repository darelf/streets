import plyvel, time, json, markdown, os
from glob import glob


class Contacts:
    def __init__(self):
        self.db = None

    def parse_file(self, c, path):
        with open(path, 'r') as myfile:
            text = myfile.read()
            c['background'] = markdown.markdown(text, output_format='html5', extensions=['markdown.extensions.meta'])
        return c

    def get_contact(self, name):
        item = self.db.get(name)
        if item:
            c = json.loads(item)
            path1 = 'assets/contacts/' + name.decode() + '.md'
            path2 = 'assets/team/' + name.decode() + '.md'
            if os.path.isfile(path1):
                return self.parse_file(c, path1)
            elif os.path.isfile(path2):
                return self.parse_file(c, path2)
            return c
        else:
            return None

    def get_contact_list(self, k=None):
        contact_list = []
        for key, value in self.db:
            if (k and key.startswith(bytes(k, 'utf-8'))) or not k:
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

    def load_contact(self, fname):
        print("looking for", fname)
        key = os.path.basename(fname).split('.')[0]
        if isinstance(key, str): key = bytes(key, encoding='utf8')
        item = self.db.get(key)
        if not item:
            print("adding", fname)
            c = self.parse_contact(fname)
            self.db.put(key, bytes(json.dumps(c), 'utf-8'))
        else:
            print("already have", fname)

    def initialize(self):
        self.db = plyvel.DB('contactDB', create_if_missing=True)
        print("calling initialize")
        for x in glob('assets/contacts/*.md'):
            self.load_contact(x)

        for x in glob('assets/team/*.md'):
            self.load_contact(x)

