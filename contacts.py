import plyvel
import time
import json


class Contacts:
    def __init__(self):
        self.db = None

    def get_contact(self, name):
        item = self.db.get(name)
        if item: return json.loads(item)
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
                          'msg': 'Curabitur varius pharetra neque id porta. Duis hendrerit et massa eget consequat. In mollis diam quis lectus tempus porttitor'
                          }]
        }

        self.db = plyvel.DB('contacts', create_if_missing=True)
        item = self.db.get(b'jade')
        if not item:
            self.db.put(b'jade', bytes(json.dumps(jade), 'utf-8'))
