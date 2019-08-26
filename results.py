
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
        self._msg_keys = []
        self._sent_from_error_count = 0
        self._source_xsc = [ 0, 0, 0, 0, 0 ]
        self._source_other = 0
        self._body_type_counts = { }
        self._unique_froms = { }
        self._unique_users = { }

    @property
    def down_bbs(self):
        return self._down_bbs
    @down_bbs.setter
    def down_bbs(self, val):
        self._down_bbs = val


    def add_msg_error(self, error):
        key = error.key
        if key not in self._msg_errors:
            self._msg_errors[key] = []

        self._msg_errors[key].append(error)
        log.debug(f"adding message error { error }")

    def add_msg_key(self, key):
        self._msg_keys.append(key)

    def get_msg_keys(self):
        return self._msg_keys.copy()

    def get_msg_errors(self, key):
        """ retrieve all errors associated with this key """
        return self._msg_errors.get(key)

    def note_sent_from_error(self):
        """ increment the count of messages sent from the down bbs """
        self._sent_from_error_count += 1

    @property
    def total_msg_keys(self):
        """ total number of messages, after filtering out delivery msgs """
        return len(self._msg_keys)
    @property
    def total_msg_keys_correct(self):
        """ total number of messages that didn't have errors """
        total = 0
        for k in self._msg_keys:
            if k not in self._msg_errors:
                total += 1
        return total

    @property
    def down_msg_keys(self):
        """ the number of mesages sent from the down bbs """
        return self._sent_from_error_count

    # total message source counts
    def note_source_xsc(self, index):
        assert index >= 1
        assert index < len(self._source_xsc)
        self._source_xsc[index] += 1
    def note_source_other(self):
        self._source_other += 1

    # output message source counts
    def get_source_xsc(self, index):
        assert index >= 1
        assert index < len(self._source_xsc)
        return self._source_xsc[index]
    def get_source_other(self):
        return self._source_other
    def get_source_xsc_total(self):
        return sum(self._source_xsc)

    # total up body count types
    def note_body_type(self, body_type):
        if body_type not in self._body_type_counts:
            self._body_type_counts[body_type] = 0

        self._body_type_counts[body_type] += 1

    # output body type counts
    def get_body_types(self):
        return self._body_type_counts.keys()
    def get_body_type_count(self, body_type):
        return self._body_type_counts[body_type]

    # track unique froms and users
    def note_from_address(self, addr):
        self._unique_froms[addr] = 1
    def note_user_address(self, addr):
        self._unique_users[addr] = 1
    def get_unique_from_count(self):
        return len(self._unique_froms)
    def get_unique_user_count(self):
        return len(self._unique_users)



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





