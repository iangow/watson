# Description

## `run_watson.py`

Queries `watson_input` table in the PostgreSQL database for text associated with executives, 
submits this text, one row at a time, to the IBM Watson Personality Insights
service to obtain the each subject's psychological profile, and uploads
the results to the `watson_output_raw` in the database.

The table `watson_output_raw` has two columns: `hash`, the SHA hash of the original text, and `profile`, the profile returned by IBM Watson Personality Insights service. 

Only rows not found in the existing table are processed. This is done for two reasons:
- First, each Watson API call takes about 1 second to complete, so
  a large number of calls can take a long time to finish. Caching
  allows to skip those calls that were made previously.
- Second, the service charges for each API call.

## `create_watson_output.py`

Converts the raw output found in `watson_output_raw` into a "wide" format and adds fields from `watson_input`.
Results are stored in `watson_output_alt`. 

## personalityinsights.py

This file contains the main class to submit text to the IBM Watson
Personality Insights service. 
For this to work, you will need to install the Python bindings for this service, found [here](https://github.com/watson-developer-cloud/personality-insights-python).

An example of usage:
``` Python
from personalityinsights import PersonalityInsights as PI
pi = PI()
profile = pi.get_profile(text)
```

# Authentication with the database and the IBM Watson Bluemix Cloud

Two files containing personal identification information for
the services being used by the program should be present:

- `config.py` contains information identifying the user's account
  previously set up on the IBM Watson website.

  Further details can be found in the file `config.example.py`,
  which should be used as a template.

- `.pgpass` should be present in the home directory of the user
  running the program on a *nix OS (including MacOS). Please
  consult appropriate documentation regarding the correct placement
  of this file on a Windows machine.

  Alternatively, the environment variables `PGUSER` and `PGPASSWORD`
  should be set.
