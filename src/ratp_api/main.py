import json
import logging
import uuid

import requests
from affluence.line_mappings import line_end_points


class RatpAPI:
    """
    A class to interact with the RATP API.
    """

    GLOBAL_TRAFFIC_URL = "https://bff.bonjour-ratp.fr/lines/situations?"
    LINE_TRAFFIC_URL = "https://bff.bonjour-ratp.fr/lines/{}/situations?"
    AFFLUENCE_URL = "https://bff.bonjour-ratp.fr/itineraries/query?"

    def __init__(self, api_key: str = "e2rDkJzd2c1dPaFh7e0pJ9H7NjeqTQHg6ql31LmZ"):
        """
        Initialize the RatpAPI class with the given API key.

        :param api_key: A string representing the API key for the RATP API.
        """
        self.x_api_key = api_key
        self.x_client_guid = str(uuid.uuid4())
        self.session = self.get_session()

    def get_session(self) -> requests.Session:
        """
        Create and return a new session with pre-configured headers.

        :return: A requests.Session object for making API calls.
        """
        session = requests.Session()
        headers = {
            "x-api-key": self.x_api_key,
            "x-client-guid": self.x_client_guid,
            "x-client-platform": "bonjour_ios",
            "x-client-version": "latest",
            "Accept": "application/vnd.rss.bff.itinerary.v8+json",
            "Content-Type": "application/vnd.rss.bff.itineraries-query.v8+json",
            "User-Agent": "RATP/10.35.1 (com.ratp.ratp; build:231; iOS 17.0.3)",
        }
        session.headers.update(headers)
        return session

    def make_request(self, method, url, **kwargs) -> dict:
        """
        Make an HTTP request using the initialized session.

        :param method: HTTP method (e.g., 'GET', 'POST').
        :param url: URL to which the request is sent.
        :param kwargs: Additional arguments to pass to the request method.
        :return: The JSON response from the API if the request is successful; an empty dictionary otherwise.
        """
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.info(f"Error: {e}")
            return {}

    def get_global_traffic(self) -> dict:
        """
        Retrieve global traffic information.

        :return: A dictionary representing the global traffic situation.
        """
        return self.make_request("GET", self.GLOBAL_TRAFFIC_URL)

    def get_line_traffic(self, line_id: str) -> dict:
        """
        Retrieve traffic information for a specific line.

        :param line_id: The ID of the line for which traffic information is requested.
        :return: A dictionary representing the traffic situation for the specified line.
        """
        url = self.LINE_TRAFFIC_URL.format(line_id)
        return self.make_request("GET", url)

    def get_affluence(self, start, end, line_id):
        """
        Retrieve affluence information for a specific journey on a given line.

        :param start: A tuple (longitude, latitude) representing the start location.
        :param end: A tuple (longitude, latitude) representing the end location.
        :param line_id: The ID of the line for which affluence information is requested.
        :return: A dictionary containing affluence information, or an empty dict if not available.
        """
        line_id_adjusted = line_id.replace("bis", "B")
        payload = self._create_affluence_payload(start, end)

        response = self.make_request("POST", self.AFFLUENCE_URL, data=payload)
        return self._parse_affluence_response(response, line_id_adjusted)

    def _create_affluence_payload(self, start, end):
        """
        Create the payload for the affluence request.

        :param start: The start coordinates (longitude, latitude).
        :param end: The end coordinates (longitude, latitude).
        :return: A JSON string for the payload.
        """
        start_longitude, start_latitude = start
        end_longitude, end_latitude = end
        return json.dumps(
            {
                "destination": {"longitude": end_longitude, "latitude": end_latitude},
                "transportModes": ["ALL"],
                "origin": {"longitude": start_longitude, "latitude": start_latitude},
                "withReducedMobility": False,
            }
        )

    def _parse_affluence_response(self, response, line_id) -> dict:
        """
        Parse the response from the affluence request.

        :param response: The response received from the affluence request.
        :param line_id: The line ID used in the affluence request.
        :return: A dictionary containing parsed affluence information, or an empty dict if not available.
        """
        for itinerary in response.get("itineraries", []):
            for segment in itinerary["segments"]:
                if (
                    segment["transportMode"] == "METRO"
                    and segment["groupOfLines"]["name"] == line_id
                ):
                    comfort = segment.get("comfort", {})
                    if "level" in comfort:
                        comfort["lineId"] = segment["line"]["id"]
                        return comfort
        return {}

    def get_all_lines_affluence(self):
        """
        Retrieve affluence information for all lines.

        :return: A list of dictionaries containing affluence information for each line.
        """
        affluences = []
        for line_id, endpoints in line_end_points.items():
            try:
                comfort = self.get_affluence(
                    start=endpoints["start"]["coords"],
                    end=endpoints["end"]["coords"],
                    line_id=line_id,
                )
                if "level" in comfort:
                    comfort["lineDisplayCode"] = line_id
                    affluences.append(comfort)
                else:
                    logging.info(f"No affluence level found for {line_id}")
            except Exception as e:
                logging.info(f"Error fetching affluence for {line_id}: {e}")

        return affluences


if __name__ == "__main__":
    api = RatpAPI(api_key="e2rDkJzd2c1dPaFh7e0pJ9H7NjeqTQHg6ql31LmZ")
    logging.info(api.get_all_lines_affluence())
