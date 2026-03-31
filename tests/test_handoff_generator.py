import pytest

from scripts.handoff_generator import generate


# --- AC1: __init__.py exposes generate() and main() ---

def test_ac1_generate_callable():
    from scripts.handoff_generator import generate as g, main as m
    assert callable(g)
    assert callable(m)


# --- AC2: __main__.py entry-point pattern ---

def test_ac2_main_module_contents():
    import importlib.util, pathlib
    src = pathlib.Path(__file__).parent.parent / "scripts" / "handoff_generator" / "__main__.py"
    text = src.read_text()
    assert "from scripts.handoff_generator import main" in text
    assert "main()" in text


# --- AC3: pre-mission full args returns three sections in order ---

def test_ac3_pre_mission_full():
    result = generate("pre-mission", next_step="step", failed_attempts="none yet", transcript="Q: foo\nA: bar")
    lines = result.splitlines()
    headers = [l for l in lines if l.startswith("## ")]
    assert headers == ["## Next / Ongoing Step", "## Known Failed Attempts", "## Dev Interview Transcript"]
    assert "step" in result
    assert "none yet" in result
    assert "Q: foo" in result


# --- AC4: post-mission omits transcript, body is literal "None" ---

def test_ac4_post_mission_no_transcript():
    result = generate("post-mission", next_step="step", failed_attempts=None, transcript=None)
    headers = [l for l in result.splitlines() if l.startswith("## ")]
    assert headers == ["## Next / Ongoing Step", "## Known Failed Attempts"]
    assert "## Dev Interview Transcript" not in result
    assert "## Known Failed Attempts\n\nNone" in result


# --- AC5: pre-mission missing transcript raises ValueError naming --transcript ---

def test_ac5_pre_mission_missing_transcript():
    with pytest.raises(ValueError) as exc_info:
        generate("pre-mission", next_step="step", failed_attempts=None, transcript=None)
    assert "--transcript" in str(exc_info.value)


# --- AC6: post-mission with transcript raises ValueError ---

def test_ac6_post_mission_transcript_disallowed():
    with pytest.raises(ValueError) as exc_info:
        generate("post-mission", next_step="step", failed_attempts=None, transcript="Q&A")
    assert "--transcript" in str(exc_info.value)


# --- AC7: missing next_step raises ValueError naming --next-step ---

def test_ac7_missing_next_step_pre_mission():
    with pytest.raises(ValueError) as exc_info:
        generate("pre-mission", next_step=None, failed_attempts=None, transcript="t")
    assert "--next-step" in str(exc_info.value)


def test_ac7_missing_next_step_post_mission():
    with pytest.raises(ValueError) as exc_info:
        generate("post-mission", next_step=None, failed_attempts=None, transcript=None)
    assert "--next-step" in str(exc_info.value)


# --- AC8: mode=None raises ValueError naming the missing mode flag ---

def test_ac8_missing_mode():
    with pytest.raises(ValueError) as exc_info:
        generate(None, next_step="step", failed_attempts=None, transcript=None)
    msg = str(exc_info.value)
    assert "--pre-mission" in msg or "mode" in msg.lower()


# --- AC9: unrecognized mode raises ValueError naming conflicting/unrecognized mode ---

def test_ac9_unrecognized_mode():
    with pytest.raises(ValueError) as exc_info:
        generate("both", next_step="step", failed_attempts=None, transcript=None)
    assert "both" in str(exc_info.value) or "unrecognized" in str(exc_info.value).lower() or "conflicting" in str(exc_info.value).lower()


# --- AC10: pre-mission with failed_attempts=None has literal "None" body ---

def test_ac10_pre_mission_failed_attempts_default_none():
    result = generate("pre-mission", next_step="step", failed_attempts=None, transcript="t")
    assert "## Known Failed Attempts\n\nNone" in result
