# ApiTestPython


Tools used:
Python : 3.7.2	
PyTest : 4.3.1
PyCharm : 2018.3.5 Community Edition
Pytest-html : for Reporting
Modules used: requests package


Tests performed:
test_add_new_pet2store(get_new_pet_args):           # to add a new pet to the store
test_get_pet_details(get_pet_id_agrs):       # to get the details of given Pet_id
test_rename_pet(get_rename_pet_args):       # change the name for the given pet
test_sell_pet(get_pet_id_agrs):     # change status of Avialble pet to Sold
test_update_pet_photo				# this is not working
test_update_pet_details(get_update_pet_args):   #to update name or status for the given pet id
test_remove_pet_from_store(get_pet_id_agrs):	#to delete a pet of given id from store


How to run:
Pre-requisite:
install the requests, json, pytest & pytest-html using pip install

Go to the Project <base folder>\tests
command to run: 
	>> pytest testing.py --html=report.html
report.html & petstore_testing.log files generated in tests folder
