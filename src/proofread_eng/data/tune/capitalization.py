"""
The best engineering practice here would be to store this as a JSON file.
That would allow for greatest portability between systems and languages.
However, since I plan to use this on one system, with one language, these
benefits don't apply. In addition, the porting of many-line
text blocks with particular characters in them to JSON makes them less
human-readable. For now we'll stick with Python.

Paragraphs for capitalization examples taken from
Chapter 2
Chapter 3
Chapter 4
Chapter 21
Chapter 23

With the help of randomized chapter order
[14, 12, 8, 5, 3, 23, 4, 2, 21, 24, 20, 18, 9, 10, 7, 1, 16, 22, 15, 19, 6, 13, 17, 11]
"""

evaluation_dataset = [
    {
        "source": "Frankenstein",
        "chapter": "2",
        "paragraph": """
On the birth of a second son, my junior by seven years, my parents gave
up Entirely their wandering life and fixed themselves in their native
country. We possessed a house in Geneva, and a _campagne_ on belrive,
the eastern shore of the lake, at the distance of rather more than a
league from the city. we resided principally in the latter, and the
lives of my parents were passed in considerable seclusion. It was my
temper to avoid a crowd and to Attach myself fervently to a few. I was
indifferent, therefore, to my school-fellows in general; but I united
myself in the bonds of the closest friendship to one among them. henry
Clerval was the son of a merchant of geneva. He was a boy of singular
talent and fancy. He Loved enterprise, hardship, and even danger for
its own sake. He was deeply read in books of chivalry and romance. He
composed heroic songs and began to write many A tale of enchantment and
knightly adventure. He tried to make us act plays and to enter into
masquerades, in which the characters were drawn from the heroes of
roncesvalles, of the round table of King Arthur, and the chivalrous
train who shed their blood to redeem the holy sepulchre from the hands
of the infidels.
                """,
        "mistakes": [
            {
                "first_char": 75,
                "last_char": 82,
                "wrong_text": "Entirely",
                "correct_text": "entirely",
            },
            {
                "first_char": 203,
                "last_char": 209,
                "wrong_text": "belrive",
                "correct_text": "Belrive",
            },
            {
                "first_char": 303,
                "last_char": 305,
                "wrong_text": "we ",
                "correct_text": "We ",
            },
            {
                "first_char": 449,
                "last_char": 455,
                "wrong_text": "Attach ",
                "correct_text": "attach ",
            },
            {
                "first_char": 624,
                "last_char": 628,
                "wrong_text": "henry",
                "correct_text": "Henry",
            },
            {
                "first_char": 667,
                "last_char": 672,
                "wrong_text": "geneva",
                "correct_text": "Geneva",
            },
            {
                "first_char": 721,
                "last_char": 725,
                "wrong_text": "Loved",
                "correct_text": "loved",
            },
            {
                "first_char": 885,
                "last_char": 885,
                "wrong_text": "A",
                "correct_text": "a",
            },
            {
                "first_char": 1046,
                "last_char": 1057,
                "wrong_text": "roncesvalles",
                "correct_text": "Roncesvalles",
            },
            {
                "first_char": 1067,
                "last_char": 1078,
                "wrong_text": "round table ",
                "correct_text": "Round Table ",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "3",
        "paragraph": """
I closed not my eyes that night. My internal being was in a state of
insurrection and turmoil; i felt that order would thence arise, but I
had no power to produce it. By degrees, after the morning’s dawn,
sleep came. I awoke, and my Yesternight’s thoughts were as a dream.
There only remained a resolution to return to my ancient studies and to
devote myself to a science for which I believed mySelf to possess a
natural talent. On the same day I paid M. waldman a visit. His
manners in private were even more mild and attractive than in public,
for there was a certain dignity in his Mien during his lecture which in
his own house was replaced by the greatest affability and kindness. I
gave Him pretty nearly the same account of my former pursuits as I had
given to his fellow professor. He heard with attention the little
narration concerning my studies and smiled at the names of Cornelius
agrippa and Paracelsus, but without the contempt that M. krempe had
exhibited. He said that “These were men to whose indefatigable zeal
modern philosophers were indebted for most of the foundations of their
knowledge. They had left to us, as an easier task, to give new names
and arrange in connected Classifications the facts which they in a
great degree had been the instruments of bringing to light. The
labours of men of genius, however erroneously directed, scarcely ever
fail in ultimately turning to the solid advantage of mankind.” I
listened to his statement, which was delivered without any presumption
or affectation, and then added that his lecture had removed my
prejudices against modern chemists; I expressed myself in measured
terms, with the modesty and deference due from a youth to his
instructor, without letting escape (Inexperience in life would have
made me ashamed) any of the enthusiasm which stimulated my intended
labours. I requested his advice concerning the books I ought to
procure.
            """,
        "mistakes": [
            {
                "first_char": 95,
                "last_char": 95,
                "wrong_text": "i",
                "correct_text": "I",
            },
            {
                "first_char": 233,
                "last_char": 245,
                "wrong_text": "Yesternight’s",
                "correct_text": "yesternight’s",
            },
            {
                "first_char": 393,
                "last_char": 398,
                "wrong_text": "mySelf",
                "correct_text": "myself",
            },
            {
                "first_char": 455,
                "last_char": 461,
                "wrong_text": "waldman",
                "correct_text": "Waldman",
            },
            {
                "first_char": 585,
                "last_char": 588,
                "wrong_text": "Mien",
                "correct_text": "mien",
            },
            {
                "first_char": 693,
                "last_char": 695,
                "wrong_text": "Him",
                "correct_text": "him",
            },
            {
                "first_char": 894,
                "last_char": 900,
                "wrong_text": "agrippa",
                "correct_text": "Agrippa",
            },
            {
                "first_char": 951,
                "last_char": 956,
                "wrong_text": "krempe",
                "correct_text": "Krempe",
            },
            {
                "first_char": 1195,
                "last_char": 1209,
                "wrong_text": "Classifications",
                "correct_text": "classifications",
            },
            {
                "first_char": 1735,
                "last_char": 1746,
                "wrong_text": "Inexperience",
                "correct_text": "inexperience",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "4",
        "paragraph": """
One of the phenomena which had peculiarly attracted my attention was
the structure of the human frame, and, indeed, any animal endued with
life. whence, I often asked myself, did the principle of life proceed?
It was a bold question, and one which has ever been considered as a
mystery; yet with how many things are we upon the brink of becoming
acquainted, if cowardice or Carelessness did not restrain our
inquiries. I revolved these circumstances in my mind and determined
thenceforth to apply myself more particularly to those branches of
natural philosophy which relate to physiology. unless I had been
animated by an almost supernatural enthusiasm, my application to this
study would have BEEN irksome and almost intolerable. To examine the
causes of life, we must first have recourse to death. I became
acquainted with the science of anatomy, but this was not sufficient; I
must also observe the natural Decay and corruption of the human body.
In my education my father had taken the greatest precautions that my
mind should be impressed with no Supernatural Horrors. I do not ever
remember to have trembled at a tale of superstition or to have feared
the apparition of a spirit. darkness had no effect upon my fancy, and
a churchyard was to me merely the receptacle of bodies deprived of
life, which, from being the seat of beauty and strength, had become
food for the worm. Now I was led to examine the cause and progress of
this decay and forced to spend days and nights in vaults and
Charnel-Houses. My attention was fixed upon every object the most
insupportable to the delicacy of the human feelings. I saw how the
fine form of man was degraded and wasted; I beheld the corruption of
death succeed to the Blooming cheek of life; I saw how the worm
inherited the wonders of the eye and brain. I paused, examining and
analysing all the minutiae of causation, as exemplified in the change
from life to death, and death to life, until from the midst of this
darkness a sudden light broke in upon me—a light so brilliant And
wondrous, yet so simple, that while I became dizzy with the immensity
of the prospect which it illustrated, I was surprised that among so
many men of genius who had directed their inquiries towards the same
science, that I alone should be reserved to discover so astonishing a
secret.
            """,
        "mistakes": [
            {
                "first_char": 145,
                "last_char": 150,
                "wrong_text": "whence",
                "correct_text": "Whence",
            },
            {
                "first_char": 374,
                "last_char": 385,
                "wrong_text": "Carelessness",
                "correct_text": "carelessness",
            },
            {
                "first_char": 590,
                "last_char": 595,
                "wrong_text": "unless",
                "correct_text": "Unless",
            },
            {
                "first_char": 695,
                "last_char": 698,
                "wrong_text": "BEEN",
                "correct_text": "been",
            },
            {
                "first_char": 911,
                "last_char": 915,
                "wrong_text": "Decay",
                "correct_text": "decay",
            },
            {
                "first_char": 1053,
                "last_char": 1072,
                "wrong_text": "Supernatural Horrors",
                "correct_text": "supernatural horrors",
            },
            {
                "first_char": 1187,
                "last_char": 1194,
                "wrong_text": "darkness",
                "correct_text": "Darkness",
            },
            {
                "first_char": 1495,
                "last_char": 1508,
                "wrong_text": "Charnel-Houses",
                "correct_text": "charnel-houses",
            },
            {
                "first_char": 1718,
                "last_char": 1725,
                "wrong_text": "Blooming",
                "correct_text": "blooming",
            },
            {
                "first_char": 2029,
                "last_char": 2031,
                "wrong_text": "And",
                "correct_text": "and",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "21",
        "paragraph": """
Still, as I urged our leaving ireland with such inquietude and impatience,
my father thought it best to yield. We took our passage on board a vessel
bound for havre-de-grace and sailed with a fair wind from the irish shores.
It was midnight. I lay on the deck looking at the stars and listening to
the Dashing of the waves. I hailed the darkness that shut Ireland from my
sight, and my pulse beat with a Feverish joy when I reflected that I should
soon see Geneva. The past appeared to me in the light of a frightful dream;
yet the vessel in which I was, the wind that blew me from the Detested
shore of Ireland, and the sea Which surrounded me, told me too forcibly
that I was deceived by no vision and that Clerval, my friend and dearest
companion, had fallen a victim to me and the monster of my Creation. I
repassed, in my memory, my whole life; my quiet happiness while residing
with my family in Geneva, the death of my mother, and my departure for
ingolstadt. I remembered, shuddering, the mad enthusiasm that hurried me on
to the creation of my Hideous enemy, and I called to mind the night in
which he first lived. I was unable to pursue the train of thought; a
thousand feelings pressed upon me, and I wept bitterly.
            """,
        "mistakes": [
            {
                "first_char": 30,
                "last_char": 36,
                "wrong_text": "ireland",
                "correct_text": "Ireland",
            },
            {
                "first_char": 159,
                "last_char": 172,
                "wrong_text": "havre-de-grace",
                "correct_text": "Havre-de-Grace",
            },
            {
                "first_char": 211,
                "last_char": 215,
                "wrong_text": "irish",
                "correct_text": "Irish",
            },
            {
                "first_char": 302,
                "last_char": 308,
                "wrong_text": "Dashing",
                "correct_text": "dashing",
            },
            {
                "first_char": 404,
                "last_char": 411,
                "wrong_text": "Feverish",
                "correct_text": "feverish",
            },
            {
                "first_char": 586,
                "last_char": 593,
                "wrong_text": "Detested",
                "correct_text": "detested",
            },
            {
                "first_char": 625,
                "last_char": 629,
                "wrong_text": "Which",
                "correct_text": "which",
            },
            {
                "first_char": 799,
                "last_char": 806,
                "wrong_text": "Creation",
                "correct_text": "creation",
            },
            {
                "first_char": 955,
                "last_char": 964,
                "wrong_text": "ingolstadt",
                "correct_text": "Ingolstadt",
            },
            {
                "first_char": 1053,
                "last_char": 1059,
                "wrong_text": "Hideous",
                "correct_text": "hideous",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "23",
        "paragraph": """
There were no horses to be procured, and I must return by the lake; but the
wind was unfavourable, and the rain fell In Torrents. However, it was
hardly morning, and I might reasonAbly hope to arrive by night. I hired men
to row and took an oar myself, For I had always experienced relief from
mental torment in bodily exercise. But the Overflowing misery I now felt,
and the excess of agitation that I endured rendered me incapable of any
exertion. I threw down the oar, and Leaning my head upon my hands, gave way
to every gloomy idea that arose. If I looked up, I Saw scenes which were
familiar to me in my happier time and which I had contemplated but the day
before in the company of her who was now but A Shadow and a recollection.
Tears streamed from my eyes. The rain had ceased for a moment, and I saw
the fish play in the waters as they had done a few hours before; they had
then been observed by elizabeth. Nothing is so painful to the human mind as
a great and sudden change. The sun might shine or the clouds Might lower,
but nothing could appear to me as it had done the day before. A fiend had
snatched from me every hope of future happiness; no creature had ever been
so miserable as I was; so Frightful an event is single in the history of
man.
            """,
        "mistakes": [
            {
                "first_char": 117,
                "last_char": 127,
                "wrong_text": "In Torrents",
                "correct_text": "in torrents",
            },
            {
                "first_char": 174,
                "last_char": 183,
                "wrong_text": "reasonAbly",
                "correct_text": "reasonably",
            },
            {
                "first_char": 253,
                "last_char": 255,
                "wrong_text": "For",
                "correct_text": "for",
            },
            {
                "first_char": 337,
                "last_char": 347,
                "wrong_text": "Overflowing",
                "correct_text": "overflowing",
            },
            {
                "first_char": 476,
                "last_char": 482,
                "wrong_text": "Leaning",
                "correct_text": "leaning",
            },
            {
                "first_char": 567,
                "last_char": 569,
                "wrong_text": "Saw",
                "correct_text": "saw",
            },
            {
                "first_char": 709,
                "last_char": 716,
                "wrong_text": "A Shadow",
                "correct_text": "a shadow",
            },
            {
                "first_char": 907,
                "last_char": 915,
                "wrong_text": "elizabeth",
                "correct_text": "Elizabeth",
            },
            {
                "first_char": 1022,
                "last_char": 1026,
                "wrong_text": "Might",
                "correct_text": "might",
            },
            {
                "first_char": 1210,
                "last_char": 1218,
                "wrong_text": "Frightful",
                "correct_text": "frightful",
            },
        ],
    },
]
