/**
 * Boot configuration for Java isolates
 */
{
	/* Common Python stack */
	"$merge" : [ "boot-common.js"],

	/*
	 * Bundles
	 */
	"bundles" : [ {
		"name" : "cohorte.java.java"
	} ],

	/*
	 * Components
	 */
	"composition" : [
	/* Configuration of common components */
	{
		"name" : "pelix-remote-shell",
		"properties" : {
			// Random shell port
			"pelix.shell.port" : "${run:node.shell-port}"
		}
	},

	/* JVM runner */
	{
		"factory" : "cohorte-java-runner-factory",
		"name" : "cohorte-java-runner"
	} ]
}
