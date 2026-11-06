# Thin wrapper for Linux/macOS/CI. On Windows, run the same tasks with `uv run poe <task>`.
.PHONY: install check lint format typecheck test audit dev corpus migrate up down

install:   ; uv sync
check:     ; uv run poe check
lint:      ; uv run poe lint
format:    ; uv run poe format
typecheck: ; uv run poe typecheck
test:      ; uv run poe test
audit:     ; uv run poe audit
dev:       ; uv run poe dev
corpus:    ; uv run poe corpus
migrate:   ; uv run poe migrate
up:        ; docker compose -f deploy/compose.yaml --env-file .env --profile core up -d --build
down:      ; docker compose -f deploy/compose.yaml --env-file .env --profile core down
