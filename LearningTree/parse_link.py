import re
def parse_for_links(text):
	def link_replace(matchobj):
		link = matchobj.group(1)
		text = matchobj.group(2) if len(matchobj.groups) == 3 else matchobj.group(1)

		try:
			linkObject = Link(url=link)
			linkObject.save()
		except:
			pass 
		return "<a href='{0}'>{1}</a>".format(link, text)

	return re.sub('\[(.*?)\]\((.*?)\)', link_replace, text).sub('\[(.*?)\]', link_replace, text)


