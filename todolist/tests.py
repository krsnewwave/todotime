import datetime
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from django.utils import dateformat
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from todolist.models import Note


class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_admin_site(self):
        # open browser
        self.browser.get(self.live_server_url + '/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

    def test_admin_creates_users(self):
        # find "Users"
        self.browser.get(self.live_server_url + '/admin/')
        username = self.browser.find_element_by_name('username')
        username.send_keys('dylanv')

        password = self.browser.find_element_by_name('password')
        password.send_keys('dylanv')
        password.send_keys(Keys.RETURN)

        # go to users place
        users_link = self.browser.find_elements_by_link_text('Users')
        self.assertIsNotNone(users_link)
        self.assertTrue(len(users_link) > 0)

    def test_login(self):
        """Register new user, login, success"""
        # please view fixtures for the available users
        self.browser.get(self.live_server_url + '/todolist/login/')
        username = self.browser.find_element_by_name('username')
        username.send_keys('dylanv')

        password = self.browser.find_element_by_name('password')
        password.send_keys('dylanv')
        password.send_keys(Keys.RETURN)
        # get current date
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('New Note', body.text)
        expected = dateformat.format(datetime.datetime.now(), "jS F Y H:i")
        self.assertIn(expected, body.text)

    def test_logout(self):
        """Log out user"""
        # login user
        self.test_login()
        # logout
        logout_link = self.browser.find_element_by_link_text('Logout')
        # press link
        logout_link.click()
        # find login again in screen
        button = self.browser.find_elements_by_name('Log in')
        self.assertIsNotNone(button)

    def test_new_note(self):
        """Add new note, current year, day +7, current month"""
        self.test_login()
        self.browser.get(self.live_server_url + '/todolist/new/')

        # text
        expected_note_text = 'test new note'
        submit = self.browser.find_element_by_name('text')
        submit.send_keys('%s' % expected_note_text)

        # date today
        curr_date = datetime.date.today()
        # due date dropdown
        # current month
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_month']/option[text()='%s']" % curr_date.strftime("%B")).click()
        # curr day + 7
        day_7 = curr_date + datetime.timedelta(days=7)
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_day']/option[text()='%s']" % day_7.strftime("%d").lstrip('0')).click()
        # current year
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_year']/option[text()='%s']" % curr_date.strftime("%Y")).click()

        # click update
        submit.send_keys(Keys.RETURN)

        # find note in home page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(expected_note_text, body.text)

    def test_edit_note_text(self):
        """Edit note details"""
        self.test_login()

        # create the note
        expected_note_text = 'test new note'
        self.test_new_note()

        edit_text = 'test edit note'
        text = self.browser.find_element_by_link_text(expected_note_text)
        text.click()
        text = self.browser.find_element_by_id('id_text')
        text.clear()
        text.send_keys(edit_text)
        text.send_keys(Keys.RETURN)

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(edit_text, body.text)

    def test_delete_note(self):
        """Delete note"""
        self.test_login()

        # create the note
        expected_note_text = 'test new note'
        self.test_new_note()

        # only one note to delete
        self.browser.find_element_by_link_text('Delete').click()

        # find the note
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn(expected_note_text, body.text)

    def test_tick_cancel(self):
        """Tick cancel"""
        self.test_login()

        # create the note
        self.test_new_note()

        # only one note to cancel
        self.browser.find_element_by_link_text('Mark as Cancelled').click()

        # should have cancel in the body text
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Cancelled', body.text)

    def test_tick_due(self):
        """Tick due"""
        self.test_login()
        self.browser.get(self.live_server_url + '/todolist/new/')

        # create the note
        self.test_new_note()

        # only one note to cancel
        self.browser.find_element_by_link_text('Mark as Cancelled').click()

        # should have cancel in the body text
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Cancelled', body.text)

    def test_transfer_to_next_day(self):
        """Add a new note in the past, when displayed, it must be the next day"""
        self.test_login()
        self.browser.find_element_by_link_text('New Note').click()
        # text
        expected_note_text = 'test new note'
        submit = self.browser.find_element_by_name('text')
        submit.send_keys('%s' % expected_note_text)

        # date today
        curr_date = datetime.date.today()
        # due date dropdown
        # month
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_month']/option[text()='%s']" % curr_date.strftime("%B")).click()
        # curr day -1
        day_minus_1 = curr_date + datetime.timedelta(days=-1)
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_day']/option[text()='%s']" % day_minus_1.strftime("%d").lstrip('0')).click()
        # year
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_year']/option[text()='%s']" % curr_date.strftime("%Y")).click()

        # click update
        submit.send_keys(Keys.RETURN)

        # expect that the date due is current date + 1
        expected_date = curr_date + datetime.timedelta(days=1)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(expected_date.strftime('%b. %d, %Y'), body.text)

    def test_transfer_due(self):
        """Adds a new note, transfer the date, display in main index"""
        self.test_login()
        self.browser.get(self.live_server_url + '/todolist/new/')

        # create the note, curr month, curr year, curr day + 7
        self.test_new_note()

        # click that note
        expected_note_text = 'test new note'
        edit_text = 'test edit note'
        text = self.browser.find_element_by_link_text(expected_note_text)
        text.click()
        text = self.browser.find_element_by_id('id_text')
        text.clear()
        text.send_keys(edit_text)

        # edit that note to day to curr day + 3
        curr_date = datetime.date.today()
        # due date dropdown
        # current month
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_month']/option[text()='%s']" % curr_date.strftime("%B")).click()
        # curr day + 3 instead
        day_3 = curr_date + datetime.timedelta(days=7)
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_day']/option[text()='%s']" % day_3.strftime("%d").lstrip('0')).click()
        # current year
        self.browser.find_element_by_xpath(
            "//select[@id='id_date_due_year']/option[text()='%s']" % curr_date.strftime("%Y")).click()

        # click update
        text.send_keys(Keys.RETURN)

        # go to main index, find that dates have been updated
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(day_3.strftime('%b. %d, %Y'), body.text)

    def test_7_days_purge(self):
        """Adds a new note in the past, should not appear in main index"""
        note = Note()
        expected_note_text = 'old note'
        note.text = '%s' % expected_note_text
        note.is_cancelled = False
        note.is_done = False
        note.date_due = datetime.date.today()
        note.date_posted = datetime.date.today() - datetime.timedelta(days=8)
        note.user_id = 1
        note.save()

        self.test_login()

        # should not find anything
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn(expected_note_text, body.text)


