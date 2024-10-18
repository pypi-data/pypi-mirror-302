import argparse
import datetime
import logging
import os
import random
import re
import sys
import threading
import time

import pytz
import requests
import yaml

# Set up logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Create a logger
logger = logging.getLogger(__name__)


######### Custom exceptions ##########


class NotPlayerToProcess(Exception):
    def __init__(self):
        logger.info(
            "Did not find any players. "
            "Please check Read.me how to pass user login and password"
        )


class NotFoundCSRFToken(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without server returning CSRF token in html, "
            f"check server response: {yaml.dump(message)}"
        )


class UnauthorizedLogin(Exception):

    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from login request, "
            f"check user credentials and server response: {yaml.dump(message)}"
        )


class NotFoundActivity(Exception):

    def __init__(self, search, output):
        logger.error(
            f"Unable to find activity using {search}. Server response: {yaml.dump(output)}"
        )


class NotOpenEnrollment(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from enrollment call, "
            f"check server response: {message}"
        )


class UserNotSelected(Exception):
    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from user selection call, "
            f"check server response: {yaml.dump(message)}"
        )


class ActivityNotAddedToCart(Exception):

    def __init__(self, message):
        logger.error(
            f"Unable to proceed without getting 200 response from add activity to cart, "
            f"check if all inputs to add activity are correct. Server response: {yaml.dump(message)}"
        )


class CheckoutFailed(Exception):
    def __init__(self, message):
        logger.error(
            f"Getting non-success response code for final submission, "
            f"please debug server response: {message}"
        )


