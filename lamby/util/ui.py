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


def initialize_projects(app, current_user):
    projects = [
        Project('Project Name', 'Description'),
        Project('Project Name', 'Description'),
        Project('Project Name', 'Description'),
        Project('Project Name', 'Description'),
        Project('Project Name', 'Description')
    ]
    app.jinja_env.globals['dummy_projects'] = projects
