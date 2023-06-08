from hyfms.handles import Hyfms


if __name__ == '__main__':
    hyfms = Hyfms()

    print('\n=== GREEN! ===\n')

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===     ->     ===\n')
    print('\n=== HALF RIGHT ===\n')
    hyfms.goHalfRight()
    hyfms.goAhead()

    print('\n===    --->    ===\n')
    print('\n=== FULL RIGHT ===\n')
    hyfms.goRight()
    hyfms.goAhead()

    print('\n===    --->    ===\n')
    print('\n=== FULL RIGHT ===\n')
    hyfms.goRight()
    hyfms.goAhead()

    print('\n===    --->    ===\n')
    print('\n=== FULL RIGHT ===\n')
    hyfms.goRight()
    hyfms.goAhead()

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===    --->    ===\n')
    print('\n=== FULL RIGHT ===\n')
    hyfms.goRight()
    hyfms.goAhead()

    print('\n=== GREEN. ===\n')

    hyfms.handleExit()
