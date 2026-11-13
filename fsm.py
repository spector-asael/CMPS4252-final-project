# --- Two-Bit FSM State Encodings ---
STATE_TEMPERATURE = 0b00  # S0: 00
STATE_HUMIDITY = 0b01     # S1: 01
STATE_DISTANCE = 0b10     # S2: 10
STATE_INVALID = 0b11      # S3: 11 (Unused / invalid state)


def next_state(current_state):
    """Advance to the next 2-bit FSM state and recover from invalid state 11."""
    if current_state == STATE_TEMPERATURE:
        return STATE_HUMIDITY
    elif current_state == STATE_HUMIDITY:
        return STATE_DISTANCE
    elif current_state == STATE_DISTANCE:
        return STATE_TEMPERATURE
    else:
        return STATE_TEMPERATURE


def state_to_bits(state):
    """Return the 2-bit binary string representation (e.g., '00', '01', '10')."""
    return f"{state & 0b11:02b}"
