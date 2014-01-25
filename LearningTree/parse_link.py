import re
def parse_for_links(text):
	return re.sub('\[.*?\]', link_replace, text)



def link_replace(matchobj):
	link = matchobj.group()[1:-1]
	print link
	# TODO: check if link is in list
	# TODO: if not, add a new link
	# replace the link with a local URL
	return "<a href='{0}'>{0}</a>".format(link)
	
