/**
 * Configuration for Herald XMPP transport
 */
{
	/*
	 * Herald XMPP transport bundles
	 */
	"bundles" : [ {
		"name" : "herald.transports.xmpp.directory"
	}, {
		"name" : "herald.transports.xmpp.transport"
	} ],

	// Import the common component configuration
	"$merge" : [
		"all-xmpp.js"
	],
	
	"composition":[
		{
	        "name" : "herald-xmpp-transport",
	        "properties" : {{
	            "xmpp.server" : "${run:transport-xmpp.xmpp-server}",
	            "xmpp.port" : "${run:transport-xmpp.xmpp-port}",
	            "xmpp.user.jid" : "${run:transport-xmpp.xmpp-user-jid}",
	            "xmpp.user.password" : "${run:transport-xmpp.xmpp-user-password}"
	        }}
	    }
	]
}
