import io

import pytest
from fastapi.testclient import TestClient
from openpyxl import Workbook

from app.main import app
from app.orders.sheet import SheetError, check_sheet

HEADER = ["order_id", "customer_name", "phone", "amount", "product", "address"]


def order(n):
    return [f"KK{1000 + n}", f"Customer {n}", "98290 41122", "1299", "Cotton Anarkali Kurti", f"House {n}, Jaipur 302017"]


def fifty_rows_with_two_bad():
    """50 orders; Excel row 5 has no phone, row 9 has no amount (header is row 1)."""
    rows = [order(n) for n in range(50)]
    rows[5 - 2][2] = ""
    rows[9 - 2][3] = ""
    return rows


def as_csv(rows, header=HEADER):
    buf = io.StringIO()
    buf.write(",".join(header) + "\n")
    for r in rows:
        buf.write(",".join(f'"{v}"' for v in r) + "\n")
    return buf.getvalue().encode()


def as_xlsx(rows, header=HEADER):
    book = Workbook()
    sheet = book.active
    sheet.append(header)
    for r in rows:
        sheet.append(r)
    buf = io.BytesIO()
    book.save(buf)
    return buf.getvalue()


# Spec scenario (orders/order-intake: Sheet with two bad rows)
def test_csv_with_two_bad_rows():
    report = check_sheet("orders.csv", as_csv(fifty_rows_with_two_bad()))
    assert report.summary() == "48 orders ready"
    assert report.problems_text() == "Row 5: phone missing, Row 9: amount missing"


def test_xlsx_with_two_bad_rows():
    report = check_sheet("orders.xlsx", as_xlsx(fifty_rows_with_two_bad()))
    assert report.summary() == "48 orders ready"
    assert report.problems_text() == "Row 5: phone missing, Row 9: amount missing"


def test_upload_endpoint_reports_the_same():
    client = TestClient(app)
    res = client.post("/orders/sheet/check", files={"file": ("orders.csv", as_csv(fifty_rows_with_two_bad()), "text/csv")})
    assert res.status_code == 200
    body = res.json()
    assert body["ready"] == 48
    assert body["summary"] == "48 orders ready"
    assert body["problems"] == [{"row": 5, "problem": "phone missing"}, {"row": 9, "problem": "amount missing"}]


# Values sellers really type
def test_ready_order_is_cleaned():
    rows = [["KK1", "Priya Sharma", "+91 98290 41122", "₹1,299", "Cotton Anarkali Kurti", "B-24, Malviya Nagar, Jaipur"]]
    o = check_sheet("orders.csv", as_csv(rows)).orders[0]
    assert (o.row, o.phone, o.amount_paise) == (2, "9829041122", 129900)


def test_excel_numbers_for_phone_and_amount():
    rows = [["KK1", "Priya Sharma", 9829041122, 1299.5, "Kurti", "Jaipur"]]
    o = check_sheet("orders.xlsx", as_xlsx(rows)).orders[0]
    assert (o.phone, o.amount_paise) == ("9829041122", 129950)


def test_column_names_ignore_case_and_order():
    header = ["Phone", "ORDER_ID", "amount", "customer_name", "address", "product"]
    rows = [["9829041122", "KK1", "899", "Rahul Verma", "Lucknow", "Rayon Kurti"]]
    assert check_sheet("orders.csv", as_csv(rows, header)).ready_count == 1


def test_blank_lines_are_skipped():
    rows = [order(1), ["", "", "", "", "", ""], order(2)]
    report = check_sheet("orders.csv", as_csv(rows))
    assert report.ready_count == 2 and report.problems == []


# Row problems
def test_invalid_phone_and_amount():
    rows = [["KK1", "A", "98290 411", "1299", "P", "Addr"], ["KK2", "B", "9829041122", "free", "P", "Addr"]]
    report = check_sheet("orders.csv", as_csv(rows))
    assert report.problems == [(2, "phone invalid"), (3, "amount invalid")]


def test_several_problems_in_one_row():
    rows = [["KK1", "A", "", "", "P", "Addr"]]
    assert check_sheet("orders.csv", as_csv(rows)).problems == [(2, "phone missing and amount missing")]


def test_repeated_order_id():
    report = check_sheet("orders.csv", as_csv([order(1), order(1)]))
    assert report.ready_count == 1
    assert report.problems == [(3, "order id repeats row 2")]


# Whole-file problems
def test_missing_columns():
    with pytest.raises(SheetError, match="Missing columns: phone, amount."):
        check_sheet("orders.csv", as_csv([["KK1", "A", "P", "Addr"]], ["order_id", "customer_name", "product", "address"]))


def test_wrong_file_type():
    with pytest.raises(SheetError, match="Please upload a .csv or .xlsx file."):
        check_sheet("orders.pdf", b"%PDF")


def test_endpoint_explains_wrong_file_type():
    res = TestClient(app).post("/orders/sheet/check", files={"file": ("orders.pdf", b"%PDF", "application/pdf")})
    assert res.status_code == 400
    assert res.json()["detail"] == "Please upload a .csv or .xlsx file."
