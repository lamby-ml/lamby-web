import os

from lamby.filestore.util import get_object_from_key, get_object_body, \
    download_file_from_key


def test_fs_connection(test_fs):
    pass


def test_get_object_from_key_with_valid_key(test_fs):
    bucket = test_fs.default_bucket
    bucket.put_object(Key='test-obj', Body=b'Hello, World!')

    get_object_from_key('test-obj')


def test_get_object_from_key_handles_invalid_key(test_fs):
    try:
        get_object_from_key('invalid')
    except Exception as e:
        assert e.message == 'Cannot find bucket named invalid\n'


def test_get_object_body_of_valid_object(test_fs):
    bucket = test_fs.default_bucket
    bucket.put_object(Key='test-obj', Body=b'Hello, World!')

    obj = get_object_from_key('test-obj')
    body = get_object_body(obj)

    assert body == 'Hello, World!'


def test_download_file_from_key(test_fs):
    bucket = test_fs.default_bucket
    bucket.put_object(Key='test-obj', Body=b'Hello, World!')

    download_file_from_key('test-obj', 'tmp.txt')

    with open('tmp.txt', 'r') as f:
        assert f.read() == 'Hello, World!'

    os.remove('tmp.txt')
