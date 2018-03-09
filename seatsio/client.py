from bunch import bunchify

from seatsio.domain import Chart, Event, Subaccount
from seatsio.httpClient import HttpClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class Client:

    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.baseUrl = base_url
        self.httpClient = HttpClient(base_url, secret_key)
        self.charts = Charts(self.httpClient)
        self.events = Events(self.httpClient)
        self.subaccounts = Subaccounts(self.httpClient)


class Charts:

    def __init__(self, http_client):
        self.httpClient = http_client

    def retrieve(self, chart_key):
        response = self.httpClient.url("/charts/{key}", key=chart_key).get()
        return Chart(response.body)

    def retrieve_with_events(self, chart_key):
        response = self.httpClient.url("/charts/{key}?expand=events", key=chart_key).get()
        return Chart(response.body)

    def create(self, name=None, venue_type=None, categories=None):
        body = {}
        if name:
            body['name'] = name
        if venue_type:
            body['venueType'] = venue_type
        if categories:
            body['categories'] = categories
        response = self.httpClient.url("/charts").post(body)
        return Chart(response.body)

    def retrieve_published_version(self, key):
        response = self.httpClient.url("/charts/{key}/version/published", key=key).get()
        return bunchify(response.body)

    def copy(self, key):
        response = self.httpClient.url("/charts/{key}/version/published/actions/copy", key=key).post()
        return Chart(response.body)

    def copy_to_subaccount(self, chart_key, subaccount_id):
        response = self.httpClient.url("/charts/{key}/version/published/actions/copy-to/{subaccountId}",
                                       key=chart_key,
                                       subaccountId=subaccount_id).post()
        return Chart(response.body)

    def copy_draft_version(self, key):
        response = self.httpClient.url("/charts/{key}/version/draft/actions/copy", key=key).post()
        return Chart(response.body)

    def discard_draft_version(self, key):
        self.httpClient.url("/charts/{key}/version/draft/actions/discard", key=key).post()

    def update(self, key, name):
        body = {}
        if name:
            body['name'] = name
        self.httpClient.url("/charts/{key}", key=key).post(body)

    def move_to_archive(self, chart_key):
        self.httpClient.url("/charts/{key}/actions/move-to-archive", key=chart_key).post()

    def list_all_tags(self):
        response = self.httpClient.url("/charts/tags").get()
        return response.body["tags"]

    def add_tag(self, key, tag):
        return self.httpClient.url("/charts/{key}/tags/{tag}", key=key, tag=tag).post()

    def remove_tag(self, key, tag):
        self.httpClient.url("/charts/{key}/tags/{tag}", key=key, tag=tag).delete()

    def list(self):
        return Lister(PageFetcher(self.httpClient, "/charts"))

    def archive(self):
        return Lister(PageFetcher(self.httpClient, "/charts/archive"))


class Events:

    def __init__(self, http_client):
        self.httpClient = http_client

    def create(self, chart_key):
        body = {"chartKey": chart_key}
        response = self.httpClient.url("/events").post(body)
        return Event(response.body)


class Subaccounts:
    def __init__(self, http_client):
        self.http_client = http_client

    def create(self):
        response = self.http_client.url("/subaccounts").post()
        return Subaccount(response.body)
