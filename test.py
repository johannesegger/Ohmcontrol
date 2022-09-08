from fn import update_state, state_to_string

def test_update_state(state, watt_to_grid, expected_state):
    actual_state = update_state(state, watt_to_grid)
    if actual_state == expected_state:
        print(f"update_state(({state_to_string(state)}), {watt_to_grid}) = {state_to_string(actual_state)}")
    else:
        print(f"ERROR: update_state(({state_to_string(state)}), {watt_to_grid}) = {state_to_string(actual_state)}, but should be '{state_to_string(expected_state)}'")

test_update_state((0b00, 0.0), -10000.0, (0b00, 0.0))
test_update_state((0b00, 0.0), -6750.0, (0b00, 0.0))
test_update_state((0b00, 0.0), -4500.0, (0b00, 0.0))
test_update_state((0b00, 0.0), -2250.0, (0b00, 0.0))
test_update_state((0b00, 0.0), 0.0, (0b00, 0.0))
test_update_state((0b00, 0.0), 2250.0, (0b00, 0.7))
test_update_state((0b00, 0.0), 4500.0, (0b01, 0.5))
test_update_state((0b00, 0.0), 6750.0, (0b11, 0.2))
test_update_state((0b00, 0.0), 10000.0, (0b11, 1.0))

test_update_state((0b01, 0.0), -10000.0, (0b00, 0.0))
test_update_state((0b01, 0.0), -6750.0, (0b00, 0.0))
test_update_state((0b01, 0.0), -4500.0, (0b00, 0.0))
test_update_state((0b01, 0.0), -2250.0, (0b00, 0.2))
test_update_state((0b01, 0.0), 0.0, (0b01, 0.0))
test_update_state((0b01, 0.0), 2250.0, (0b01, 0.7))
test_update_state((0b01, 0.0), 4500.0, (0b11, 0.5))
test_update_state((0b01, 0.0), 6750.0, (0b11, 1.0))
test_update_state((0b01, 0.0), 10000.0, (0b11, 1.0))

test_update_state((0b11, 0.0), -10000.0, (0b00, 0.0))
test_update_state((0b11, 0.0), -6750.0, (0b00, 0.0))
test_update_state((0b11, 0.0), -4500.0, (0b00, 0.5))
test_update_state((0b11, 0.0), -2250.0, (0b01, 0.2))
test_update_state((0b11, 0.0), 0.0, (0b11, 0.0))
test_update_state((0b11, 0.0), 2250.0, (0b11, 0.7))
test_update_state((0b11, 0.0), 4500.0, (0b11, 1.0))
test_update_state((0b11, 0.0), 6750.0, (0b11, 1.0))
test_update_state((0b11, 0.0), 10000.0, (0b11, 1.0))

test_update_state((0b00, 0.5), 750, (0b00, 0.7))
test_update_state((0b00, 0.5), 3750, (0b01, 0.7))
test_update_state((0b00, 0.5), 2250, (0b01, 0.2))
