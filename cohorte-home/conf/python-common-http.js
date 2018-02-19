/**
 * Common Java configuration: HTTP / JSON bundles
 */
{
	/*
	 * Pelix HTTP bundles
	 */
	"bundles" : [
	/* Pelix HTTP Bundle */
	{
		"name" : "pelix.http.basic"
	} ],

	/*
	 * , { "name" : "cohorte.shell.signals" }, { "name" : "cohorte.signals.http" }, {
	 * "name" : "cohorte.signals.directory" }, { "name" :
	 * "cohorte.signals.directory_updater" }
	 */

	/*
	 * Components
	 */
	"composition" : [ 
		{
			"$include":{
				"path":["python-common-httpv6.js#composition[*]"],
				"condition":"'${run:transport-http}' == None and '${run:transport-http.http-ipv}' == '6'"
			}
		},{
			"$include":{
				"path":["python-common-httpv4.js#composition[*]"],
				"condition":"'${run:transport-http}' != None and '${run:transport-http.http-ipv}' == '4'"
			}
		}
	]

/*
 * Signals components { "factory" : "cohorte-signals-receiver-http-factory",
 * "name" : "cohorte-signals-receiver-http" }, { "factory" :
 * "cohorte-signals-sender-http-factory", "name" : "cohorte-signals-sender-http" }, {
 * "factory" : "cohorte-signals-directory-factory", "name" :
 * "cohorte-signals-directory" }, { "factory" :
 * "cohorte-signals-directory-updater-factory", "name" :
 * "cohorte-signals-directory-updater" }
 */
}