class CamdenClient:
    """
    Class to act as a client for the
    Camden Volleyball registration.
    """

    # use them only for the initial call to initiate
    # user session and get csrf token
    NOT_AUTHENTICATED_HEADERS = {
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "host": "anc.apm.activecommunities.com",
        "referer": "https://anc.apm.activecommunities.com/",
        "upgrade-insecure-requests": "1",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-user": "1",
        "Sec-Fetch-Site": "same-site",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept": "*/*",
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    }

    # use them for making requests to api endpoints (REST)
    API_HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8",
        "connection": "keep-alive",
        "content-type": "application/json;charset=utf-8",
        "host": "anc.apm.activecommunities.com",
        "origin": "https://anc.apm.activecommunities.com",
        "page_info": '{"page_number":1,"total_records_per_page":20}',
        "referer": 'https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?onlineSiteId=0&locale=en-US&from_original_cui=true&override_partial_error=False&custom_amount=False&params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl',
        "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": " ".join(
            [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "AppleWebKit/537.36 (KHTML, like Gecko)",
                "Chrome/129.0.0.0 Safari/537.36",
            ]
        ),
        "x-csrf-token": None,  # make sure to update after getting token
        "x-requested-with": "XMLHttpRequest",
    }

    def __init__(
        self,
        login,
        password,
        force_mode=False,
        keywords="Drop In Volleyball",
        activity_id=None,
    ):
        self.user_login = login
        self.user_password = password
        self.force_mode = force_mode
        self.keywords = keywords
        self.activity_id = activity_id

        # placeholders
        self.session = requests.session()
        self.session.cookies = requests.cookies.RequestsCookieJar()
        self.csrf_token = None
        self.enrolled = False
        self.test_mode = False

        self.start_time = time.perf_counter()

    def authorize(self):
        """
        Method to authorize client by:

        1. getting CSRF token
        2. posting login and updating session cookies

        :return:
        """

        self._get_csrf_token()

        self._update_cookies_after_login()

    def register(self):

        self.test_mode = False

        if not self.force_mode:
            self.wait_for_enrollment_to_open()

        self.authorize()

        self.start_time = time.perf_counter()

        self._enroll()

        self._select_user()

        if not self.enrolled:
            self._add_to_cart()
            self._checkout()
            self._get_cart_receipt()

            logger.info(
                f"User {self.user_login} registered in "
                f"{round(time.perf_counter() - self.start_time, 2)} seconds"
            )

        return self.enrolled

    def test(self):

        self.test_mode = True

        self.authorize()

        self._enroll()

        self._select_user()

        self._add_to_cart()

        logger.info(
            f"User {self.user_login} test PASSED. Registration time: "
            f"{round(time.perf_counter() - self.start_time, 2)} seconds"
        )

        return True

    ############# Private methods ################

    def _get_csrf_token(self):
        """ """
        logger.info(f"User {self.user_login} requested csrf token")

        res = self.session.get(
            (
                "https://anc.apm.activecommunities.com/sanjoseparksandrec/signin?"
                "onlineSiteId=0&locale=en-US&"
                "from_original_cui=true&"
                "override_partial_error=False&"
                "custom_amount=False&"
                "params=aHR0cHM6Ly9hcG0uYWN0aXZlY29tbXVuaXRpZXMuY29tL3Nhbmpvc2VwYXJrc2FuZHJlYy9BY3RpdmVOZXRfSG9tZT9GaWxlTmFtZT1hY2NvdW50b3B0aW9ucy5zZGkmZnJvbUxvZ2luUGFnZT10cnVl"
            ),
            headers=CamdenClient.NOT_AUTHENTICATED_HEADERS,
        )

        # Regex pattern to extract the CSRF token
        csrf_token_pattern = r'window\.__csrfToken = "([a-f0-9-]+)"'

        # Applying the regex pattern to extract the CSRF token
        csrf_token_match = re.search(csrf_token_pattern, res.text)

        # Check if the regex match was successful
        if csrf_token_match:
            csrf_token = csrf_token_match.group(1)
            logger.info(f"User {self.user_login} CSRF Token: {csrf_token}")
            self.csrf_token = csrf_token

        else:
            raise NotFoundCSRFToken(res.text)

        self.session.cookies.update(res.cookies)

    def _update_cookies_after_login(self):

        if not self.user_login and not self.user_password:
            raise RuntimeError("Unable to proceed without credentials")

        logger.info(f"User {self.user_login} simulate login and update session cookies")

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "login_name": self.user_login,
            "password": self.user_password,
            "recaptcha_response": "",
            "signin_source_app": "0",
            "locale": "en-US",
            "ak_properties": None,
        }

        res = self.session.post(
            "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/user/signin?locale=en-US",
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.customer_id = res.json()["body"]["result"]["customer"]["customer_id"]
            self.session.cookies.update(res.cookies)
            logger.info(f"User {self.user_login} got customerId: {self.customer_id}")
        else:
            raise UnauthorizedLogin(res.text)

    def _get_activity_id(self):

        if self.activity_id:
            logger.info(
                f"User {self.user_login} using known activity id: {self.activity_id}"
            )
            return self.activity_id

        if self.test_mode:
            keywords = ""
            date_before = ""
            date_after = ""
        else:
            keywords = self.keywords
            current_date = datetime.date.today()
            date_before = (current_date + datetime.timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
            date_after = current_date.strftime("%Y-%m-%d")

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_search_pattern": {
                "skills": [],
                "time_after_str": "",
                "days_of_week": "0010100",
                "activity_select_param": 2,
                "center_ids": [],
                "time_before_str": "",
                "open_spots": None,
                "activity_id": None,
                "activity_category_ids": [],
                "date_before": date_before,
                "min_age": 18,
                "date_after": date_after,
                "activity_type_ids": [],
                "site_ids": [],
                "for_map": False,
                "geographic_area_ids": [],
                "season_ids": [],
                "activity_department_ids": [],
                "activity_other_category_ids": [],
                "child_season_ids": [],
                "activity_keyword": keywords,
                "instructor_ids": [],
                "max_age": "45",
                "custom_price_from": "0",
                "custom_price_to": "0",
            },
            "activity_transfer_pattern": {},
        }

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec"
            "/rest/activities/list?locale=en-US"
        )

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        all_activities = []

        if res.status_code == 200:
            all_activities = res.json()["body"]["activity_items"]

        if not all_activities:
            raise NotFoundActivity(keywords, res.text)

        logger.info(
            f"User {self.user_login} search returned "
            f"{len(all_activities)} activities using keywords <{keywords}> "
            f"and date interval: <{date_after} - {date_before}>"
        )

        # For testing purposes will select random activity
        if self.test_mode:
            activity = random.choice(all_activities)
            logger.info(
                f"User {self.user_login} selected random activity: <{activity.get('desc')[:22]}>"
            )
        else:
            # filter out paid activities
            all_activities = [
                activity
                for activity in all_activities
                if activity["fee"]["label"] == "Free"
            ]

            activity = all_activities[0]
            logger.info(
                f"User {self.user_login} selected first activity "
                f"{activity['id']}: {activity.get('desc')[:22]}"
            )

        self.activity_id = activity["id"]

        return self.activity_id

    def _enroll(self):
        """
        Requires valid activity id

        Possible cases:

        - not open for enrollment

        """

        activity_id = self._get_activity_id()

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "activity_id": activity_id,
            "transfer_out_transaction_id": 0,
            "reg_type": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} was enrolled after {time.perf_counter() - self.start_time}"
            )
            self.session.cookies.update(res.cookies)
        else:
            server_response = res.json().get("headers", {}).get("response_message")
            raise NotOpenEnrollment(f"{self.user_login}: {server_response}")

    def _select_user(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "customer_id": self.customer_id,
            "overrides": [],
            "is_edit_transfer": False,
            "transfer_out_transaction_id": 0,
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/participant?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            self.session.cookies.update(res.cookies)
            logger.info(
                f"User {self.user_login} was selected "
                f"after {time.perf_counter() - self.start_time}"
            )
        else:
            if "Already Enrolled" in res.text:
                # that is considered successful execution, we can exit
                logger.info(f"User {self.user_login} already enrolled")
                self.enrolled = True
                self._get_cart_receipt()
            else:
                raise UserNotSelected(res.text)

    def _add_to_cart(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "reno": 1,
            "participant_note": "",
            "question_answers": [
                {
                    "reno": 1,
                    "question_id": 2,
                    "customquestion_index": "1",
                    "parent_question_id": 0,
                    "user_entry_answer": "None",
                    "answer_id": [],
                },
                {
                    "reno": 1,
                    "question_id": 157,
                    "customquestion_index": "2",
                    "parent_question_id": 0,
                    "user_entry_answer": "",
                    "answer_id": [1031],
                },
            ],
            "donation_param": [],
            "waivers": [],
            "pickup_customers": [],
            "participant_usa_hockey_number": {
                "usah_code": "",
                "position_id": 1,
            },
            "token": "",
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/activity/enrollment/addtocart?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if not res.status_code == 200:
            raise ActivityNotAddedToCart(res.text)
        else:
            self.enrolled = True
            logger.info(
                f"User {self.user_login} added to cart "
                f"after {time.perf_counter() - self.start_time}"
            )

    def _checkout(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        payload = {
            "waiver_initials_online_text": True,
            "online_waiver_initials": "",
            "initials": [],
        }

        url = "https://anc.apm.activecommunities.com/sanjoseparksandrec/rest/checkout?locale=en-US"

        res = self.session.post(
            url,
            json=payload,
            cookies=self.session.cookies,
            headers=headers,
        )

        if res.status_code == 200:
            logger.info(
                f"User {self.user_login} checked out after {time.perf_counter() - self.start_time}"
            )
        else:
            raise CheckoutFailed(res.text)

    ############ Helpers #################

    def wait_for_enrollment_to_open(self):
        # Define the Pacific Standard Timezone
        pst = pytz.timezone('America/Los_Angeles')

        # Get the current time in PST
        now = datetime.datetime.now(pst)

        # Print the current timestamp
        logger.info(
            f"User {self.user_login} current timestamp in PST: {now.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Define the target time to wait until (~ 19:30:01 PST)
        target_time = now.replace(hour=19, minute=30, second=0)

        # Check if the current time is already past the target time
        if now >= target_time:
            logger.info(
                f"User {self.user_login} current time is already past 19:30:00 PST."
            )
        else:
            # Calculate the time difference to wait
            time_diff = (target_time - now).total_seconds()
            logger.info(f"User {self.user_login} waiting until 19:30:00 PST...")

            # Wait until the target time is reached
            time.sleep(time_diff)
            logger.info(f"User {self.user_login} wait is over, starting...")

    ############ Not required for registration, just FYI #########

    def _get_cart_receipt(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        # 1729101431907
        ui_random = int(time.time() * 1000)

        url = (
            f"https://anc.apm.activecommunities.com/sanjoseparksandrec"
            f"/rest/cartReceipt?locale=en-US&ui_random={ui_random}"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

        receipt_number = res.json().get("body", {}).get("receipt_number")
        logger.info(f"User {self.user_login} confirmation receipt {receipt_number}")

    def _get_user_account(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec/myaccount?"
            "locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_enrollment_details(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            f"https://anc.apm.activecommunities.com/sanjoseparksandrec"
            f"/rest/activity/detail/{self.activity_id}?locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)

    def _get_login_check(self):

        headers = CamdenClient.API_HEADERS | {"x-csrf-token": self.csrf_token}

        url = (
            "https://anc.apm.activecommunities.com/sanjoseparksandrec"
            "/rest/common/logincheck?locale=en-US"
        )

        res = self.session.get(
            url,
            cookies=self.session.cookies,
            headers=headers,
        )

        self.session.cookies.update(res.cookies)


def process_single_player(
    login,
    password,
    test_mode,
    force_mode,
    activity_id=None,
):

    logger.info(f"Processing in test mode: {test_mode}. ")
    if test_mode:

        attempts = 5

        camden_client = CamdenClient(
            login=login,
            password=password,
        )

        while attempts > 0:
            try:
                if camden_client.test():
                    attempts = -1
            except Exception as e:
                logger.info(e)
            time.sleep(1)
            attempts -= 1

        if attempts == 0:
            logger.info(f"Test for user {login} FAILED")
    else:

        attempts = 10
        camden_client = CamdenClient(
            login=login,
            password=password,
            force_mode=force_mode,
            activity_id=activity_id,
        )

        while attempts > 0:
            try:
                if camden_client.register():
                    attempts = 0
            except Exception as e:
                logger.info(e)

            time.sleep(1)
            attempts -= 1


def main():

    parser = argparse.ArgumentParser(
        description="Automate user actions to register player for the next Camden volleyball activity",
        epilog=(
            """
            EXAMPLES:

            The following command will execute script with all default values,
            use config file to navigate to registration url, use players credentials to login
            and trigger registration:
                % python camden_api_client.py

            The following command will use custom configuration file:
                % python camden_api_client.py --players-from-file my-file.yml

            The following command will use player credentials from cli:
                % python camden_api_client.py --player <login>:<password>

            The following command will test setup:
                % python camden_api_client.py --player <login>:<password> --test


            """
        ),
    )

    parser.add_argument(
        "--test",
        "-t",
        help="If true, will simulate registration without final checkout. Also using random activity to register",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--force",
        "-f",
        help="If true, will not wait till 19:30 PST to start registration",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--players-from-file",
        help="If specified, will override default master.yml file",
        action="store",
        default="../master.yml",
    )

    parser.add_argument(
        "--player",
        help="If specified, will use player login and password in the format <login>:<password>",
        action="store",
    )

    parser.add_argument(
        "--activity",
        help="If specified, will use this activity to register. Recommended to pass for performance optimization",
        action="store",
    )

    args, unknown = parser.parse_known_args()

    if args.player:
        players = [
            {
                "login": args.player.split(":")[0],
                "password": args.player.split(":")[1],
            }
        ]

    else:
        # will read from the same folder as current file
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the file you want to read
        file_to_read = os.path.join(current_dir, args.players_from_file)

        with open(file_to_read) as f:
            players = yaml.safe_load(f.read()).get("players")
            players = [player for player in players if player.get("enroll", False)]

    if not players:
        raise NotPlayerToProcess()

    test_mode = args.test
    force_mode = args.force
    activity_id = args.activity

    for player in players:

        t = threading.Thread(
            target=process_single_player,
            args=(
                player.get("login"),
                player.get("password"),
                test_mode,
                force_mode,
                activity_id,
            ),
        )

        t.start()


if __name__ == "__main__":
    main()
