{
	"composition" : [ {
		/*
		 * Override the HTTP service configuration
		 */		
		"name" : "pelix-http-service",
		"factory" : "pelix.http.service.basic.factory",
		"properties" : {
			"pelix.http.port" : 8092
		}
	} ]
}