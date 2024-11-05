import re


async def check_public_link(link: str) -> bool:
    public_tme_regex = r't\.me\/([\w\d_]+)\/(\d+)'
    private_tme_regex = r't\.me\/c\/(-?\d+)\/(\d+)'
    public_tg_regex = r'tg:\/\/resolve\?domain=([\w\d_]+)&post=(\d+)'
    private_tg_regex = r'tg:\/\/privatepost\?channel=(-?\d+)&post=(\d+)'

    private_match = re.search(private_tme_regex, link) or re.search(private_tg_regex, link)
    public_match = re.search(public_tme_regex, link) or re.search(public_tg_regex, link)
    if not private_match and public_match:
        return True, public_match.groups()
    return False, None
