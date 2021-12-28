
class Router:
    """
    Responsible for route between views
    """
    def segue(to, fr=None):
        # Hide "from" view if it given
        if fr: fr.disappear()
        # Show "to" view
        to.appear()