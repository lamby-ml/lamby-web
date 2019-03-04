def test_fs_put_object(test_fs):
    bucket = test_fs.default_bucket
    bucket.put_object(Key='test-obj', Body=b'Hello, World!')
