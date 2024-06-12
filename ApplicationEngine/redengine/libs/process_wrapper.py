class ProcessWrapper():
    """Handles communication between parent and child process"""
    def __init__(self, parent = None, child = None) -> None:
        self.parent_process = parent
        self.child_process = child

    def set_child(self, child):
        self.child_process = child
        
    def set_parent(self, parent):
        self.parent_process = parent
        