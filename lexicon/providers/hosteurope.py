# coding=utf-8
"""Module for HostEurope"""
from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from lexicon.providers.base import Provider as BaseProvider

LOGGER = logging.getLogger(__name__)
NAMESERVER_DOMAINS = ['ns1.hans.hosteurope.de', 'ns2.hans.hosteurope.de']


def provider_parser(subparser):
    """Configure a provider parser for Hosteurope"""
    subparser.add_argument(
        "--auth-username",
        help="Specify HostEurope KIS Username"
    )
    subparser.add_argument(
        "--auth-password",
        help="Specify HostEurope KIS Password"
    )


class Provider(BaseProvider):
    """
    Implements the HostEurope AutoDNS Provider using the service https://kis.hosteurope.de/.

    """

    def __init__(self, config):
        super(Provider, self).__init__(config)
        LOGGER.warning(
            "HostEurope did not yet officially have an API for their AutoDNS \n"
            "This client uses the PHP endpoint to alter the DNS records",
        )
        self.domain_id = None
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def __del__(self):
        self.driver.close()

    def _wait_start_page(self):
        self.driver.get(
            "https://kis.hosteurope.de/administration/domainservices/index.php" +
            "?menu=2&mode=autodns&submode=edit&domain={0}".format(self.domain)
        )
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "hostadd")))

    def _format_domain_name(self, name):
        if name.endswith(self.domain):
            name = name.replace(".{0}".format(self.domain), "")
        if name.endswith('{0}.'.format(self.domain)):
            name = name.replace(".{0}.".format(self.domain), "")

        return name

    def _find_identifier(self, rtype, name, content):
        self._wait_start_page()
        identifier = None
        name = self._format_domain_name(name)
        records = self._list_records(rtype, name, content)
        if len(records) == 1:
            identifier = records[0]['id']

        return identifier

    def _find_hidden_input(self, identifier):
        try:
            hidden = self.driver.find_element_by_xpath("//input[@name='hostid' and @value='{}']".format(identifier))
            return hidden
        except NoSuchElementException as e:
            LOGGER.error(
                "Record id %s not found", identifier
            )
            LOGGER.error(e)
            return None

    def _update_record_by_id(self, identifier, rtype, content):
        hidden = self._find_hidden_input(identifier)
        if not hidden:
            return False

        row_text = hidden.find_element_by_xpath("./..")
        row = row_text.find_elements_by_tag_name("td")

        type_field = row[1]
        record_field = row[2]

        type_select = Select(type_field.find_element_by_tag_name('select'))
        record_pointer = record_field.find_element_by_name("pointer")
        pointer_update = record_field.find_element_by_xpath("./input[@name='submit' and @value='Update']")

        type_select.select_by_visible_text(rtype)
        record_pointer.clear()
        record_pointer.send_keys(content)
        pointer_update.click()

        if self._get_lexicon_option('ttl'):
            self._set_record_ttl_by_id(identifier, str(self._get_lexicon_option('ttl')))

        return True

    def _delete_record_by_id(self, identifier=None):
        if identifier:
            hidden = self._find_hidden_input(identifier)
            if not hidden:
                return False

            row_text = hidden.find_element_by_xpath("./..")
            row = row_text.find_elements_by_tag_name("td")
            record_field = row[2]

            pointer_delete = record_field.find_element_by_xpath("./input[@name='submit' and @value='Löschen']")
            pointer_delete.click()

            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="contentcol"]/div/table[1]/tbody/tr[2]/td/ul/li/a[1]')
            ))

            delete_btn = self.driver.find_element_by_xpath(
                '//*[@id="contentcol"]/div/table[1]/tbody/tr[2]/td/ul/li/a[1]')
            delete_btn.click()
            return True
        else:
            return False

    def _set_record_ttl_by_id(self, identifier, ttl):
        self.driver.get(
            "https://kis.hosteurope.de/administration/domainservices/index.php" +
            "?menu=2&mode=autodns&submode=edit&domain={0}".format(self.domain)
        )
        WebDriverWait(self.driver, 5).until(EC.title_contains("Nameserver"))

        hidden = self.driver.find_element_by_xpath("//input[@name='hostid' and @value='{}']".format(identifier))
        row_text = hidden.find_element_by_xpath("./..")
        row = row_text.find_elements_by_tag_name("td")

        ttl_field = row[3]
        ttl_submit = ttl_field.find_element_by_name('submit')

        ttl_select = Select(ttl_field.find_element_by_tag_name('select'))
        ttl_select.select_by_value(ttl)
        ttl_submit.click()

    def _authenticate(self):
        self.driver.get(
            "https://kis.hosteurope.de/administration/domainservices/index.php" +
            "?menu=2&mode=autodns&submode=edit&domain={0}".format(self.domain)
        )
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        self.driver.find_element_by_id("1").send_keys(self._get_provider_option('auth_username'))
        self.driver.find_element_by_id("2").send_keys(self._get_provider_option('auth_password'))
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        WebDriverWait(self.driver, 5).until(EC.title_contains("HE-KIS"))

        self.domain_id = self.domain
        return self.driver.find_element_by_name("hostadd") is not None

    def _create_record(self, rtype, name, content):
        if rtype not in ["A", "AAAA", "CNAME", "TXT"]:
            raise Exception("Unsupported type: %s".format(rtype))

        name = self._format_domain_name(name)

        is_record_set = False
        for record in self._list_records(rtype, name, None):
            if record['type'] == rtype and self._format_domain_name(record['name']) == name:
                is_record_set = True
                if record['content'] == content:
                    return True

        hostadd = self.driver.find_element_by_name("hostadd")
        hostadd.send_keys(name)

        row_text = hostadd.find_element_by_xpath("./../../..")
        row = row_text.find_elements_by_tag_name("td")

        type_field = row[1]
        type_select = Select(type_field.find_element_by_tag_name('select'))
        type_select.select_by_visible_text(rtype)

        content_field = row[2].find_element_by_name("pointeradd")
        content_field.clear()
        content_field.send_keys(content)

        submit_btn = row[2].find_element_by_name("submit")
        submit_btn.click()

        if is_record_set:
            allow_set_button = self.driver.find_element_by_xpath(
                '//*[@id="contentcol"]/div/table[1]/tbody/tr[2]/td/ul/li/a[1]'
            )
            if allow_set_button:
                allow_set_button.click()

        # Set TTL
        if self._get_lexicon_option('ttl'):
            identifier = self._find_identifier(rtype, name, content)
            self._set_record_ttl_by_id(identifier, str(self._get_lexicon_option('ttl')))

        return True

    def _list_records(self, rtype=None, name=None, content=None):
        self._wait_start_page()
        records = []

        # Find record table
        hostadd = self.driver.find_element_by_name("hostadd")
        table = hostadd.find_element_by_xpath("./../../../../..")

        for row_text in table.find_elements_by_tag_name("tr")[1:-1]:
            row = row_text.find_elements_by_tag_name("td")

            type_field = row[1]
            record_field = row[2]
            ttl_field = row[3]

            record_pointer = record_field.find_element_by_name("pointer")
            record_hostid = row_text.find_element_by_name("hostid")

            type_select = Select(type_field.find_element_by_tag_name('select'))
            ttl_select = Select(ttl_field.find_element_by_tag_name('select'))

            record_id = record_hostid.get_property("value")
            record_type = type_select.first_selected_option.text
            record_name = row[0].text.split('\n')[0]
            record_content = record_pointer.get_property("value")
            record_ttl = ttl_select.first_selected_option.get_attribute('value')
            processed_record = {
                'id': record_id,
                'type': record_type,
                'name': record_name,
                'content': record_content,
                'ttl': record_ttl,
            }
            records.append(processed_record)

        LOGGER.debug('list_records(all): %s', records)

        name = self._format_domain_name(name)
        if rtype:
            records = [record for record in records if record['type'] == rtype]
        if name:
            records = [record for record in records if record['name'] == '{0}.{1}'.format(name, self.domain)]
        if content:
            records = [record for record in records if record['content'].lower() == content.lower()]

        LOGGER.debug('list_records(filtered): %s', records)
        return records

    def _update_record(self, identifier, rtype=None, name=None, content=None):
        if rtype not in ["A", "AAAA", "CNAME", "TXT"]:
            raise Exception("Unsupported type: %s".format(rtype))

        if not identifier:
            identifier = self._find_identifier(rtype, name, None)

        return self._update_record_by_id(identifier, rtype, content)

    def _delete_record(self, identifier=None, rtype=None, name=None, content=None):
        if not identifier:
            identifier = self._find_identifier(rtype, name, content)

        return self._delete_record_by_id(identifier)

    def _request(self, action='GET', url='/', data=None, query_params=None):
        pass
