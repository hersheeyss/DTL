import hashlib

def hash_identity(student_id: str) -> str:
    """Hash student_id so we don't store it directly in votes table."""
    return hashlib.sha256(student_id.encode()).hexdigest()
