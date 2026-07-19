# CHANGELOG

	## v0.3.4 

		### NEW
		1. adding the ability to amake the package
		### UPDATES
		1. import changes to make it work again?!

	## v0.3.3 

		### NEW
		1. adding arguemnts into the subprocess call by combining lists

	## v0.3.2 

		### NEW
		1. adding arguemnts into the subprocess call

	## v0.3.1 

		### NEW
		1. updating so can run hotpath from global python but specify a local venv to run instead

	## v0.3.0 

		### UPDATES
		1. how to use pip to install
		### MISC
		1. issue with incrimention never triggering as line before divides by 0 triggering error and therefore never incrimenting which would fix the error from happening!

	## v0.2.0 

		### NEW
		1. move from printing stdout at the end of the process to streaming the std out; update: move diff into to be developed, counter happens after the print so run count doesn't start at 2
		1. temp hack to remove .git from runs if no ignore files are declared
		### UPDATES
		1. adding comments
		### MISC
		1. printing total stats
		1. Update LICENSE

	## v0.1.1 

		### REFACTORS
		1. state altering logic into state instead of in utils - keeping non state altering functions in utils is the intention

	## v0.1.0 

		### NEW
		1. name to avoid collisions
		1. function in utils which abstracts the logic out of the 'god loop'
		### UPDATES
		1. core refactor and introduced state and associated functionns
		1. default to only not look at .git files
		1. README arguments passed in with acutal CLI flags
		### MISC
		1. issues with ignore files not implimenting the defaults and processing the list correctly