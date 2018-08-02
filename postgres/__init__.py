
try:
    import pg
except ImportError, e:
    print("no postgres support")
    pass # module doesn't exist, deal with it.
