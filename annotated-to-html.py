import re

test = """When the sand//sand.n.01 coating//coating.n.01 was wiped//wipe.v.01
off, a green//green.s.01 tint//shade.n.02 appeared//appear.v.02 . It was a
lump//hunk.n.02 of glass//glass.n.01 , so//so.r.01 thick//thick.a.01 as to be
almost//about.r.07 opaque//opaque.a.01 ; the smoothing of the sea//sea.n.01 had
completely//wholly.r.01 worn//wear.v.04 off any edge//edge.n.01 or
shape//shape.n.01 , so that it was impossible//impossible.a.01 to
say//allege.v.01 whether it had been bottle//bottle.n.01 , tumbler//tumbler.n.02
or window//window.n.01 -pane//pane.n.01 ; it was nothing but glass//glass.n.01 ;
it was almost//about.r.07 a precious//precious.s.02 stone//gem.n.02 . You had
only//merely.r.01 to enclose//envelop.v.01 it in a rim//rim.n.01 of
gold//gold.n.03 , or pierce//pierce.v.05 it with a wire//wire.n.01 , and it
became//become.v.02 a jewel//jewel.n.01 ; part//part.n.02 of a
necklace//necklace.n.01 , or a dull//dull.a.02 , green//green.s.01
light//light.n.01 upon a finger//finger.n.01 . Perhaps//possibly.r.01
after//subsequently.r.01 all//wholly.r.01 it was really//truly.r.01 a
gem//jewel.n.01 ; something worn//wear.v.02 by a dark//black.s.05 Princess
trailing//chase.v.01 her finder//finder.n.01 in the water//body_of_water.n.01 as
she sat//sit.v.01 in the stern//stern.n.01 of the boat//boat.n.01 and
listened//listen.v.01 to the slaves//slave.n.02 singing//singe.v.01 as they
rowed//row.v.01 her across the Bay. Or the oak//oak.n.01 sides//side.n.05 of a
sunk//sink.v.04 Elizabethan//elizabethan.a.01 treasure//treasure.n.01
-chest//chest.n.02 had split//burst.v.01 apart//apart.r.06 , and,
rolled//roll.v.01 over//over.r.01 and over//over.r.01 , over//over.r.01 and
over//over.r.01 , its emeralds//emerald.n.01 had come//come.v.04 at
last//last.r.02 to short//light.s.18 . John turned//turn.v.04 it in his
hands//hand.n.01 ; he held//hold.v.02 it to the light//light.n.02 ; he
held//hold.v.02 it so that its irregular//irregular.a.01 mass//mass.n.03
blotted//blot.v.01 out the body//body.n.01 and extended//stretch.v.02
right//right.a.01 arm//arm.n.01 of his friend//friend.n.01 . The
green//green.n.01 thinned//thin.v.01 and thickened//thicken.v.02
slightly//slightly.r.01 as it was held//hold.v.02 against the sky//sky.n.01 or
against the body//body.n.01 . It pleased//please.v.01 him; it
puzzled//perplex.v.01 him; it was so//so.r.01 hard//hard.a.02 , so//so.r.01
concentrated//hard.a.07 , so//therefore.r.01 definite//definite.a.01 an
object//aim.n.02 compared//compare.v.01 with the vague//dim.s.02 sea//sea.n.01
and the hazy//bleary.s.02 shore//shore.n.02. [cite:@1920athenaeum 543]
"""

print(re.sub(r"\b\s([A-Za-z]+?)//([a-z_]+?)\.[navs]\.[0-9]{2}\b",
       ' <a class="synset" href="http://wordnet-rdf.princeton.edu/lemma/\g<1>">\g<2></a> ',
       test))
