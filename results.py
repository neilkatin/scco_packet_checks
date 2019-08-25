
import logging
import re

log = None

class Results(object):

    def __init__(self, mailbox):
        global log
        if log == None:
            log = logging.getLogger(__name__)
        self.mailbox = mailbox
        log.debug(f"initialzing Results")
        
        # hold all errors indexed by message key; each entry is an array
        self._msg_errors = {}
        self._valid_msg_keys = []

    @property
    def down_bbs(self):
        return self._down_bbs
    @down_bbs.setter
    def down_bbs(self, val):
        self._down_bbs = val

    @property
    def from_header(self):
        return self._from_header
    @from_header.setter
    def from_header(self, val):
        self._from_header = val


    def add_from_to(self, key, msg, from_header, to):
        log.debug(f"from <{ from_header }> to <{ to }>")

    def add_msg_error(self, error):
        key = error.key
        if key not in self._msg_errors:
            self._msg_errors[key] = []

        self._msg_errors[key].append(error)
        log.debug(f"adding message error { error }")

    def add_valid_msg_key(self, key):
        self._valid_msg_keys.append(key)

    def get_valid_msg_keys(self):
        return self._valid_msg_keys.copy()


class Address(object):
    """ parse an email address into user@domain; domain to localhost.resthost.  missing components will be None """

    _domainparse = re.compile(r'@', flags=re.IGNORECASE)
    _hostparse = re.compile(r'\.', flags=re.IGNORECASE)
    
    def __init__(self, address):
        self._address = address
        self._parse(address)

    def _parse(self, address):

        # split into host@domain
        result = self._domainparse.split(address, maxsplit=1)
        self._user = result[0]
        if len(result) < 2:
            self._domain = None
        else:
            self._domain = result[1]

            # split into _localhost._resthost
            result = self._hostparse.split(self._domain, maxsplit=1)
            self._localhost = result[0]
            if len(result) < 2:
                self._resthost = None
            else:
                self._resthost = result[1]

    @property
    def user(self):
        return self._user

    @property
    def domain(self):
        return self._domain

    @property
    def localhost(self):
        return self._localhost

    @property
    def resthost(self):
        return self._resthost


    def __str__(self):
        return f"Address({ self._address }) -> {self._user}@{self._localhost}.{self._resthost}"


class MsgError(object):

    def __init__(self, key, msg, error_string):
        self._key = key
        self._msg = msg
        self._error_string = error_string

    @property
    def key(self):
        return self._key

    @property
    def msg(self):
        return self._msg

    @property
    def error_string(self):
        return self._error_string

    def __str__(self):
        return f"{ self._error_string } on msg { self._key }"





