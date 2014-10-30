/**
 * Common component configuration for the XMPP transport
 */
{
	/*
	 * XMPP core component
	 */
	"composition" : [ {
		"factory" : "herald-xmpp-transport-factory",
		"name" : "herald-xmpp-transport",
		"properties" : {
			"xmpp.server" : "localhost",
			"xmpp.port" : "5222",
			"xmpp.monitor.jid" : "bot@phenomtwo3000",
			"xmpp.room.jid" : "cohorte@conference.phenomtwo3000",
			// FIXME: Should be given by the forker
			"xmpp.monitor.key" : "42"
		}
	} ]
}
