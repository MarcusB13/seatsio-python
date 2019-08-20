from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrievePublishedVersionThumbnailTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()

        thumbnail = self.client.charts.retrieve_published_version_thumbnail(chart.key)

        assert_that(thumbnail).contains("PNG")
