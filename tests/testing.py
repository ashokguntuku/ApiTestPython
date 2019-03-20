
import requests
import json
import pytest
import logging



@pytest.fixture(scope="function", params=[{ "id": '123456789', 'name': 'doggie', 'status': 'available' }])
def get_new_pet_args(request):
    param = request.param
    yield param

@pytest.fixture(scope="function", params=['123456789' ,])
def get_pet_id_agrs(request):
    param = request.param
    yield param

@pytest.fixture(scope="function", params=['available' ,])
def get_pet_status_agrs(request):
    param = request.param
    yield param

@pytest.fixture(scope="function", params=[{ "id": '123456789', 'name': 'Rambo', 'status': 'sold' }])
def get_update_pet_args(request):
    param = request.param
    yield param

@pytest.fixture(scope="function", params=[{ "id": '123456789', 'name': 'Rickey'}])
def get_rename_pet_args(request):
    param = request.param
    yield param

def get_logger(module_name, file_name, log_devel=logging.INFO):
    FORMAT = '%(asctime)-15s %(filename)s %(levelname)s : %(message)s'
    logging.basicConfig(filename=file_name, format=FORMAT)
    LOG = logging.getLogger(module_name)
    LOG.setLevel(log_devel)
    return LOG

LOG = get_logger('pet store', 'petstore_testing.log')


base_url =    'https://petstore.swagger.io/v2'

url_find_pets = base_url + '/pet/findByStatus?status={0}' # list of all the pets with a specific status
url_pets = base_url + '/pet'     # Create a new pet (or) Update any of the attributes of pet
url_pet = base_url + '/pet/{0}'  # Get the details of a pet (or) update the name / status of a pet
url_pet_modify_image = base_url + '/pet/{0}/uploadImage'  # add / modify the image of a pet

headers = {'Content-Type': 'application/json',
           'accept': 'application/json'}

def get_response( test_url, headers=None):
    response = requests.get(test_url, headers=headers)
    return response


'''
This is test is to add new pet to the store
test consumnes args prepared by pytest @pytest.fixture
eg: @pytest.fixture(scope="function", params=[{ "pid": '123456789', 'name': 'Ricky', 'status': 'available' }])
'''
def test_add_new_pet2store(get_new_pet_args):           # to add a new pet to the store
    payload = get_new_pet_args
    body = json.dumps(payload)
    LOG.info('Adding new pet to store with pet {0} details'.format(body))
    response = requests.post(url_pets, data=body, headers=headers)
    LOG.debug(' Add pet to store response [ {0} ] '.format(response.text))
    LOG.debug('Add pet to store response code [ {0} ] to store'.format(response.status_code))
    assert response.status_code == 200
    petdetails = json.loads(response.text)
    assert petdetails['status'] == 'available'
    LOG.info('Added pet [ {0} ] to store'.format(response.text))


def test_get_pet_details(get_pet_id_agrs):       # to get the details of given Pet_id
    pet_id = get_pet_id_agrs
    LOG.info('Querying pet details with id {0} '.format(pet_id))
    response = get_response(url_pet.format(pet_id), headers)
    assert response.status_code == 200
    LOG.info('Got pet details [ {0} ] for id {1} '.format(response.text, pet_id))

def test_rename_pet(get_rename_pet_args):       # change the name for the given pet

    ren_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'accept': 'application/json'}
    payload = get_rename_pet_args
    petid = payload['id']
    name = payload['name']
    del payload['id']
    # Get the pet details
    response = get_response(url_pet.format(petid), headers)
    assert response.status_code == 200
    LOG.info('Pet details to be renamed {0} '.format(response.text))

    LOG.info('Renaming pet with new name {0} '.format( name ))
    response = requests.post(url_pet.format(petid), data=payload, headers=ren_headers)
    LOG.debug(' Renaming pet API response [ {0} ] '.format(response.text))
    LOG.debug('Renaming pet API response code [ {0} ] '.format(response.status_code))
    assert response.status_code == 200
    response = get_response(url_pet.format(petid), headers)
    assert response.status_code == 200
    petdetails = json.loads(response.text)
    assert petdetails['name'] == name
    LOG.info('Renamed the pet - details {0} '.format(response.text))


