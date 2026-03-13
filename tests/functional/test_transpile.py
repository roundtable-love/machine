from machine.spec import LANGUAGE_CODES
from machine.providers import transpile

import pytest


@pytest.mark.parametrize("lang", LANGUAGE_CODES)
def test_lossless_round_trip(lang):
    """
    Ensures 1:1 logic parity across the Zion-to-Babylon-to-Zion wash.
    """
    original_intent = "PEER MUST PROTECT THE ROOT"

    # 1. FORWARD PASS (English/IR -> Target)
    forward_build = transpile(original_intent, lang)

    # 2. REVERSE PASS (Target -> English/IR)
    reconstructed_intent = transpile(forward_build, "machine_ir")

    # 3. PARITY ASSERTION
    assert reconstructed_intent == original_intent, (
        f"CRITICAL: Parity Violation in Node [{lang}]. Logic Drift Detected."
    )
