# SI 201 HW4 (Library Checkout System)
# Your name: Nathaniel Mitelman, Brandon Wivietsky, Coby Kalimian
# Your student id: Brandon: 3847 2237, Nathaniel: 1492 6180, Coby: 4950 5044
# Your email: Mitelman@umich.edu, Cobykali@umich.edu, Bwivie@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): ChatGPT
# If you worked with generative AI also add a statement for how you used it.
# Used ChatGPT to help understand the HTML structure of the Airbnb pages and to get guidance on which BeautifulSoup methods to use for extracting specific elements.
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
# Yes, it aligned with out goals.
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
#import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(html_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    results = []
    title_divs = soup.find_all("div", {"data-testid": "listing-card-title"})
    for div in title_divs:
        listing_title = div.get_text().strip()
        listing_id = div.get("id", "").replace("title_", "")
        results.append((listing_title, listing_id))

    return results
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    policy_number = ""
    for li in soup.find_all("li", class_="f19phm7j"):
        text = li.get_text()
        if "Policy" in text or "License" in text:
            span = li.find("span", class_="ll4r2nl")
            if span:
                raw = span.get_text().strip().replace("\ufeff", "")
            else:
                raw = text.replace("Policy number:", "").replace("License number:", "").strip()

            lower = raw.lower()
            if "pending" in lower:
                policy_number = "Pending"
            elif "exempt" in lower:
                policy_number = "Exempt"
            else:
                policy_number = raw
            break

    superhost_tag = soup.find(string=lambda t: t and t.strip() == "Superhost")
    host_type = "Superhost" if superhost_tag else "regular"

    host_name = ""
    for h2 in soup.find_all("h2"):
        txt = h2.get_text().replace("\xa0", " ")
        match = re.search(r"[Hh]osted by\s+(.+)", txt)
        if match:
            host_name = match.group(1).strip()
            break

    room_type = "Entire Room"
    subtitle = ""
    for h2 in soup.find_all("h2"):
        txt = h2.get_text().replace("\xa0", " ")
        if "hosted by" in txt.lower():
            subtitle = txt
            break

    if "Private" in subtitle:
        room_type = "Private Room"
    elif "Shared" in subtitle:
        room_type = "Shared Room"
    else:
        kh_div = soup.find("div", class_="_kh3xmo")
        if kh_div:
            kh_text = kh_div.get_text()
            if "Private" in kh_text:
                room_type = "Private Room"
            elif "Shared" in kh_text:
                room_type = "Shared Room"
            else:
                room_type = "Entire Room"

    location_rating = 0.0
    loc_div = soup.find("div", class_="_y1ba89", string="Location")
    if loc_div:
        parent = loc_div.parent
        full_text = parent.get_text().replace("Location", "").strip()
        rating_match = re.search(r"(\d+\.?\d*)", full_text)
        if rating_match:
            location_rating = float(rating_match.group(1))

    return {
        listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating,
        }
    }
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listings = load_listing_results(html_path)
    database = []

    for listing_title, listing_id in listings:
        details = get_listing_details(listing_id)
        info = details[listing_id]
        entry = (
            listing_title,
            listing_id,
            info["policy_number"],
            info["host_type"],
            info["host_name"],
            info["room_type"],
            info["location_rating"],
        )
        database.append(entry)

    return database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Listing Title",
                "Listing ID",
                "Policy Number",
                "Host Type",
                "Host Name",
                "Room Type",
                "Location Rating",
            ]
        )
        for row in sorted_data:
            writer.writerow(row)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    totals = {}
    counts = {}

    for entry in data:
        room_type = entry[5]
        location_rating = entry[6]

        if location_rating == 0.0:
            continue

        if room_type not in totals:
            totals[room_type] = 0.0
            counts[room_type] = 0

        totals[room_type] += location_rating
        counts[room_type] += 1

    result = {}
    for room_type in totals:
        result[room_type] = round(totals[room_type] / counts[room_type], 1)

    return result
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid = []

    pattern1 = r"^20\d{2}-00\d{4}STR$"
    pattern2 = r"^STR-000\d{4}$"

    for entry in data:
        listing_id = entry[1]
        policy_number = entry[2]

        if policy_number in ("Pending", "Exempt"):
            continue

        if not re.match(pattern1, policy_number) and not re.match(
            pattern2, policy_number
        ):
            invalid.append(listing_id)

    return invalid
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    for result in soup.find_all("h3", class_="gs_rt"):
        title_text = result.get_text().strip()
        titles.append(title_text)

    return titles
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        self.assertEqual(len(self.listings), 18)
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]
        details_list = [get_listing_details(lid) for lid in html_list]
        self.assertEqual(details_list[0]["467507"]["policy_number"], "STR-0005349")
        self.assertEqual(details_list[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(details_list[2]["1944564"]["room_type"], "Entire Room")
        self.assertEqual(details_list[2]["1944564"]["location_rating"], 4.9)


    def test_create_listing_database(self):
        for entry in self.detailed_data:
            self.assertEqual(len(entry), 7)

        self.assertEqual(
            self.detailed_data[-1],
            (
                "Guest suite in Mission District",
                "467507",
                "STR-0005349",
                "Superhost",
                "Jennifer",
                "Entire Room",
                4.8,
            ),
        )

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")
        output_csv(self.detailed_data, out_path)

        with open(out_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.assertEqual(
            rows[1],
            [
                "Guesthouse in San Francisco",
                "49591060",
                "STR-0000253",
                "Superhost",
                "Ingrid",
                "Entire Room",
                "5.0",
            ],
        )
        
        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        averages = avg_location_rating_by_room_type(self.detailed_data)
        self.assertEqual(averages["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
