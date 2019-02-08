import MacPyver as mp

#test outname:
def outname():
    assert mp.__file__[:-4]+'_test.tif' = mp.outname(mp.__file__, 'test','tif')

