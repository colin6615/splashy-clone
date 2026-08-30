# Source - https://stackoverflow.com/a/47422975
# Posted by TemporalWolf, modified by community. See post 'Timeline' for change history
# Retrieved 2026-08-30, License - CC BY-SA 3.0
score = 4
with open("highscore.txt", "r+") as hisc:
    hi = hisc.read()
    if not hi:  # not hi will only be true for strings on an empty string
        hi = "0"
    if score > int(hi):
        print("NEW HIGHSCORE!")
        print(score)
        hisc.seek(0)  # We already read to the end. We need to go back to the start
        hisc.write(str(score))
        hisc.truncate()  # Delete anything left over... not strictly necessary
    else:
        print("HIGHSCORE =%s" % hi)
