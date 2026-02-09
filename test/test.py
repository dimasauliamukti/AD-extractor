from config import JSON,ASSETS
from table import table
import json

#Open Database
with open(JSON,"r") as f:
    database=json.load(f)

#data_test
data_test={"evaluate":[ {"aircraft_models":"MD-11",
          "msn":"48123",
          "modification_applied":[]},
          {"aircraft_models":"DC-10-30F",
          "msn":"47890",
          "modification_applied":[] },
          {"aircraft_models":"Boeing 737-800",
          "msn":"30123",
          "modification_applied":[] },
          {"aircraft_models":"A320-214",
          "msn":"5234",
          "modification_applied":[] },
          {"aircraft_models":"A320-232",
          "msn":"6789",
          "modification_applied":["mod 24591 (production)"] },
          {"aircraft_models":"A320-214",
          "msn":"7456",
          "modification_applied":["SB A320-57-1089 Rev 04"] },
          {"aircraft_models":"A321-111",
          "msn":"8123",
          "modification_applied":[] },
          {"aircraft_models":"A321-112",
          "msn":"364",
          "modification_applied":["mod 24977 (production)"] },
          {"aircraft_models":"A319-100",
          "msn":"9234",
          "modification_applied":[]},
          {"aircraft_models":"MD-10-10F",
          "msn":"46234",
          "modification_applied":[]},
          {"aircraft_models":"MD-11F",
          "msn":"48400",
          "modification_applied":[]},
          {"aircraft_models":"A320-214",
          "msn":"4500",
          "modification_applied":["mod 24591 (production)"]},
          {"aircraft_models":"A320-214",
          "msn":"4500",
          "modification_applied":[]},
          ]}

def qqww(rule,test):
    aircraft=test.get("aircraft_models")
    mods=test.get("modification_applied",[])
   
    excluded=rule["Applicability"].get("excluded_if_modifications",[])
    required=rule["Applicability"].get("required_modifications",[])
    ad_number=rule["AD_number"]
    
    if aircraft not in rule["Applicability"]["aircraft_models"]:
        return "Not Applicable",ad_number
    
    if any(req in mod for mod in mods for req in required):
        return "Not Affected",ad_number
    
    if any(exc in mod for mod in mods for exc in excluded):
        return "Not Affected",ad_number
    
    return "Affected" ,ad_number

data_table = []
for tests in data_test["evaluate"]:
    row = {}
    mods = tests.get("modification_applied", [])

    row["Aircraft Model"] = tests["aircraft_models"]
    row["MSN"] = tests["msn"]

    mod = tests.get("modification_applied", [])
    row["Modification Applied"] = ", ".join(mod) if mod else "None"

    for data in database["ruled_based"]:
        status, number = qqww(data, tests)
        row[number] = status  

    data_table.append(row)

table(data_table,ASSETS)
