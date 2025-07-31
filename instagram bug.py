import threading
import time
import random

class CommentLikeSystem:
    """
    Simulates Instagram's like system with a basic in-memory store.
    Prevents multiple likes from the same user for the same comment.
    """
    def _init_(self):
        self.likes = set()
        self.lock = threading.Lock()

    def like_comment(self, user_id, comment_id):
        with self.lock:
            key = (user_id, comment_id)
            if key not in self.likes:
                self.likes.add(key)
                print(f"[{threading.current_thread().name}] ✅ Like registered for {key}")
            else:
                print(f"[{threading.current_thread().name}] ⚠ Already liked {key}")
        time.sleep(random.uniform(0.05, 0.2))  # Simulate network/API delay

def simulate_user_taps(system, user_id, comment_id, tap_count):
    """
    Simulates rapid user taps by spawning threads to like a comment.
    """
    threads = []
    for i in range(tap_count):
        t = threading.Thread(
            target=system.like_comment,
            args=(user_id, comment_id),
            name=f"Tap-{i+1}"
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if _name_ == "_main_":
    comment_system = CommentLikeSystem()
    simulate_user_taps(comment_system, user_id="user_007", comment_id="comment_123", tap_count=10)
