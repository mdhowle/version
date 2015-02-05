import string
from itertools import zip_longest


class Version:
    _version = None
    _parsed_version = None
    _tags = []
    delimiters = {'.'}
    case_sensitive = True

    def __init__(self, version=None, delimiters=None, guess_delimiters=True, case_sensitive=True):
        if delimiters is not None:
            self.delimiters.update(*delimiters)

        self.case_sensitive = case_sensitive

        if version is not None:
            if delimiters is None or guess_delimiters:
                self.delimiters.update(self.guess_delimiters(str(version)))
            self.version = version

    def __repr__(self):
        return "<Version %s>" % self.version

    def __str__(self):
        return self.version

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value
        value = str(value)

        version_digits = self.split(value, *list(self.delimiters))
        version_digits = self.normalize(version_digits)
        result = []

        w = ""
        vtype = None

        for val in version_digits:
            last_vtype = vtype
            vtype = type(val)

            if val in self.delimiters:
                vtype = None

            if vtype == str:
                w += val
                continue

            if vtype != str and last_vtype == str:
                result.append(w)
                w = ""

            if vtype is not None:
                result.append(val)

        if w and vtype is str:
            result.append(w)

        self._parsed_version = tuple(result)

    @property
    def parsed_version(self):
        if self._parsed_version is not None:
            return self._parsed_version
        return None

    def __eq__(self, other):
        if not isinstance(other, Version):
            other = Version(other, guess_delimiters=True)

        if self.parsed_version == other.parsed_version:
            return True

        if self.parsed_version is None or other.parsed_version is None:
            return False

        for v1, v2 in zip_longest(self.parsed_version, other.parsed_version):
            if not self.case_sensitive:
                if isinstance(v1, str):
                    v1 = v1.lower()
                if isinstance(v2, str):
                    v2 = v2.lower()

            if v1 is None:
                if v2 == 0:
                    continue
                else:
                    return False
            elif v2 is None:
                if v1 == 0:
                    continue
                else:
                    return False
            elif v1 != v2:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if not isinstance(other, Version):
            other = Version(other, guess_delimiters=True)

        if self.parsed_version is None or other.parsed_version is None:
            return False

        for v1, v2 in zip_longest(self.parsed_version, other.parsed_version):

            if not self.case_sensitive:
                if isinstance(v1, str):
                    v1 = v1.lower()
                if isinstance(v2, str):
                    v2 = v2.lower()

            if v1 is None:
                v1 = 0
            elif v2 is None:
                v2 = 0
            try:
                if v1 > v2:
                    return True
                elif v1 < v2:
                    return False
                elif v1 == v2:
                    continue
            except TypeError:
                return False
        return False

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        if not isinstance(other, Version):
            other = Version(other, guess_delimiters=True)

        if self.parsed_version is None or other.parsed_version is None:
            return False

        for v1, v2 in zip_longest(self.parsed_version, other.parsed_version):
            if not self.case_sensitive:
                if isinstance(v1, str):
                    v1 = v1.lower()
                if isinstance(v2, str):
                    v2 = v2.lower()

            if v1 is None:
                v1 = 0
            elif v2 is None:
                v2 = 0
            try:
                if v1 < v2:
                    return True
                elif v1 > v2:
                    return False
                elif v1 == v2:
                    continue
            except TypeError:
                return False
        return False

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    @staticmethod
    def normalize(items):
        """Convert items in list to their proper type"""
        results = []
        for i in range(len(items)):
            try:
                results.append(int(items[i]))
            except ValueError:
                results.append(items[i])
        return results

    @staticmethod
    def split(s, *delimiters):
        """Split string with one or more delimiters"""
        result = []
        tmp = []

        for ch in s:
            if ch in delimiters:
                result.extend(tmp)
                result.append(ch)
                tmp = []
            else:
                tmp.append(ch)
        result.extend(tmp)
        return result

    @staticmethod
    def guess_delimiters(s):
        """Guess delimiters from a list of punctuation"""
        results = set()
        for ch in string.punctuation:
            if ch in s:
                results.add(ch)
        return results
