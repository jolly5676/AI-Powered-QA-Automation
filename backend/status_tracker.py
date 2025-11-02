import threading

class StatusTracker:
    """Thread-safe global progress tracker for live Streamlit display."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StatusTracker, cls).__new__(cls)
                cls._instance.status = {}
        return cls._instance

    def update(self, filename, message, stage=None, percent=None):
        if filename not in self.status:
            self.status[filename] = {"stage": stage or "Start", "progress": percent or 0, "message": message}
        else:
            self.status[filename].update({"stage": stage or "Start", "progress": percent or 0, "message": message})
        print(f"[{filename}] {message}")

    def get_status(self):
        return dict(self.status)
