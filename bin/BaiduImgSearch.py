import urllib2, re

class FetchImgTools:
	def __init__(self):
		self.connter = 0
		self.baidu_img_url = 'http://image.baidu.com/n/pc_search?queryImageUrl=URL&fm=result_camera&uptype=paste&drag=1'
		self.img_data_begin = "'sameList': Array"
		self.img_data_end = 'sameSizeNum'

		self.imgList = list()
		self.visitedImgList = list()

		self.line_separator = '\n'
		self.filed_separator = '\t'

	def getBaiduImgByImgUrl(self, urlFile):
		for line in open(urlFile):
			line = line.strip(self.line_separator)
			segs = line.split(self.filed_separator)
			if len(segs) != 2:
				query, url = segs
			getBaiduImgByImgUrlImp(url)


	# search baidu img by img url
	def getBaiduImgByImgUrlImp(self, url):
		
		searchUrl = self.baidu_img_url.replace('URL', url)
		content = urllib2.urlopen(searchUrl).read()
		
		begin = content.find(self.img_data_begin)
		if begin == -1:
			return

		end = content.find(self.img_data_end)
		if end == -1:
			return
	
		content = content[begin:end]

		imgRegex = '"objURL":"(.*?)"'
		imgList = re.findall(imgRegex, content)
	
		for img in imgList:
			if img not in self.visitedImgList:
				if img not in self.imgList:
					self.imgList.append(img)
					self.counter += 1

				self.visitedImgList.append()

				
	def downloadImg(self, saveImgPath):
		createPath(saveImgPath)

		outputStream = open(saveImgPath, 'wb')
		for imgUrl in self.imgList:
			imgData = urllib2.urlopen(imgUrl).read()

			if data == '':
				return
			outputStream.write(imgData)

		outputStream.close()
	
	def createPath(self, path):
		if not os.path.exists(path)
			os.makedirs(path)

testurl = 'http://imgsrc.baidu.com/baike/pic/item/377adab44aed2e735cc9850b8401a18b87d6faf1.jpg'

getBaiduImgByImgUrlImp(testurl)
#BaiduUrlFile = ''
#getBaiduImgByImgUrl(BaiduUrlFile)
