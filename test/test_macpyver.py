import MacPyver as mp

#test outname:
def outname():
    assert mp.__file__[:-4]+'_test.tif' = mp.outname(mp.__file__, 'test','tif')


def test_glob_rec():
    assert len(mp.info.info.glob_rec(mp.__file__[:-13])) == 505
