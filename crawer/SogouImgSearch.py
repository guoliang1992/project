import urllib2, re

testurl = 'http://tse2.mm.bing.net/th?id=OIP.Mf41f73bd0526f320e7b2e82ead9a0d69o0'



# search sogou img by img url
def getSogouImgByImgUrlImp(url):
	ImgDataBegin = 'var imgTempData = {'
	SogouImgUrl = 'http://pic.sogou.com/ris?query=URL&flag=1'

	searchUrl = SogouImgUrl.replace('URL', url)
	content = urllib2.urlopen(searchUrl).read()

	begin = content.find(ImgDataBegin)
	if begin == -1:
		return
	content = content[begin + len(ImgDataBegin) - 1:]
	#print content

	imgRegex = '"pic_url":"([^"]+)"'
	imgList = re.findall(imgRegex, content)
	

	print 'url\t%s' % url
	for img in imgList:
		print img


def getSogouImgByImgUrl(urlFile):
	for line in open(urlFile):
		line = line.strip('\n')
		segs = line.split('\t')
		if len(segs) != 2:
			query, url = segs
		getSogouImgByImgUrlImp(url)


SogouUrlFile = ''
getSogouImgByImgUrl(SogouUrlFile)







