from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RegenerateDesignerKeyTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()

        self.client.subaccounts.regenerate_designer_key(subaccount.id)

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.designerKey).is_not_blank().is_not_equal_to(subaccount.designerKey)
