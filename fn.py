from math import floor

def update_state(state, watt_to_grid):
    (on_off_state, pwm_ratio) = state

    watt_to_grid += pwm_ratio * 3000

    state_mask = 0b11
    while watt_to_grid >= 3000 and on_off_state < state_mask:
        on_off_state = (on_off_state << 1 | 0b1) & state_mask
        watt_to_grid -= 3000
    while watt_to_grid < 0 and on_off_state > 0:
        on_off_state = on_off_state >> 1
        watt_to_grid += 3000

    pwm_ratio = min(max(watt_to_grid / 3000.0, 0), 1)
    pwm_ratio = floor(pwm_ratio * 10) / 10

    return (on_off_state, pwm_ratio)

def state_to_string(state):
    (on_off_state, pwm_ratio) = state

    active_phases = 0
    i = on_off_state
    while i > 0:
        active_phases += 1
        i = i >> 1

    return f"{active_phases} {'phase' if active_phases == 1 else 'phases'} active, PWM ratio: {pwm_ratio:.0%}"
