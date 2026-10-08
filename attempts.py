MAX_ATTEMPTS = 5

attempt_data = {}


def record_failure(username, level):
    """Increment the failed-attempt count for a username at a given level.
    Returns (attempts_used, attempts_left)."""

    if username not in attempt_data:
        attempt_data[username] = {}

    attempt_data[username][level] = attempt_data[username].get(level, 0) + 1

    attempts_used = attempt_data[username][level]
    attempts_left = MAX_ATTEMPTS - attempts_used

    return attempts_used, attempts_left


def reset_attempts(username):
    """Clear all attempt counters for a username (used on success or lockout)."""

    if username in attempt_data:
        del attempt_data[username]


def reset_level(username, level):
    """Clear the attempt counter for just one level."""

    if username in attempt_data and level in attempt_data[username]:
        del attempt_data[username][level]