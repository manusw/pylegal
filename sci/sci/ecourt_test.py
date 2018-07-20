import requests

cookies = {
    'PHPSESSID': '85k041a83hlh8mfcklua26m500',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://services.ecourts.gov.in/ecourtindia_v5.1/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('state_code', '1'),
    ('dist_code', '19'),
    ('court_code', '4'),
    ('caseStatusSearchType', 'CNRNumber'),
    ('cino', 'MHAU010000092015'),
    ('national_court_code', 'MHAU01'),
)

response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_filing_case_history.php', headers=headers, params=params, cookies=cookies,verify=False,timeout=(10, 130))

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_filing_case_history.php?state_code=1^&dist_code=19^&court_code=4^&caseStatusSearchType=CNRNumber^&cino=MHAU010000092015^&national_court_code=MHAU01', headers=headers, cookies=cookies)

#params = (
#    ('case_no', '201901000022015'),
#    ('state_cd', '1'),
#    ('dist_cd', '19'),
#    ('court_code', '4'),
#    ('appFlag', ''),
#    ('national_court_code', 'MHAU01'),
#    ('court_complex_code', ''),
#    ('cino', 'MHAU010000092015'),
#)

#response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_civil_case_history.php', headers=headers, params=params, cookies=cookies,verify=False,timeout=(10, 130))
print(response.content)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_civil_case_history.php?case_no=201901000022015^&state_cd=1^&dist_cd=19^&court_code=4^&appFlag=^&national_court_code=MHAU01^&court_complex_code=^&cino=MHAU010000092015', headers=headers, cookies=cookies)