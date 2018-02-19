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
				// Use the IPv6 stack by default
				"pelix.http.address" : "::",
	
				// Use the first port available
				"pelix.http.port" : 0
			}
		}
	]

}
