import traceback

class JSONValidator:
    def __init__(self, schema, object):
        '''
        JSON validator
        :param: schema: The schema that will be used
        :param: object: The JSON to validate
        '''
        self.schema = schema
        self.object = object
        self.messages = []
    
    def _add_msg(self, msg):
        msg = ' '.join(msg)
        print(msg)
        self.messages.append(msg)

    def _verify(self, object, schema):
        if not isinstance(object[schema['key']], schema['type']):
            self._add_msg(['Invalid type for key:', schema['key']])
            self._add_msg(['Excepted:', schema['type']])
            self._add_msg(['Got:', type(object[schema['key']]), '\n'])

            object[schema['key']] = schema['default'] if 'default' in schema else schema['type']()

            self.valid = False
        if 'items' in schema:
            self._validate(schema['items'], object[schema['key']])

    def _validate(self, schema, object):
        for s in schema:
            try:
                if isinstance(object, list):
                    for o in object:
                        self._verify(o, s)
                elif s['key'] in object:
                    self._verify(object, s)
                elif s['required'] or self.require_all or s['key'] in self.required_keys:
                    self._add_msg(['Missing Key:', s['key']])
                    self.valid = False

                    object[s['key']] = s['default'] if 'default' in s else s['type']()

                    self._verify(object, s)
            except:
                self.valid = False
                self._add_msg(['============================================'])
                self._add_msg(['Invalid structure, please check again:'])
                self._add_msg(['***** Schema:', str(s)])
                self._add_msg(['***** Key:', s['key']])
                self._add_msg(['*****', traceback.format_exc()])

    def validate(self, require_all=False, required_keys=[]):
        self.valid = True
        self.require_all = require_all
        self.required_keys = required_keys
        self._validate(self.schema, self.object)
        return self.valid, self.messages

