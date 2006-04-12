#!/usr/bin/env python

class LibraryDoor:
    def verb_open(self, player, tool):
        player.place.oneHears(player,
           to_subject=("After some experimentation, you discover that the door is large, heavy, and has no usable handholds, and that standing around tugging inneffectually on the pistons makes you look silly.",),
           to_other=(player, " gropes for a handhold on the door, and spends a few seconds tugging inneffectually on one of the pistons before finally giving up.")
           )
