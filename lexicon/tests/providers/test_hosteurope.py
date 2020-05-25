# Test for one implementation of the interface
from unittest import TestCase

import pytest

from lexicon.tests.providers.integration_tests import IntegrationTests, _vcr_integration_test


# Hook into testing framework by inheriting unittest.TestCase and reuse
# the tests which *each and every* implementation of the interface must
# pass, by inheritance from integration_tests.IntegrationTests
class HosteuropeProviderTests(TestCase, IntegrationTests):
    """Integration tests for Hosteurope provider"""
    provider_name = 'hosteurope'
    domain = 'invenium.io'

    def _filter_post_data_parameters(self):
        return ['brandId', 'identifier', 'password', 'recaptcha']

    def _filter_headers(self):
        return ['cookie', ':path:']

    def _filter_query_parameters(self):
        return ['brandId', 'identifier', 'password', 'recaptcha']

    def _filter_response(self, response):
        """See `IntegrationTests._filter_response` for more information on how
        to filter the provider response."""

        if response['headers'].get('set-cookie', None) is not None:
            del response['headers']['set-cookie']

        return response

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_authenticate(self):
        super(HosteuropeProviderTests, self).test_provider_authenticate()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_authenticate_with_unmanaged_domain_should_fail(self):
        super(HosteuropeProviderTests, self).test_provider_authenticate_with_unmanaged_domain_should_fail()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_for_A_with_valid_name_and_content(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_for_A_with_valid_name_and_content()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_for_CNAME_with_valid_name_and_content(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_for_CNAME_with_valid_name_and_content()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_for_TXT_with_valid_name_and_content(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_for_TXT_with_valid_name_and_content()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_for_TXT_with_full_name_and_content(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_for_TXT_with_full_name_and_content()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_for_TXT_with_fqdn_name_and_content(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_for_TXT_with_fqdn_name_and_content()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_no_arguments_should_list_all(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_list_records_with_no_arguments_should_list_all()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_name_filter_should_return_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_list_records_with_name_filter_should_return_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_full_name_filter_should_return_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_list_records_with_full_name_filter_should_return_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_fqdn_name_filter_should_return_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_list_records_with_fqdn_name_filter_should_return_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_after_setting_ttl(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_list_records_after_setting_ttl()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_should_return_empty_list_if_no_records_found(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_list_records_should_return_empty_list_if_no_records_found()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_arguments_should_filter_list(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_list_records_with_arguments_should_filter_list()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_update_record_should_modify_record(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_update_record_should_modify_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_update_record_should_modify_record_name_specified(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_update_record_should_modify_record_name_specified()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_update_record_with_full_name_should_modify_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_update_record_with_full_name_should_modify_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_update_record_with_fqdn_name_should_modify_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_update_record_with_fqdn_name_should_modify_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_by_identifier_should_remove_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_delete_record_by_identifier_should_remove_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_by_filter_should_remove_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_delete_record_by_filter_should_remove_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_by_filter_with_full_name_should_remove_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_delete_record_by_filter_with_full_name_should_remove_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_by_filter_with_fqdn_name_should_remove_record(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_delete_record_by_filter_with_fqdn_name_should_remove_record()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_with_duplicate_records_should_be_noop(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_with_duplicate_records_should_be_noop()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_create_record_multiple_times_should_create_record_set(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_create_record_multiple_times_should_create_record_set()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_with_invalid_filter_should_be_empty_list(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_list_records_with_invalid_filter_should_be_empty_list()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_list_records_should_handle_record_sets(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_list_records_should_handle_record_sets()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_with_record_set_name_remove_all(self):
        super(HosteuropeProviderTests, self).test_provider_when_calling_delete_record_with_record_set_name_remove_all()

    @_vcr_integration_test
    @pytest.mark.skip(reason="NONE")
    def test_provider_when_calling_delete_record_with_record_set_by_content_should_leave_others_untouched(self):
        super(HosteuropeProviderTests,
              self).test_provider_when_calling_delete_record_with_record_set_by_content_should_leave_others_untouched()
