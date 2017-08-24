{
	"name": "hello-app",
	"root": {
		"name": "hello-app-composition",
		"components": [
			{
				"name"    : "HC",
				"factory" : "hello_components_factory",
				"isolate" : "web"
			}, {
				"name"    : "EN",
				"factory" : "hello_english_factory",
				"isolate" : "components1"
			}, {
				"name"    : "FR",
				"factory" : "hello_french_factory",
				"isolate" : "components1"
			}, {
				"name"    : "ES",
				"factory" : "hello_spanish_factory",
				"isolate" : "components2"
			}, {
				"name"    : "AR",
				"factory" : "hello_arabic_factory",
				"isolate" : "components3"
			}
		]
	}
}
