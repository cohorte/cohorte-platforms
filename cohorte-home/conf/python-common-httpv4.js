/**
 * Common Java configuration: HTTP / JSON bundles
 */
{

	/*
	 * Components
	 */
	"composition" : [ 
		{
	        "name" : "pelix-http-service",
	        "properties" : {
	            // Use the IPv4 stack
	            "pelix.http.address" : "0.0.0.0"
	        }
		}
	]

}
