"""
Responsible for route between screens
"""
root = None
controllers = []

def segue(fr, to=None, modal=False):
    global root
    # Close modal view if we go back to its main view or segue is not modal
    if not modal or fr == root.modal:
        root.modal = None
        # Remove last controller from the controller's stack if we segue back
        if len(controllers) >= 2 and fr == controllers[-1] and to == controllers[-2]:
            controllers.pop()
        # Add new controller to the stack
        elif to:
            controllers.append(to)
        # Show new controller
        root = controllers[-1]
    # Show new modal controller 
    elif to:
        root.modal = to

def shown(view):
    global root
    # Get main view of the controller
    main_view = view.super if view.super else view
    # Return if view is shown as a main view on the screen
    if root.modal:
        return root.modal.view == main_view
    else:
        return root.view == main_view
