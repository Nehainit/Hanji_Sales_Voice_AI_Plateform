from app.voice.active_calls import ActiveCalls


# Spec scenario (voice/outbound-calling: One call at a time per customer)
def test_second_call_to_same_number_is_refused():
    calls = ActiveCalls()
    assert calls.start("9829041122") is True
    assert calls.start("9829041122") is False


def test_number_can_be_called_again_after_call_ends():
    calls = ActiveCalls()
    calls.start("9829041122")
    calls.end("9829041122")
    assert calls.start("9829041122") is True


def test_different_numbers_are_independent():
    calls = ActiveCalls()
    assert calls.start("9829041122") is True
    assert calls.start("9876543210") is True
    assert "9829041122" in calls and "9876543210" in calls


def test_ending_a_number_not_on_a_call_is_harmless():
    calls = ActiveCalls()
    calls.end("9829041122")
    assert "9829041122" not in calls
