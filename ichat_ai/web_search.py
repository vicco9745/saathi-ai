import base64
import html
import re
import urllib.parse
import urllib.request


BING_URL = "https://www.bing.com/search"


def _clean_text(value):
    value = re.sub(r"<.*?>", "", value or "")
    return html.unescape(value).strip()


def _original_url(bing_url):
    bing_url = html.unescape(bing_url)

    match = re.search(r"[?&]u=a1([^&]+)", bing_url)
    if not match:
        return bing_url

    encoded = match.group(1)

    try:
        return base64.urlsafe_b64decode(
            (encoded + "===")
        ).decode("utf-8", "ignore")
    except Exception:
        return bing_url


def fetch_webpage(url):
    if not url:
        return ""

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        response = urllib.request.urlopen(request, timeout=10)
        data = response.read().decode("utf-8", "ignore")
    except Exception:
        return ""

    data = re.sub(r"<script.*?</script>", " ", data, flags=re.S | re.I)
    data = re.sub(r"<style.*?</style>", " ", data, flags=re.S | re.I)
    data = re.sub(r"<[^>]+>", " ", data)
    data = html.unescape(data)
    data = re.sub(r"\s+", " ", data)

    return data.strip()


def search_web(query, limit=5):
    query = query.strip()

    if not query:
        return []

    params = urllib.parse.urlencode({
        "q": query,
        "setlang": "hi"
    })

    url = f"{BING_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    try:
        response = urllib.request.urlopen(request, timeout=10)
        data = response.read().decode("utf-8", "ignore")
    except Exception:
        return []

    items = re.findall(
        r'<li class="b_algo".*?</li>',
        data,
        re.S
    )

    results = []

    for item in items[:limit]:
        title_match = re.search(
            r"<h2.*?</h2>",
            item,
            re.S
        )

        description_match = re.search(
            r"<p[^>]*>.*?</p>",
            item,
            re.S
        )

        link_match = re.search(
            r'<h2[^>]*>\s*<a[^>]+href="([^"]+)"',
            item,
            re.S
        )

        title = _clean_text(
            title_match.group(0) if title_match else ""
        )

        description = _clean_text(
            description_match.group(0)
            if description_match
            else ""
        )

        link = _original_url(
            link_match.group(1)
            if link_match
            else ""
        )

        if title:
            page_content = fetch_webpage(link)
            results.append({
                "title": title,
                "description": description,
                "url": link,
                "content": page_content
            })

    return results
