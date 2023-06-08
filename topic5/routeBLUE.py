from hyfms.handles import Hyfms


if __name__ == '__main__':
    hyfms = Hyfms()

    print('\n=== BLUE!! ===\n')

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===     ->     ===\n')
    print('\n=== HALF RIGHT ===\n')
    hyfms.goHalfRight()
    hyfms.goAhead()

    print('\n===     <-     ===\n')
    print('\n=== HALF  LEFT ===\n')
    hyfms.goHalfLeft()
    hyfms.goAhead()

    print('\n===    <---    ===\n')
    print('\n=== FULL  LEFT ===\n')
    hyfms.goLeft()
    hyfms.goAhead()

    print('\n===    <---    ===\n')
    print('\n=== FULL  LEFT ===\n')
    hyfms.goLeft()
    hyfms.goAhead()

    print('\n===    <---    ===\n')
    print('\n=== FULL  LEFT ===\n')
    hyfms.goLeft()
    hyfms.goAhead()

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    print('\n===    <---    ===\n')
    print('\n=== FULL  LEFT ===\n')
    hyfms.goLeft()
    hyfms.goAhead()

    print('\n===  STRAIGHT  ===\n')
    hyfms.goAhead()

    hyfms.handleExit()
