import sys

if len(sys.argv) == 2:

	import re
	
	OneDriveUrl = sys.argv[1]

	O = re.fullmatch('https://1drv.ms/f/s!\S+', OneDriveUrl)
	if O:
		import requests

		from urllib.parse import parse_qs, urlparse

		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}

		s = requests.Session()
		r = s.get(OneDriveUrl, allow_redirects = False, headers = headers)

		up = urlparse(r.headers['Location'])

		pqs = parse_qs(up.query)

		authkey = pqs['authkey'][0]

		resid = pqs['resid'][0]

		cid = resid.split('!')[0]

		headers['Accept'] = 'application/json'
		headers['AppId'] = '1141147648'
    
		#~ print(resid)
		#~ print(cid)
		#~ print(authkey)

		r = requests.get(f'https://skyapi.onedrive.live.com/API/2/GetItems?sb=0&ps=100&sd=0&gb=0,1,2&d=1&m=de-DE&iabch=1&pi=5&path=1&lct=1&rset=odweb&v=0.3291468777304306&si=0&authKey={authkey}&id={resid}&cid={cid}',
			allow_redirects = False, headers = headers)


		robj = r.json()

		item1 = robj['items'][0]

		type = item1['iconType']

		if type == 'NonEmptyDocumentFolder' or type == 'NonEmptyAlbum':
			#~ print('YAY this is the correct folder type for the operation')
			
			count = item1['folder']['documentCount']
			
			children = item1['folder']['children']
			
			for child in children:
				download = child['urls']['download']
				print(download)
		else:
			print(f'Type is unkown: {type}')
	else:
		print()
		print('ERROR: URL must be of the type https://1drv.ms/f/s!%FOLDERSHORTLINKTOKEN%')
else:
	print('No URL provided, URL must be of the type https://1drv.ms/f/s!%FOLDERSHORTLINKTOKEN%')

