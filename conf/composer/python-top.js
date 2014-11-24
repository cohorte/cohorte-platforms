/**
 * Start configuration for a Top Composer (Python version)
 */
{
	/*
	 * Composer bundles
	 */
	"bundles" : [
	/* Parser */
	/*{
		"name" : "cohorte.composer.parser"
	},
	*/
	/* Top Composer components */
	{
		"name" : "cohorte.composer.top.composer"
	}, {
		"name" : "cohorte.composer.top.distributor"
	}, {
		"name" : "cohorte.composer.top.status"
	}, {
		"name" : "cohorte.composer.top.commander"
	}, {
		"name" : "cohorte.composer.top.store_handler"
	},

	/* Distributor criteria */
	{
		"name" : "cohorte.composer.top.criteria.distance.configuration"
	},

	/* Shell commands */
	{
		"name" : "cohorte.shell.composer_top"
	},

	/* web admin */
	{
		"name" : "webadmin.webadmin"
	
	} ] ,

	"composition" : [ {
		"factory" : "cohorte-composer-top-factory",
		"name" : "cohorte-composer-top",
		"properties" : {
			"autostart" : "True"
		}
	} ]
/* All components of the Composer are automatically instantiated */
}
