from driftrag.golden_cli import apply_reviews, parse_reviews, render_sheet
from evalkit.golden import GoldenItem, RelevantSection


def golden(item_id: str, **extra: object) -> GoldenItem:
    data: dict[str, object] = {
        "id": item_id,
        "lang": "en",
        "question": "How do I scale a deployment?",
        "category": "command",
        "relevant": [{"document": "deployment.md", "section": "Deployments > Scaling"}],
        "reference_answer": "kubectl scale",
        "origin": "llm-drafted",
    }
    data.update(extra)
    return GoldenItem.model_validate(data)


def tick(sheet: str, item_id: str, label: str, notes: str = "") -> str:
    block_start = sheet.index(f"### `{item_id}`")
    box = sheet.index("- [ ] ", sheet.index(label, block_start) - 10)
    sheet = sheet[:box] + "- [x] " + sheet[box + 6 :]
    if notes:
        marker = sheet.index("**Notes:**", block_start) + len("**Notes:**")
        sheet = sheet[:marker] + "\n" + notes + sheet[marker:]
    return sheet


def excerpt(section: RelevantSection, lang: str) -> str | None:
    return f"Text of {section.section}"


ITEMS = [
    golden("aa-ok"),
    golden("bb-fix"),
    golden("cc-bad"),
    golden("dd-skip"),
    golden("ee-done", status="verified", verified_by="Someone"),
]


def test_sheet_shows_only_drafts_with_documentation_excerpts() -> None:
    sheet = render_sheet(ITEMS, excerpt)
    assert "### `aa-ok`" in sheet
    assert "### `ee-done`" not in sheet
    assert "> Text of Deployments > Scaling" in sheet


def test_round_trip_applies_decisions() -> None:
    sheet = render_sheet(ITEMS, excerpt)
    sheet = tick(sheet, "aa-ok", "Correct as written")
    sheet = tick(sheet, "bb-fix", "Needs changes", notes="Use --replicas in the answer")
    sheet = tick(sheet, "cc-bad", "Reject", notes="Not realistic")

    updated, report = apply_reviews(ITEMS, parse_reviews(sheet), "Youssef Zemzem")
    by_id = {i.id: i for i in updated}

    assert report["verified"] == ["aa-ok"]
    assert by_id["aa-ok"].status == "verified"
    assert by_id["aa-ok"].verified_by == "Youssef Zemzem"
    assert by_id["cc-bad"].status == "rejected"
    assert "Not realistic" in by_id["cc-bad"].notes
    assert by_id["bb-fix"].status == "draft"
    assert report["changes"] == ["bb-fix: Use --replicas in the answer"]
    assert report["unreviewed"] == ["dd-skip"]
    assert by_id["ee-done"] == ITEMS[4]


def test_two_ticked_boxes_is_an_error_and_changes_nothing() -> None:
    sheet = render_sheet([golden("aa-ok")], excerpt)
    sheet = tick(sheet, "aa-ok", "Correct as written")
    sheet = tick(sheet, "aa-ok", "Reject")
    updated, report = apply_reviews([golden("aa-ok")], parse_reviews(sheet), "Y")
    assert report["errors"] == ["aa-ok: more than one box ticked"]
    assert updated[0].status == "draft"


def test_ticks_with_spaces_inside_the_brackets_count() -> None:
    sheet = render_sheet([golden("aa-ok"), golden("bb-ok")], excerpt)
    sheet = sheet.replace("- [ ] ✅ Correct as written", "- [x ] ✅ Correct as written", 1)
    sheet = sheet.replace("- [ ] ✅ Correct as written", "- [ X] ✅ Correct as written", 1)
    reviews = parse_reviews(sheet)
    assert reviews["aa-ok"].decision == "verified"
    assert reviews["bb-ok"].decision == "verified"


def test_sheet_can_be_limited_to_the_first_drafts() -> None:
    sheet = render_sheet(ITEMS, excerpt, max_items=2)
    assert "### `aa-ok`" in sheet
    assert "### `bb-fix`" in sheet
    assert "### `cc-bad`" not in sheet
