/**
 * Common Java configuration: HTTP / JSON bundles
 */
{

	/*
	 * Components
	 */
	"composition" : [ 
		{
			"factory" : "pelix.http.service.basic.factory",
	        "name" : "pelix-http-service",
	        "properties" : {
	            // Use the IPv4 stack
	            "pelix.http.address" : "0.0.0.0",
            	// Use the first port available
				"pelix.http.port" : 0
	        }
		}
	]

}
