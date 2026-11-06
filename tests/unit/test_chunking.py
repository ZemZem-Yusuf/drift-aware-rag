import itertools

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from driftrag.rag.chunking import (
    ChunkerConfig,
    chunk_page,
    clean_markup,
    parse_page,
    split_sections,
)

PAGE = """---
reviewers:
- someone
title: "Pods"
content_type: concept
---

<!-- overview -->

_Pods_ are the smallest deployable units. A Pod is a group of one or more
{{< glossary_tooltip text="containers" term_id="container" >}}, with shared storage.

## What is a Pod?

{{< note >}}
You need a [container runtime](/docs/setup/container-runtimes/) on each node.
{{< /note >}}

### Using Pods

Example manifest:

```yaml
# this is a YAML comment, not a heading
apiVersion: v1
kind: Pod

metadata:
  name: nginx
```

## Pod lifecycle

Pods are ephemeral.
"""


def test_front_matter_title_is_read_and_removed() -> None:
    page = parse_page(PAGE)
    assert page.title == "Pods"
    assert "reviewers" not in page.body
    assert "content_type" not in page.body


def test_hugo_markup_is_cleaned_but_meaning_kept() -> None:
    body = parse_page(PAGE).body
    assert "group of one or more\ncontainers, with shared storage" in body
    assert "{{" not in body
    assert "<!--" not in body
    assert "You need a container runtime on each node." in body  # link text kept, URL dropped


def test_images_keep_alt_text() -> None:
    assert clean_markup("See ![the Pod diagram](/img/pod.svg) here.") == "See the Pod diagram here."


def test_sections_get_heading_paths_and_code_comments_are_not_headings() -> None:
    page = parse_page(PAGE)
    paths = [path for path, _ in split_sections(page.title, page.body)]
    assert paths == [
        "Pods",
        "Pods > What is a Pod?",
        "Pods > What is a Pod? > Using Pods",
        "Pods > Pod lifecycle",
    ]


def test_code_blocks_stay_whole() -> None:
    chunks = chunk_page(PAGE, ChunkerConfig())
    code_chunk = next(c for c in chunks if "apiVersion" in c.content)
    assert "# this is a YAML comment" in code_chunk.content
    assert "name: nginx" in code_chunk.content  # blank line inside the fence didn't split it


def test_without_front_matter_the_fallback_title_is_used() -> None:
    chunks = chunk_page(
        "Just text that is long enough to be a chunk on its own." * 3,
        ChunkerConfig(),
        fallback_title="concepts/x.md",
    )
    assert chunks[0].heading_path == "concepts/x.md"


def test_long_sections_are_split_with_overlap() -> None:
    paragraphs = [f"Paragraph {i}. " + "word " * 30 for i in range(12)]
    page = "# Title\n\n" + "\n\n".join(paragraphs)
    config = ChunkerConfig(max_chars=500, overlap_chars=200, min_chars=0)

    chunks = chunk_page(page, config)

    assert len(chunks) > 1
    assert all(len(c.content) <= 500 for c in chunks)
    # Each chunk after the first starts with the last paragraph of the previous chunk.
    for previous, current in itertools.pairwise(chunks):
        last_paragraph = previous.content.split("\n\n")[-1]
        assert current.content.startswith(last_paragraph)


def test_tiny_trailing_chunks_are_merged() -> None:
    page = "# T\n\n" + "a" * 150 + "\n\nok"
    chunks = chunk_page(page, ChunkerConfig(max_chars=200, overlap_chars=0, min_chars=50))
    assert len(chunks) == 1
    assert chunks[0].content.endswith("ok")


def test_config_id_changes_with_any_parameter() -> None:
    assert ChunkerConfig().config_id == ChunkerConfig().config_id
    assert ChunkerConfig().config_id != ChunkerConfig(max_chars=1000).config_id


def test_overlap_must_be_small() -> None:
    with pytest.raises(ValidationError, match="overlap"):
        ChunkerConfig(max_chars=400, overlap_chars=300)


markdown_text = st.lists(
    st.one_of(
        st.text(alphabet=st.characters(categories=["L", "N", "Zs"]), min_size=1, max_size=900),
        st.sampled_from(["# H1", "## H2", "### H3", "```", "", "- item"]),
    ),
    max_size=40,
).map("\n".join)


@settings(max_examples=150)
@given(markdown_text, st.integers(min_value=200, max_value=1500))
def test_chunks_respect_limits_for_any_input(text: str, max_chars: int) -> None:
    config = ChunkerConfig(max_chars=max_chars, overlap_chars=max_chars // 4, min_chars=40)
    chunks = chunk_page(text, config)
    assert all(len(c.content) <= max_chars for c in chunks)
    assert all(c.content.strip() for c in chunks)
    assert [c.ordinal for c in chunks] == list(range(len(chunks)))
    assert chunk_page(text, config) == chunks  # deterministic