def test_sell_pet(get_pet_id_agrs):     # change status of Avialble pet to Sold
    petid = get_pet_id_agrs
    response = get_response(url_pet.format(petid), headers)
    assert response.status_code == 200
    LOG.info('Pet details to be sold {0} '.format(response.text))

    petdetails = json.loads(response.text)

    assert petdetails['status'] == 'available'

    payload = {  "status": 'sold'    }
    sell_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json'}
    response = requests.post(url_pet.format(petid), data=payload, headers=sell_headers)
    assert response.status_code == 200
    LOG.debug(' Selling pet API response [ {0} ] '.format(response.text))
    LOG.debug('Selling pet API response code [ {0} ] '.format(response.status_code))
    response = get_response(url_pet.format(petid), headers)
    assert response.status_code == 200
    petdetails = json.loads(response.text)
    assert petdetails['status'] == 'sold'
    LOG.info('Sold pet -  details {0} '.format(response.text))


'''
def test_update_pet_photo(petid, img_file):
    #payload = json.load('./data/newpet.json')
    photo_headers = {'Content-Type': 'multipart/form-data',
               'accept': 'application/json'}

    files = {'file': open(img_file, 'rb')}
    body = json.dumps(files)
    response = requests.post(url_pet_modify_image.format(petid), files=body, headers=photo_headers)
    print('photo update status ' + str(response))
    assert response.status_code == 200
'''

def test_update_pet_details(get_update_pet_args):
    payload = get_update_pet_args
    status = payload['status']
    body = json.dumps(payload)
    LOG.info('Updating existing pet with details {0} '.format(body))
    response = requests.put(url_pets, headers=headers, data=body)
    assert response.status_code == 200
    LOG.debug('Update pet API response code {0}  '.format(response.status_code))
    petdetails = json.loads(response.text)
    assert petdetails['status'] == status
    LOG.info('Updated the pet  details {0} '.format(response.text))

def test_get_pets_of_status(get_pet_status_agrs):        # to get the pets list of specific status
    status = get_pet_status_agrs
    LOG.info('Get existing pets with status {0} '.format(status))
    url = url_find_pets.format(status)
    response = get_response(url, headers)
    assert response.status_code == 200
    assert response.text != ''
    pets = json.loads(response.text)
    LOG.info('Got [ {0} ] pets with status {1} '.format(len(pets), status))

def test_remove_pet_from_store(get_pet_id_agrs):
    petid = get_pet_id_agrs
    LOG.info('Removing existing pets {0} from store '.format(petid))
    response = requests.delete(url_pet.format(petid), headers=headers)
    LOG.debug('Remove pet API response code {0}  '.format(response.status_code))
    assert response.status_code == 200
    response = get_response(url_pet.format(petid), headers)
    assert response.status_code != 200
    LOG.info('Removed pet {0} from store  '.format(petid))


'''    
test_add_new_pet2store()
avaialable_pets = json.loads(test_get_pets_of_status('available'))
sold_pets = json.loads(test_get_pets_of_status('sold'))
assert len(avaialable_pets) >= 1
assert len(sold_pets) >= 1
test_get_pet_details(avaialable_pets[0]['id'])
test_sell_pet(avaialable_pets[0]['id'])
#test_update_pet_photo('9199424981609355055', './data/mydoggie.jpg')
test_remove_pet_from_store(sold_pets[0]['id'])
test_update_pet_details(avaialable_pets[0]['id'], name='Rickey')
test_update_pet_details(sold_pets[0]['id'], status='available')

'''
# test_rename_pet(available_pets[0]['id'], 'Rambo')

# test_rename_pet('15435006001686', 'Rambo')
# test_sell_pet('15435006001686')