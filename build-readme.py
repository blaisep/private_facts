import datetime
import operator
import pathlib
import re
import typing

import feedparser
import httpx
import jinja2

ROOT_DIR = pathlib.Path(__file__).parent.resolve()
README_FILE = ROOT_DIR / "README_generated.md"
TEMPLATE_FILE = ROOT_DIR / "TEMPLATE.md"
NOTE_URL = "https://github.com/bbelderbos/bobcodesit/blob/main/{note_filename}"
NOTES_INDEX = "https://raw.githubusercontent.com/bbelderbos/bobcodesit/main/index.md"
BLUESKY_FEED = "https://bsky.app/profile/did:plc:e2ndzn2nunpgqh2r2b43ijk5/rss"
NUMBER_BLUESKY_POSTS = 3
NUMBER_TIPS = 5


class ContentPiece(typing.NamedTuple):
    url: str
    title: str
    date: str


def _parse_notes_index() -> set[tuple[str, str]]:
    """
    Parse bobcodesit tips index to get tuples of
    (title, note_file)
    """
    resp = httpx.get(NOTES_INDEX)
    notes = re.findall(r"notes/\d+\.md", resp.text)
    pat = re.compile(r"\[(.*?)\]\((notes/\d+\.md)")
    notes = re.findall(pat, resp.text)
    return set(notes)


def _convert_to_raw_url(github_url: str) -> str:
    return github_url.replace("github.com", "raw.githubusercontent.com").replace(
        "/blob/", "/refs/heads/"
    )


def _fetch_file_content(raw_url: str) -> str:
    response = httpx.get(raw_url)
    response.raise_for_status()
    return response.text


def _extract_title_and_paragraph(content: str) -> str | None:
    lines = content.splitlines()
    title = lines[0].lstrip("#").strip() if lines[0].startswith("#") else None
    paragraphs = [
        line.strip() for line in lines if line.strip() and not line.startswith("#")
    ]
    first_paragraph = paragraphs[0] if paragraphs else None
    if title is None or first_paragraph is None:
        return None
    return f"{title}: {first_paragraph} ..."


def get_latest_tips(num_items: int = NUMBER_TIPS) -> list[ContentPiece]:
    """
    Get the last tips from bobcodesit tips GitHub repo
    """
    notes = _parse_notes_index()
    last_notes = sorted(notes, key=operator.itemgetter(1), reverse=True)[:num_items]

    content_pieces = []
    for note in last_notes:
        title, md_file = note

        url = NOTE_URL.format(note_filename=md_file)

        tstamp_number = re.sub(r"notes/(\d+)\.md", r"\1", md_file)
        tstamp_dt = datetime.datetime.strptime(tstamp_number, "%Y%m%d%H%M%S")
        date_readable = tstamp_dt.strftime("%d %b %Y")

        raw_url = _convert_to_raw_url(url)
        content = _fetch_file_content(raw_url)
        title = _extract_title_and_paragraph(content)
        if title is not None:
            content_pieces.append(ContentPiece(url=url, title=title, date=date_readable))
    return content_pieces


def get_latest_bluesky_posts(num_items: int = NUMBER_BLUESKY_POSTS) -> list[ContentPiece]:
    """
    Get the last bluesly posts from feed
    """
    entries = feedparser.parse(BLUESKY_FEED).entries
    data = []
    for entry in entries[:num_items]:
        data.append(
            ContentPiece(
                url=entry.link, title=entry.description, date=entry.published[:11]
            )
        )
    return data


def generate_readme(content: dict[str, list[ContentPiece]]) -> None:
    """
    Generate Readme file from template file
    """
    template_content = TEMPLATE_FILE.read_text()
    jinja_template = jinja2.Template(template_content)
    updated_content = jinja_template.render(**content)
    README_FILE.write_text(updated_content)


if __name__ == "__main__":
    content = dict(
        posts=get_latest_bluesky_posts(),
        tips=get_latest_tips(),
    )
    generate_readme(content)
