# RatpAPI Python Wrapper

## Overview
RatpAPI is a Python wrapper for interacting with the RATP (Régie Autonome des Transports Parisiens) API. This library provides easy access to real-time traffic information, line-specific traffic details, and affluence data for journeys on the RATP network in Paris.

## Features
- Fetch global traffic information on the RATP network.
- Retrieve traffic information for specific lines using the `LineID` enum for easy reference.
- Get affluence data for journeys on particular lines.
- Utilizes Pydantic models for data validation and parsing.


## Installation
To use RatpAPI in your project, you can install it via pip:
```bash
pip install ratp-api-python
```

## Usage
a
### Setting Up
First, import the `RatpAPI` class and initialize it with your API key:

```python
from ratp_api.main import RatpAPI

api = RatpAPI()
```

### Using the LineID Enum
The `LineID` enum provides a convenient way to reference specific lines by their IDs:
```python
from ratp_api.enums import LineID

# Example: Using LineID for RER A
line_id = LineID.RER_A
```

### Fetching Global Traffic Information
To get global traffic data:
```python
global_traffic = api.get_global_traffic()
print(global_traffic)
```

### Fetching Line-Specific Traffic
To get traffic information for a specific line using the `LineID` enum:
```python
line_data = api.get_line_traffic(line_id=LineID.METRO_14)
for situation in line_data.situations:
    print(situation)
# Output:
# isActive=True isPlanned=True criticity='HIGH' messages=["Jusqu'au 04/02, le week-end, trafic interrompu sur l'ensemble de la ligne en raison de travaux. Bus de remplacement. Plus d'informations sur la page dédiée."]
# isActive=False isPlanned=True criticity='HIGH' messages=["Du 01/02 au 08/02, du lundi au jeudi à partir de 22h, trafic interrompu sur l'ensemble de la ligne en raison de travaux. Bus de remplacement. Plus d'informations sur la page dédiée."]
# isActive=False isPlanned=True criticity='HIGH' messages=["Jusqu'au 31/01, du lundi au jeudi à partir de 22h, trafic interrompu sur l'ensemble de la ligne en raison de travaux. Bus de remplacement. Plus d'informations sur la page dédiée."]

```

### Fetching Affluence for Journeys
To get affluence data for a specific journey on a line:
```python
line_id = LineID.RER_A          # Using LineID enum

affluence_data = api.get_line_affluence(line_id=line_id)
print(affluence_data)
```

### Fetching Affluence for All Lines
To get affluence data for all lines:
```python
all_lines_affluence = api.get_all_lines_affluence()
print(all_lines_affluence)
```

## Contributing
Contributions to the RatpAPI project are welcomed!

## License
This project is licensed under the MIT License.

---