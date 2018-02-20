{
	
	/*
	 * bundles
	 */
	"bundles" : [ 
		{
			"$include":{
				"path":["python-http.js#bundles[*]"],
				"condition": "'http' in '${run:transport}'" 
			}
		},
		{
			"$include":{
				"path":["python-xmpp.js#bundles[*]"],
				"condition": "'xmpp' in '${run:transport}'" 
			}
		} 
	], 
	
	/*
	 * Components
	 */
	"composition" : [ 
		{
			"$include":{
				"path":["python-http.js#composition[*]"],
				"condition": "'http' in '${run:transport}'" 
			}
		},
		{
			"$include":{
				"path":["python-xmpp.js#composition[*]"],
				"condition": "'xmpp' in '${run:transport}'" 
			}
		} 
	], 
	/*
	 * Avoid discovering local peers using multicast
	 * when Local Discovery is used 
	 * (starting from 1.2.0 version of Cohorte)
	 */
	"properties" : {		
		"$include":{
			"path":["python-http.js#properties"],
			"condition": "'http' in '${run:transport}'" 
		},
		"$include":{
			"path":["python-xmpp.js#properties"],
			"condition": "'xmpp' in '${run:transport}'" 
		}
	}
} 
