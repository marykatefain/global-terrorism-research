from whoosh.query import *
def search(request):
    qs_list = Statement.objects.all()
    print "HELLO WORLD"
    query = request.GET.get("search")
    '''
    query_auth = request.GET.get("auth_search")
    if query_auth:
	qs_list = Statement.objects.all()
	qs_list = qs_list.filter(Q(author__person_name__icontains=query_auth))
    '''
    if query:
       if "->" in query:
          print "Keyword context operator detected" 
       qs_list = Statement.objects.all()
       #complex lookups for various fields
       qs_list = qs_list.filter(
          Q(title__icontains=query) | Q(statement_id__icontains=query) |
          Q(author__person_name__icontains=query) | Q(released_by__org_name__icontains=query)
       ).distinct() #these are all the items that can be searched by basic char analysis at the moment.
       
       set_of_keywords = Keyword.objects.all()
       #Search results are put into the context dictionary
       context = {
          "results": qs_list, "keywords": set_of_keywords,
       }
       print "QS_LIST: "
       print qs_list
       #print "CONTEXT: "
       #print context
       #for x in qs_list:
           #print "URL: "
           #print x.get_absolute_url()
    #if 'search' in request.POST:
        #print "HELLO WORLD FROM CONDITIONAL!"
        #search = request.POST['search']
        #print "SEARCH: ", search
       return render(request, 'search/search.html', context)

def get_search_by(GET_list, search_dictionary):
   """check to see if the items we want to search in the GET request have values submitted"""
   return [search_type for search_type in search_dictionary if GET_list[search_type]]

def search(request):
    from whoosh.index import open_dir
    from whoosh.qparser import MultifieldParser, QueryParser
    from whoosh.qparser.dateparse import DateParserPlugin 

    print request.GET
    #<QueryDict: {u'auth_search': [u''], u'csrfmiddlewaretoken': [u'yg2KtF6FxRV4w7bEq0BhMTHDNvLyerd5RXx7xsdpwwJ7DwjVt7q6na2iI2GdowTx'], u'search': [u'Iraq'], u'key_search': [u''], u'title_search': [u'']}>
    #(statement_id:Iraq OR title:iraq OR author:iraq OR keyword:Iraq OR context:Iraq)
    # might need to check if empty, not if in

    # This defines what we can possibly search for
    # keys should match the way it is in the get request
    # values should match what it is in the whoosh index
    search_dictionary = {"auth_search" : "author", "key_search" : "keyword", "title_search" : "title"}   
    
    search_by = get_search_by(request.GET, search_dictionary)
    ix = open_dir("index")  # open up our index
    # now open up our searcher
    with ix.searcher() as searcher:
        query = False # we use this to check if there is a preexisting query to add to
        for search_type in search_by:
	    search_terms  = request.GET[search_type]      # term(s) we are going to be searching e.g. [Iraq]
	    schema_field = search_dictionary[search_type] # field we are searching on e.g. keyword
            parser = QueryParser(schema_field, ix.schema)
	    query_for_field = False
	    for search_term in search_terms:
		if query_for_field:
		    query_for_field = query_for_field | parser.parse(search_term)
		else:
		    query_for_field = parser.parse(search_term)
	    if query:
		query = query & query_for_field 
	    else:
	        query = query_for_field

	    print query
	    results  = searcher.search(query, limit=None)
            result_list = []
            statement_list = []
            for r in results:
               print r
	       statement_list.append(Statement.objects.get(statement_id = r["statement_id"]))
               result_list.append(r)

            keywords = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_obj() for result in result_list] #get all statements.keyword_in_contexts
            context = {'results' : results, 'keywords' : keywords, 'contexts' : ["cat"], 'key_con' : {"a key" : "a con"} , 'search' : "my search" }
	    return render(request, 'search/search.html', context)

    """ This is where I'm leaving off. I'm back on the quest of how to make an empty query, which might just not be possible?
        Regardless, just keep progressing down this guy I think. I'm at the part where I go through individual keys"""
            
    if 'title_search' in request.GET:
	title_parser = QueryParser("title", ix.schema)
    if 'search' in request.GET:
	    search = request.GET['search']

	    with ix.searcher() as searcher:
		# https://whoosh.readthedocs.io/en/latest/parsing.html
		mparser = MultifieldParser(["statement_id", "title", "author", "keyword", "context"], ix.schema)
		mparser.add_plugin(DateParserPlugin())
		dateparse = QueryParser("issue_date", schema= ix.schema)
		dateparse.add_plugin(DateParserPlugin()) # http://whoosh.readthedocs.io/en/latest/dates.html
	 	filter_request = False
                if 'Filter' in request.GET:
		   if "filter_by_date" in request.GET:
			filter_date = True
		   else:
			filter_date = False
                   # because to the best of my knowledge I can't make an empty query
		   # I need to do this little hack
	 	   filter_request = True
		   no_con_yet     = True
		   no_key_yet     = True
		   no_key_con_yet = True
		   
		   ex_no_con_yet     = True
		   ex_no_key_yet     = True
		   ex_no_key_con_yet = True
