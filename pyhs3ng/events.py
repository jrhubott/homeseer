"""Models a HomeSeer event"""


class HomeSeerEvent:
    def __init__(self, raw, request):
        self._raw = raw
        self._request = request

    @property
    def group(self):
        return self._raw["Group"]

    @property
    def name(self):
        return self._raw["Name"]

    async def run(self):
        json = {"action": "runevent", "group": self.group, "name": self.name}
        await self._request("post", json=json)
