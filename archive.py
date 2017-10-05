import plyvel, time, json, markdown, os
from glob import glob

class Archive:
    def __init__(self):
        self.db = plyvel.DB('archiveDB', create_if_missing=True)
        self.contacts_db = self.db.prefixed_db(b'contacts:')
        self.team_db = self.db.prefixed_db(b'team:')
        self.missions_db = self.db.prefixed_db(b'missions:')
        self.archive_db = self.db.prefixed_db(b'archive:')
        self.db_names = {
            'contact': self.contacts_db,
            'team': self.team_db,
            'mission': self.missions_db,
            'archive': self.archive_db
        }

    def parse_file(self, c, path):
        with open(path, 'r') as myfile:
            text = myfile.read()
            c['background'] = markdown.markdown(text, output_format='html5',
                                                extensions=['markdown.extensions.meta'])
        return c

    def add_comment(self, db, name, commenter, msg):
        item = self.db_names[db].get(name)
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
                self.db_names[db].put(name, bytes(json.dumps(c), 'utf-8'))
            return s
        return 0

    def remove_comment(self, db, name, sequence):
        item = self.db_names[db].get(name)
        if item:
            c = json.loads(item)
            comments = c['comments']
            for x in comments:
                if x['sequence'] == sequence:
                    comments.remove(x)
                    break
            self.db_names[db].put(name, bytes(json.dumps(c), 'utf-8'))
            return sequence
        return 0

    def get_item(self, db, name):
        item = self.db_names[db].get(name)
        if item:
            c = json.loads(item)
            path = 'assets/' + db + '/' + name.decode() + '.md'
            if os.path.isfile(path):
                return self.parse_file(c, path)
            return c
        else:
            return None

    def get_item_list(self, db, k=None):
        contact_list = []
        for key, value in self.db_names[db]:
            if (k and key.startswith(bytes(k, 'utf-8'))) or not k:
                c = json.loads(value)
                contact_list.append(c)
        return contact_list

    def parse_item(self, fname, base_dir):
        md = markdown.Markdown(output_format='html5', extensions=['markdown.extensions.meta'])
        with open(fname, 'r') as myfile:
            text = myfile.read()
            md.convert(text)

        meta = md.Meta
        c = {}
        for m in meta:
            c[m] = ''.join(meta[m])
        c['base_dir'] = base_dir

        return c

    def load_item(self, db, fname, base_dir):
        print("looking for", fname)
        key = os.path.basename(fname).split('.')[0]
        if isinstance(key, str): key = bytes(key, encoding='utf8')
        item = self.db_names[db].get(key)
        if not item:
            print("adding", fname)
            c = self.parse_item(fname, base_dir)
            self.db_names[db].put(key, bytes(json.dumps(c), 'utf-8'))
        else:
            print("already have", fname)

    def initialize(self):
        print("calling initialize")
        for x in glob('assets/contact/*.md'):
            self.load_item('contact', x, 'contact')

        for x in glob('assets/team/*.md'):
            self.load_item('team', x, 'team')

        for x in glob('assets/mission/*.md'):
            self.load_item('mission', x, 'mission')

        for x in glob('assets/archive/*.md'):
            self.load_item('archive', x, 'archive')
