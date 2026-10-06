"""Order sheet upload: check the file first, then save and plan calls only on "Start calling"."""
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile

from app.integrations import supabase
from app.orders.sheet import SheetError, SheetReport, check_sheet
from app.scheduler.planning import load_call_settings, plan_first_call
from app.scheduler.queue import CallQueue, get_queue

router = APIRouter(prefix="/orders")

MAX_SHEET_BYTES = 5 * 1024 * 1024


def _checked(filename: str, data: bytes) -> SheetReport:
    if len(data) > MAX_SHEET_BYTES:
        raise HTTPException(413, "This file is bigger than 5 MB. Split it into smaller sheets.")
    try:
        return check_sheet(filename, data)
    except SheetError as e:
        raise HTTPException(400, str(e))


def _problems(report: SheetReport) -> dict:
    return {
        "problems": [{"row": row, "problem": problem} for row, problem in report.problems],
        "problems_text": report.problems_text(),
    }


@router.post("/sheet/check")
async def check_uploaded_sheet(file: UploadFile):
    """Step 1: report what's ready. Saves nothing and plans no calls."""
    report = _checked(file.filename or "", await file.read())
    return {"ready": report.ready_count, "summary": report.summary(), **_problems(report)}


# TODO(Phase 3): take the store from the logged-in seller instead of a form field.
@router.post("/sheet/start")
def start_calling_sheet(file: UploadFile, store_id: str = Form(...), queue: CallQueue = Depends(get_queue)):
    """Step 2, the seller pressed "Start calling": save the ready orders and plan their first calls."""
    report = _checked(file.filename or "", file.file.read())
    if not supabase.get_store(store_id):
        raise HTTPException(404, "Store not found.")
    settings = load_call_settings(supabase, store_id)
    saved = planned = 0
    for o in report.orders:
        row, created = supabase.save_order({
            "store_id": store_id, "external_order_id": o.order_id, "customer_name": o.customer_name,
            "customer_phone": o.phone, "amount_paise": o.amount_paise,
            "product_summary": o.product, "address": o.address,
        })
        if created:
            saved += 1
            plan_first_call(queue, row, settings)
            planned += 1
    return {"saved": saved, "already_saved": report.ready_count - saved, "calls_planned": planned, **_problems(report)}