"""
def check_key_and_filter(key):


                   for key in request.GET:
		      print request.GET[key]
		      print "working with", key
		      if request.GET[key]=='con_ON':
			if no_con_yet:
			  con_query = Term("context", key)
			  no_con_yet = False
			else:
			  con_query = con_query | Term("context", key)
		      elif request.GET[key]=='key_ON':
			if no_key_yet:
			  key_query = Term("keyword", key)
			  no_key_yet = False
			else:
			  key_query = key_query | Term("keyword", key)
		      elif request.GET[key]=='key_con_ON':
			# I am breaking these on underscores,
			# so there will be problems if a key/con has underscores
			keyword, context = key.split("_")

			key_con = Term("keyword", keyword)
			key_con = key_con & Term("context", context)

			if no_key_con_yet:
			  key_con_query = key_con
			  no_key_con_yet = False
			else:
			  key_con_query = key_con_query | key_con
		      elif filter_date and  key == "date_low":
			
			# we need to convert to python date time, then convert it back to a string
			# this seems stupid, and it kind of is
			# but I think it is neccessary to get the tools we are using to
			# work together
			
			# there is also some junk I don't want at the end, string looks like:
			# Mon Jan 01 1990 00:00:00 GMT-0500 (EST)
			# We split on the line:
			# Mon Jan 01 1990 00:00:00| GMT-0500 (EST)
 			
			#lowDate = request.POST[key][:24]
			lowDate = datetime.strptime(request.GET[key][:24], "%a %b %d %Y %X")
		      elif filter_date and key == "date_high":
			highDate = datetime.strptime(request.GET[key][:24], "%a %b %d %Y %X")
		      elif request.GET[key]=='con_OFF':
		        # now we do the excluding, which is very similar
			if ex_no_con_yet:
			  ex_con_query = Term("context", key)
			  ex_no_con_yet = False
			else:
			  ex_con_query = ex_con_query | Term("context", key)
		      elif request.GET[key]=='key_OFF':
			if ex_no_key_yet:
			  ex_key_query = Term("keyword", key)
			  ex_no_key_yet = False
			else:
			  ex_key_query = ex_key_query | Term("keyword", key)
		      elif request.GET[key]=='key_con_OFF':
			# I am breaking these on underscores,
			# so there will be problems if a key/con has underscores
			keyword, context = key.split("_")

			ex_key_con = Term("keyword", keyword)
			ex_key_con = key_con & Term("context", context)

			if ex_no_key_con_yet:
			  ex_key_con_query = ex_key_con
			  ex_no_key_con_yet = False
			else:
			  ex_key_con_query = ex_key_con_query | ex_key_con

		query = mparser.parse(search)
		#allow = query.Term("context", "Chastisement")
		if filter_request and not no_con_yet:
		  query = query & con_query 
	          print con_query
		if filter_request and not no_key_yet:
		  query = query & key_query
		  print key_query
		if filter_request and not no_key_con_yet:
		  query = query & key_con_query
		
		if filter_request and filter_date:
		  for i in range(1, int(request.GET['slider_count']) + 1):
			lowDate = datetime.strptime(request.GET["date_low"+str(i)][:24], "%a %b %d %Y %X")
			highDate = datetime.strptime(request.GET["date_high"+str(i)][:24], "%a %b %d %Y %X")
		  	if i==1:
			  date_query = DateRange("issue_date", lowDate, highDate)
			else:
			  date_query = date_query | DateRange("issue_date", lowDate, highDate)
		  query = query & date_query
		if filter_request and not ex_no_con_yet:
		  query = query - ex_con_query 
		if filter_request and not ex_no_key_yet:
		  query = query - ex_key_query
		if filter_request and not ex_no_key_con_yet:
		  query = query - ex_key_con_query
		print query
		results = searcher.search(query, limit=None)

                # if we returned no results, we need to just return here
		if len(results) == 0:
		  return render(request,  'search/search.html')

                print results, "RESULTS"
                print len(results)
                result_list = []
		statement_list = []
                for r in results:
                   print r
		   statement_list.append(Statement.objects.get(statement_id = r["statement_id"]))
                   result_list.append(r)
		print statement_list
                print "all done"
		#result_list = [results[i] for i in range(len(results))] # convert from query type to normal list
                print "Success!"
		keywords = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_obj() for result in result_list] #get all statements.keyword_in_contexts
		#contexts = [Statement.objects.get(statement_id = result["statement_id"]).get_contexts() for result in result_list]
                #Does the above line need to be here anymore if we have removed the idea of contexts as an entity unique from keywords?
		key_con  = [Statement.objects.get(statement_id = result["statement_id"]).get_keywords_contexts_obj() for result in result_list] #So does this conflict with 
                #the line that performs gett_keywords? we're getting all keywordincontexts twice.
                print "KEYWORDS (only the main_keyword objects of the KeywordInContext's associated with this statement)"
		print keywords
                print "list of tuple of keyword context pairs"
                print key_con
                
		#unioned_keywords = keywords[0]
		#for query_set in keywords:
		   #unioned_keywords = (unioned_keywords | query_set)
		#unioned_keywords.distinct()
		#print key_con
                
		# making a dictionary where the keywords are keys and all contexts that go with those keywords, across the dataset, are in there
		key_con_dict = {}
		'''
		for statement in key_con:
		   for keyword in statement:
		      KIC = keyword
		      keyword = keyword.main_keyword
		      print "keyword obj:",keyword,"keyword:", keyword.word 
		      print type(keyword.word)
		      if keyword.word in key_con_dict:
			 key_con_dict[keyword.word] = key_con_dict[keyword.word].append( statement[KIC])
		      else:
			 key_con_dict[keyword.word] = [statement[KIC]]
		for keyword in key_con_dict:
		   key_con_dict[keyword] = list(key_con_dict[keyword].distinct())
		print key_con_dict
		#if filter_request: # might not actually need this
                #The below line should be deprecated because contexts and key_con_dict are no longer necessary. At all.
		'''
		print result_list
		context = {'results' : statement_list, 'keywords' : keywords, 'contexts' : ["cat"], 'key_con' : key_con_dict, 'search' : search }
	    return render(request, 'search/search.html', context)
    else:
       print request.GET
       return render(request, 'search/search.html')
"""
class qrequest:
  def __init__(self,get):
    self.GET = get

get = {u'auth_search': ['Dylan','Emery'], u'csrfmiddlewaretoken': [u'yg2KtF6FxRV4w7bEq0BhMTHDNvLyerd5RXx7xsdpwwJ7DwjVt7q6na2iI2GdowTx'], u'search': [u'Iraq'], u'key_search': [], u'title_search': ['Iraq','Egypt']}
myrequest = qrequest(get)
search(myrequest)