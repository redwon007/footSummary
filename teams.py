import json
import datetime
import pytz
import os, glob
from pathlib import Path

def queryDefinition():
  utc=pytz.UTC

  premier_league_file = 'calendars/Premier_League.json'
  ligue_1_file = 'calendars/Ligue_1.json'

  path = 'calendars'

  queries = []

  for filename in glob.glob(os.path.join(path, '*.json')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode

      league = Path(filename).stem
      print(league)
      filename = json.load(f)

      
      
      queries_League = []
      for i, match in enumerate(filename):
        
        date_match = datetime.datetime.strptime(match['DateUtc'][:-1], '%Y-%m-%d %H:%M:%S')
        date_match = utc.localize(date_match)

        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_week_before = date_now + datetime.timedelta(days=-7)
          
        if date_week_before <= date_match <= date_now :

          query = 'resume ' + match['HomeTeam'] + ' ' + match['AwayTeam']
        
          queries_League.append(query)
          
      dict = {}
      dict[league] = queries_League

      queries.append(dict)
  return(queries)

print(queryDefinition())






