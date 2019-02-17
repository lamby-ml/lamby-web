import random


class Navlink(object):
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

    def get_name(self):
        return self.name

    def get_endpoint(self):
        return self.endpoint

    def __repr__(self):
        return '<endpoint=%s name=%s />' % (self.endpoint, self.name)


def initialize_navlinks(app, current_user):
    navlinks = [Navlink('HOME', 'home.index')]
    authenticated_navlinks = navlinks + [
        Navlink('PROFILE', 'profile.index'),
        Navlink('LOGOUT', 'auth.logout'),
    ]
    anonymous_navlinks = navlinks + [
        Navlink('SIGNUP', 'auth.signup'),
        Navlink('LOGIN', 'auth.login')
    ]
    app.jinja_env.globals['authenticated_navlinks'] = authenticated_navlinks
    app.jinja_env.globals['anonymous_navlinks'] = anonymous_navlinks


class Project(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


def get_dummy_projects():
    dummy_project_names = [
        'WasteIgnite',
        'Balln',
        'KnowHeckHere',
        'Topstr',
        'SmartRot',
        'MessageFuse',
        'Machine.ly',
        'StripMetrics',
        'EquityFloat',
        'Automatoc',
        'mtools',
        'SureXML',
        'CodePTD',
        'freecode',
        'openm',
        'desklabs',
        'DocBot',
        'flexml',
        'itools',
        'strexml',
        'zcloud',
        'opench',
        'dataspec',
        'coinhy.pe',
        'heatmaps',
        'visualyser',
        'smartm',
        'mSOURCE',
        'datamp',
        'plexml'
        'mlabs',
        'shareredy',
        'lexml',
        'vocoder',
        'logml',
        'blockchain.md',
        'batchip',
        'lauchyoursaas',
        'gtron',
        'teachip',
        'ReadyCrypt',
        'BuxMachine',
        'ctools',
        'cworks',
        'clogix',
        'lmonlabs',
        'MachinePath',
        'idexio'
    ]

    return [
        Project(name, 'Description')
        for name in random.sample(dummy_project_names, random.randint(5, 10))
    ]
