from driftrag.rag.chunking import ChunkerConfig, chunk_page
from driftrag.rag.code_samples import normalise_sample_path, resolve_code_samples

FILES = {
    "pods/simple-pod.yaml": "apiVersion: v1\nkind: Pod\nmetadata:\n  name: nginx\n",
    "configmap/env.yaml": "envFrom:\n- configMapRef:\n    name: special-config\n",
    "docs/readme.md.txt": "Use ```fences``` inside\n",
}


def lookup(path: str) -> str | None:
    return FILES.get(path)


def test_code_sample_becomes_a_labelled_code_block() -> None:
    page = 'Create the Pod:\n\n{{% code_sample file="pods/simple-pod.yaml" %}}\n\nThen apply it.'
    result = resolve_code_samples(page, lookup)
    assert result.resolved == 1
    assert result.missing == []
    assert "Example file `pods/simple-pod.yaml`:\n```yaml\napiVersion: v1" in result.text
    assert "name: nginx\n```" in result.text
    assert "{{" not in result.text


def test_old_codenew_shortcode_leading_slash_and_language_attribute() -> None:
    page = (
        '{{< codenew file="/configmap/env.yaml" >}}\n'
        '{{% code_sample language="json" file="pods/simple-pod.yaml" %}}'
    )
    result = resolve_code_samples(page, lookup)
    assert result.resolved == 2
    assert "Example file `configmap/env.yaml`:\n```yaml\nenvFrom:" in result.text
    assert "```json\napiVersion" in result.text


def test_missing_file_is_left_for_the_chunker_and_reported() -> None:
    page = 'Text {{% code_sample file="nope/missing.yaml" %}} more'
    result = resolve_code_samples(page, lookup)
    assert result.resolved == 0
    assert result.missing == ["nope/missing.yaml"]
    assert result.text == page


def test_file_containing_backticks_gets_a_different_fence() -> None:
    result = resolve_code_samples('{{% code_sample file="docs/readme.md.txt" %}}', lookup)
    assert "~~~~txt\nUse ```fences``` inside\n~~~~" in result.text


def test_other_shortcodes_are_untouched() -> None:
    page = '{{< note >}}Careful{{< /note >}} {{< glossary_tooltip text="Pod" term_id="pod" >}}'
    assert resolve_code_samples(page, lookup).text == page


def test_inlined_yaml_survives_chunking_with_its_field_names() -> None:
    page = (
        "# Use a ConfigMap\n\nAll keys as env vars:\n\n"
        '{{% code_sample file="configmap/env.yaml" %}}'
    )
    chunks = chunk_page(resolve_code_samples(page, lookup).text, ChunkerConfig(min_chars=0))
    text = "\n".join(c.content for c in chunks)
    assert "configMapRef" in text
    assert "envFrom" in text


def test_normalise_sample_path() -> None:
    assert normalise_sample_path("/controllers/job.yaml") == "controllers/job.yaml"
    assert normalise_sample_path("pods/a.yaml") == "pods/a.yaml"
