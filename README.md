# RatpAPI Python Wrapper

## Overview
RatpAPI is a Python wrapper for interacting with the RATP (Régie Autonome des Transports Parisiens) API. This library provides easy access to real-time traffic information, line-specific traffic details, and affluence data for journeys on the RATP network in Paris.

## Features
- Fetch global traffic information on the RATP network.
- Retrieve traffic information for specific lines.
- Get affluence data for journeys on particular lines.

## Installation
To use RatpAPI in your project, you can clone this repository:
```bash
git clone [repository URL]
```

## Usage

### Setting Up
First, import the `RatpAPI` class and initialize it with your API key:

```python
from ratp_api.main import RatpAPI

api = RatpAPI(api_key="your_api_key_here")
```

### Fetching Global Traffic Information
To get global traffic data:
```python
global_traffic = api.get_global_traffic()
print(global_traffic)
```

### Fetching Line-Specific Traffic
To get traffic information for a specific line:
```python
line_traffic = api.get_line_traffic("line_id_here")
print(line_traffic)
```

### Fetching Affluence for Journeys
To get affluence data for a specific journey on a line:
```python
start_coords = (longitude, latitude)  # Start location coordinates
end_coords = (longitude, latitude)    # End location coordinates
line_id = "line_id_here"

affluence_data = api.get_affluence(start=start_coords, end=end_coords, line_id=line_id)
print(affluence_data)
```

### Fetching Affluence for All Lines
To get affluence data for all lines:
```python
all_lines_affluence = api.get_all_lines_affluence()
print(all_lines_affluence)
```

## Contributing
Contributions to the RatpAPI project are welcome! Please refer to the contributing guidelines for more information.

## License
This project is licensed under [appropriate license] - see the LICENSE file for details.

---

Replace `[repository URL]` with the actual URL of your GitHub repository and `[appropriate license]` with the license type you've chosen for your project. This README provides a basic introduction to your project, including how to install and use the library. Feel free to modify and expand it according to the needs of your project.