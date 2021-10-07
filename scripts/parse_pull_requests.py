import re
import os
import requests
from datetime import datetime

with open('api_baseline.txt', 'r') as fid:
    diffversion = fid.readlines()[0].strip()

#raw_prs = requests.get('https://open-bamboo.nrao.edu/browse/CASA-RN/latestSuccessful/artifact/PAR2/pullrequests/pullrequests.txt').text.split('\n')[1:]
#raw_dates = requests.get('https://open-bamboo.nrao.edu/browse/CASA-RN/latestSuccessful/artifact/PAR2/dates/dates.txt').text.split('\n')
#raw_builds = requests.get('https://open-bamboo.nrao.edu/browse/CASA-RN/latestSuccessful/artifact/PAR2/builds/builds.txt').text.split('\n')

with open('changelog/pullrequests.txt', 'r') as fid:
    raw_prs = fid.read().split('\n')[1:]

with open('changelog/dates.txt', 'r') as fid:
    raw_dates = fid.read().split('\n')

with open('changelog/builds.txt', 'r') as fid:
    raw_builds = fid.read().split('\n')

difflog = ''
for ii, raw_line in enumerate(raw_prs):
    if len(raw_line.strip()) == 0: continue
    prdict = eval(raw_line.replace('true', 'True').replace('false', 'False').replace('null','None'))
    date = datetime.strptime(raw_dates[ii][4:-6], '%b %d %H:%M:%S %Y').strftime('%m/%d/%y')
    build = re.findall('.*?tag: (\d\.\d\.\d\.\d+).*', raw_builds[ii], flags=re.DOTALL)
    build = ' <sup>['+build[0]+']</sup> ' if len(build) > 0 else ' '
    id = prdict['key']
    components = [cc['name'] for cc in prdict['fields']['components']]
    if (len(components) == 1) and (components[0] == 'Verification'): continue
    note = prdict['fields']['customfield_10500']
    if note is not None: note = note.replace('\n','\n   ')
    difflog += '   <li><p><i>%s</i> <b>%s</b>%s- %s</p></li>\n\n' % (date, id, build, note)

# write out log of tool API diffs
with open('changelog.rst', 'w') as fid:
    fid.write('Change Log\n==========\n\nSummary of differences from ' + diffversion + '\n\nPull Requests\n+++++++++++++\n\n')
    fid.write('.. raw:: html\n\n   <ul>\n' + difflog + '   </ul>\n\n|\n')
