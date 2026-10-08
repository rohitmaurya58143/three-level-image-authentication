import secrets
import time

otp_data = {}

OTP_VALIDITY = 600     # 10 minutes
RESEND_COOLDOWN = 60   # 1 minute


def generate_otp(username):

    otp = str(secrets.randbelow(900000) + 100000)

    now = time.time()

    otp_data[username] = {
        "otp": otp,
        "expiry": now + OTP_VALIDITY,
        "last_sent": now
    }

    return otp


def can_resend_otp(username):

    if username not in otp_data:
        return True, 0

    elapsed = time.time() - otp_data[username]["last_sent"]

    if elapsed >= RESEND_COOLDOWN:
        return True, 0

    remaining = int(RESEND_COOLDOWN - elapsed)

    return False, remaining


def resend_otp(username):

    otp = str(secrets.randbelow(900000) + 100000)

    now = time.time()

    otp_data[username] = {
        "otp": otp,
        "expiry": now + OTP_VALIDITY,
        "last_sent": now
    }

    return otp


def verify_otp(username, entered_otp):

    if username not in otp_data:
        return False

    saved_otp = otp_data[username]["otp"]
    expiry_time = otp_data[username]["expiry"]

    if time.time() > expiry_time:
        del otp_data[username]
        return False

    if entered_otp == saved_otp:
        del otp_data[username]
        return True

    return False