# Create your views here.
import urllib
import json
import datetime

from django.http import HttpResponseServerError
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse


class MetaProxy(object):
    def __init__(self, data):
        self._data = data

    def _make_key(self, key):
        return '$%s' % key

    def __getitem__(self, key):
        value = self._data[self._make_key(key)]
        if key in ('created', 'edited'):
            value = datetime.datetime.fromtimestamp(value)
        if key == 'items':
            return [APIDocument(x) for x in value]
        if key == 'services':
            return dict((k, APIDocument(v)) for k, v in value.items())
        if key == 'links':
            return [APIDocument(x) for x in value]
        return value

    def __contains__(self, key):
        return self._make_key(key) in self._data


class AttrsProxy(object):
    def __init__(self, data):
        self._data = data

    def _is_valid_key(self, key):
        return not key.startswith('$')

    def __getitem__(self, key):
        if not self._is_valid_key(key):
            raise AttributeError
        return self._data[key]

    def __contains__(self, key):
        return self._is_valid_key(key) and key in self._data

    def items(self):
        for key, value in self._data.items():
            if self._is_valid_key(key):
                yield (key, value)


class APIDocument(object):
    def __init__(self, data):
        self._data = data
        self.meta = MetaProxy(data)
        self.attrs = AttrsProxy(data)

    def is_service(self):
        return self._data.get('$type') == 'application/vnd.pbs-service+json'

    def is_collection(self):
        return self._data.get('$type') == 'application/vnd.pbs-collection+json'

    def is_resource(self):
        return self._data.get('$type') == 'application/vnd.pbs-resource+json'

    def raw(self):
        return json.dumps(self._data, indent=4)

    def page_name(self):
        if self.is_resource():
            return self._data.get('$class')
        if self.is_collection():
            return self._data.get('$elements') + 's'

    def pages(self):
        page_size = self._data['$page_size']
        items_count = self._data['$items_count']
        return items_count / page_size + 1

    def has_pages(self):
        return '$page_control' in self._data

    def has_next(self):
        current_page = int(self._data['$page'])
        return current_page < self.pages()

    def has_prev(self):
        #current_page = self._data['$page']
        current_page = int(self._data['$page'])
        return current_page > 1

    def next_url(self):
        template = self._data['$page_control']
        #current_page = self._data['$page']
        print self._data
        current_page = int(self._data['$page'])
        return template.replace('{page}', str(current_page + 1))

    def prev_url(self):
        template = self._data['$page_control']
        #current_page = self._data['$page']
        current_page = int(self._data['$page'])
        return template.replace('{page}', str(current_page - 1))


def load_document(wrapped):
    def wrapper(request, url):
        url = url.encode('ascii')
        try:
            #XXX: Hack for apache.
            if not url.startswith('http://'):
                if url.startswith('http:/'):
                    url = 'http://' + url[6:]
                else:
                    url = 'http://' + url
            document = json.loads(urllib.urlopen(url).read())
        except IOError:
            return HttpResponseServerError("Can't read location.")
        except ValueError:
            return HttpResponseServerError("Can't parse response.")
        return wrapped(request, url, APIDocument(document))
    return wrapper


def landing(request):
    if request.method == 'POST':
        api_location = request.POST.get('api_location')
        if api_location is None:
            return HttpResponseServerError("No location.")
        return redirect(reverse(result, args=[api_location]))

    return render_to_response(
        'explorer/landing.html', {}, context_instance=RequestContext(request)
    )


@load_document
def result(request, api_location, document):

    if document.is_resource():
        template = 'explorer/resource.html'
    if document.is_collection():
        template = 'explorer/collection.html'
    if document.is_service():
        template = 'explorer/service.html'

    return render_to_response(
        template, {
            'document': document,
            'url': api_location,
        },
        context_instance=RequestContext(request)
    )


@load_document
def source(request, api_location, document):
    return render_to_response(
        'explorer/source.html', {
            'url': api_location,
            'document': document,
            'show_source': True,
        },
        context_instance=RequestContext(request)
    )
