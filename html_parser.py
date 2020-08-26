from html.parser import HTMLParser


class GetLinks(HTMLParser):
    def __init__(self):
        super(GetLinks, self).__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value not in ['?C=N;O=D', '?C=M;O=A', '?C=S;O=A', '?C=D;O=A', '/']:
                    self.links.append(value)

    def feed(self, data):
        super(GetLinks, self).feed(data)
        return self.links
