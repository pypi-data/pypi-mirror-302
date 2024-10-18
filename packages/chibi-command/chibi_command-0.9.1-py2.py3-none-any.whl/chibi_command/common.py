from chibi_command import Command


class Cp( Command ):
    command = 'cp'
    captive = False
    args = [ '-v' ]
