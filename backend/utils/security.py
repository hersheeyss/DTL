import hashlib

def hash_identity(student_id):
    return hashlib.sha256(student_id.encode()).hexdigest()
