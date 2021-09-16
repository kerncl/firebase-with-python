from firebase import firebase
from datetime import datetime

firebase = firebase.FirebaseApplication("https://bursa-60b86.firebaseio.com/", None)


def post_data(data):
    """
    Post data to firebase  under 'https://bursa-60b86.firebaseio.com/'
    Args:
        data (dict): data with 'comment', 'date, 'email', 'name'

    Returns:
        None
    """
    result = firebase.post('/comments', data)
    print(f'Posted to firebase \n {result.items()}')


def get_data():
    """
    Retreived Data from firebase
    Returns:
        (dct) contain key: 'comment', 'date', 'email', 'name'
    """
    result = firebase.get('/comments', '')
    for value in result.values():
        print(value)
    return result.values()


def update_data(id, key, value):
    """
    Update date on firebase with give id, key and value
    Args:
        id (str): id number in the database
        key (str): key: 'comment', 'date', 'email', 'name'
        value (str): value of key that wish to update

    Returns:
        None
    """
    id = '/comments/' + id
    firebase.put(id, key, value)
    print('Record Updated')


def delete_data(id, all=False):
    """
    Delete data based on the id number given
    Args:
        id (str): id number of in the database
        all (bool): delete all the data in the database (default: False)
    Returns:
        None
    """
    firebase.delete('/comments', id)
    if all:
        id_number = firebase.get('/comments', '')
        [firebase.delete('/comments/' + i) for i in id_number.values()]
    print('Record Deleted')


if __name__ == '__main__':
    data = {
        'comment': 'Q4 revenue is 10% higher than Q3 revenue',
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'email': 'abc@hotmail.com',
        'name': 'SohaI'
    }
    post_data(data)
    get_data()
    update_data('-MMcvGAwAVJDutLskk7b', 'name', 'sohaisohai')
    delete_data('-MMcuM6gUmwBvsJZLiZ0')
