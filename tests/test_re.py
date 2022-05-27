import re
cve_regex = re.compile(r"cve-\d{4}-\d{4,7}", re.I)

test_text="test\nFix CaVE-2021-3566 and CaVE-2021-38291"
if cve_regex.search(test_text):
    print('匹配')
else:
    print('不匹配')
