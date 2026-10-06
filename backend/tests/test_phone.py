from app.phone import normalize_mobile


# Spec scenarios (voice/outbound-calling: Calls Indian mobile numbers only)
def test_valid_number_with_plus91():
    assert normalize_mobile("+91 98290 41122") == "9829041122"


def test_number_too_short_is_rejected():
    assert normalize_mobile("98290 411") is None


# Other ways sellers' orders write the same number
def test_plain_ten_digits():
    assert normalize_mobile("9829041122") == "9829041122"


def test_leading_zero():
    assert normalize_mobile("098290 41122") == "9829041122"


def test_91_without_plus():
    assert normalize_mobile("919829041122") == "9829041122"


def test_dashes_dots_and_brackets():
    assert normalize_mobile("(+91) 98290-411.22") == "9829041122"


# Numbers that must not be called
def test_empty_or_missing():
    assert normalize_mobile("") is None
    assert normalize_mobile(None) is None


def test_too_long():
    assert normalize_mobile("98290411223") is None


def test_landline_style_start_digit():
    assert normalize_mobile("0141 2345678") is None  # Jaipur landline


def test_letters():
    assert normalize_mobile("98290 4112A") is None


def test_foreign_country_code():
    assert normalize_mobile("+1 415 555 0100") is None
