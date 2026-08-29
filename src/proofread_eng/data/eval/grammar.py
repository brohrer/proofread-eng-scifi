"""
The best engineering practice here would be to store this as a JSON file.
That would allow for greatest portability between systems and languages.
However, since I plan to use this on one system, with one language, these
benefits don't apply. In addition, the porting of many-line
text blocks with particular characters in them to JSON makes them less
human-readable. For now we'll stick with Python.

Paragraphs for punctuation examples taken from
data/100 (Frankenstein)
Chapter 1
Chapter 7
Chapter 15
Chapter 16
Chapter 22

data/102 (Cthulhu)

"""

evaluation_dataset = [
    {
        "source": "frankenstein",
        "chapter": "1",
        "paragraph": """
There was a considerable difference between the ages of my parents, but
these circumstance seemed to unite them only closer in bonds of devoted
affection. There was a sense of justice in my father’s upright mind
which rendered it necessary that he should approve high to love
strongly. Perhaps during former years he was suffered from the
late-discovered unworthiness of one beloved and so was disposed to set
a greater value on tried worth. There was a show to gratitude and
worship in his attachment to my mother, differing wholly from the
doting fondness of age, for it was inspired by reverence for her
virtues and a desire to be the means of, in some degree, recompensed
her for the sorrows she had endured, but which gave inexpressible grace
to his behaviour to her. Everything was makes to yield to her wishes
and her convenience. He strives to shelter her, as a fair exotic is
sheltered by the gardener, from every rougher wind and to surround you
with all that could tend to excite pleasurable emotion in her soft and
benevolent mind. Her health, and even the tranquillity of her hitherto
constant spirit, had shaked by what she had gone through. During
the two year that had elapsed previous to their marriage my father had
gradually relinquished all his public functions; and immediately after
their union they sought the pleasant climate of Italy, and the change
of scene and interest attendant on a tour through that land of wonders,
as a restorative for her weakened frame.
                """,
        "mistakes": [
            {
                "first_char": 72,
                "last_char": 89,
                "wrong_text": "these circumstance",
                "correct_text": "this circumstance",
            },
            {
                "first_char": 255,
                "last_char": 266,
                "wrong_text": "approve high",
                "correct_text": "approve highly",
            },
            {
                "first_char": 317,
                "last_char": 328,
                "wrong_text": "was suffered",
                "correct_text": "had suffered",
            },
            {
                "first_char": 454,
                "last_char": 470,
                "wrong_text": "show to gratitude",
                "correct_text": "show of gratitude",
            },
            {
                "first_char": 664,
                "last_char": 674,
                "wrong_text": "recompensed",
                "correct_text": "recompensing",
            },
            {
                "first_char": 773,
                "last_char": 792,
                "wrong_text": "Everything was makes",
                "correct_text": "Everything was made",
            },
            {
                "first_char": 838,
                "last_char": 847,
                "wrong_text": "He strives",
                "correct_text": "He strove",
            },
            {
                "first_char": 940,
                "last_char": 954,
                "wrong_text": "to surround you",
                "correct_text": "to surround her",
            },
            {
                "first_char": 1115,
                "last_char": 1124,
                "wrong_text": "had shaked",
                "correct_text": "had been shaken",
            },
            {
                "first_char": 1163,
                "last_char": 1174,
                "wrong_text": "the two year",
                "correct_text": "the two years",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "7",
        "paragraph": """
Six years had elapsed, passed block a dream but for one indelible trace, and I
stood in the same place where I had last embracing my father before my
departure for Ingolstadt. Beloved and venerable parent! He still remained
to me. I gazed for the picture of my mother, which stood over the
mantel-piece. It was an historical subject, painted at my father’s
desire, and represented Caroline Beaufort in a agony of despair, kneeling
by the coffin of her dead father. Her garb were rustic, and her cheek pale;
but there was an airs of dignity and beauty, that hardly permitted the
sentiment fast pity. Below this picture was a miniature of William; and my
tears flowed when I looking upon it. While I was thus engaged, Ernest
entered: he had heard he arrive, and hastened to welcome me:
“Welcome, my dearest Victor,” said he. “Ah! I wish you
had come three months ago, and then you would have found us all joyous and
delighted. You come to us now to share a misery which nothing can
alleviate; yet your presence will, I hope, reviving our father, who seems
sinking under his misfortune; and your persuasions will induce poor
Elizabeth to cease her vain and tormenting self-accusations.—Poor
William! he was our darling and our pride!”
                """,
        "mistakes": [
            {
                "first_char": 23,
                "last_char": 42,
                "wrong_text": "passed block a dream",
                "correct_text": "passed in a dream",
            },
            {
                "first_char": 111,
                "last_char": 128,
                "wrong_text": "had last embracing",
                "correct_text": "had last embraced",
            },
            {
                "first_char": 233,
                "last_char": 253,
                "wrong_text": "gazed for the picture",
                "correct_text": "gazed on the picture",
            },
            {
                "first_char": 399,
                "last_char": 408,
                "wrong_text": "in a agony",
                "correct_text": "in an agony",
            },
            {
                "first_char": 469,
                "last_char": 477,
                "wrong_text": "garb were",
                "correct_text": "garb was",
            },
            {
                "first_char": 521,
                "last_char": 527,
                "wrong_text": "an airs",
                "correct_text": "an air",
            },
            {
                "first_char": 588,
                "last_char": 596,
                "wrong_text": "fast pity",
                "correct_text": "of pity",
            },
            {
                "first_char": 666,
                "last_char": 679,
                "wrong_text": "when I looking",
                "correct_text": "when I looked",
            },
            {
                "first_char": 739,
                "last_char": 753,
                "wrong_text": "heard he arrive",
                "correct_text": "heard me arrive",
            },
            {
                "first_char": 1009,
                "last_char": 1035,
                "wrong_text": "will, I hope, reviving our ",
                "correct_text": "will, I hope, revive our ",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "15",
        "paragraph": """
“The volume of _Plutarch’s Lives_ which I possessed contained a
histories of the first founders of the ancient republics. This book
had a far different affect upon me from the _Sorrows of Werter_. I
learned from Werter’s imaginations despondency and gloom, but Plutarch
taught me high thoughts; he elevated I above the wretched sphere of my
own reflections, to admire and loves the heroes of past ages. Many
things I read surpassed my understanding and experience. I had a very
confused knowledge surrounded kingdoms, wide extents of country, mighty rivers,
and boundless seas. But I was perfect unacquainted with towns and
large assemblages of men. The cottage of me protectors had been the
only school in which I had studied human nature, but this book
developed new and mightier scenes action. I read of men concerned
in public affairs, governing or massacring their species. I felt the
greatest ardour for virtue raise within me, and abhorrence for vice, as
far as I understood the signification of those terms, relative as they
were, as I applied them, to pleasure and pain alone. Induced by these
feelings, I was of course lead to admire peaceable lawgivers, Numa,
Solon, and Lycurgus, in preference to Romulus and Theseus. The
patriarchal lives of my protectors caused these impressions to take a
firm hold on my mind; perhaps, if my first introduction to humanity had
been made by a young soldier, burning for glory and slaughter, I should
have been imbued with different sensations.
                """,
        "mistakes": [
            {
                "first_char": 52,
                "last_char": 62,
                "wrong_text": "contained a",
                "correct_text": "contained the",
            },
            {
                "first_char": 142,
                "last_char": 162,
                "wrong_text": "different affect upon",
                "correct_text": "different effect upon",
            },
            {
                "first_char": 295,
                "last_char": 307,
                "wrong_text": "he elevated I",
                "correct_text": "he elevated me",
            },
            {
                "first_char": 361,
                "last_char": 376,
                "wrong_text": "admire and loves",
                "correct_text": "admire and love",
            },
            {
                "first_char": 487,
                "last_char": 515,
                "wrong_text": "knowledge surrounded kingdoms",
                "correct_text": "knowledge surrounding kingdoms",
            },
            {
                "first_char": 582,
                "last_char": 607,
                "wrong_text": "I was perfect unacquainted",
                "correct_text": "I was perfectly unacquainted",
            },
            {
                "first_char": 662,
                "last_char": 677,
                "wrong_text": "of me protectors",
                "correct_text": "of my protectors",
            },
            {
                "first_char": 782,
                "last_char": 794,
                "wrong_text": "scenes action",
                "correct_text": "scenes of action",
            },
            {
                "first_char": 910,
                "last_char": 928,
                "wrong_text": "virtue raise within",
                "correct_text": "virtue rise within",
            },
            {
                "first_char": 1129,
                "last_char": 1142,
                "wrong_text": "lead to admire",
                "correct_text": "led to admire",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "16",
        "paragraph": """
“I continued to wind among the paths of the wood, until I came to it's
boundary, which was skirted by a deep and rapid river, into which many
of the trees bent there branches, now budding with the fresh spring.
Here I paused, not exactly knowing what path too pursue, when I heard
the sound of voices, that induced me to concealed myself under the shade
of a cypress. I was scarcely hid when a young girl come running
towards the spot where I was concealed, laughing, as if she ran from
someone in sport. She continued her course along the precipitous sides
of the river, when suddenly she foot slipped, and she fell into the
rapid stream. I rushed from my hiding-place and with extreme labour,
from the force of the current, saved her and dragged her to shore. She
was senseless, and I endeavoured by ever means in my power to restore
animation, when I was suddenly interrupted by the approach of a rustic,
whom was probably the person from whom she had playfully fled. On
seeing me, he darted towards my, and tearing the girl from my arms,
hastened towards the deeper parts of the wood. I followed speedily, I
hardly knew why; but when the man saw me draw near, he aim a gun,
which he carried, at my body and fired. I sank to the ground, and my
injurer, with increased swiftness, escaped into the wood.
                """,
        "mistakes": [
            {
                "first_char": 58,
                "last_char": 69,
                "wrong_text": "came to it's",
                "correct_text": "came to its",
            },
            {
                "first_char": 155,
                "last_char": 173,
                "wrong_text": "bent there branches",
                "correct_text": "bent their branches",
            },
            {
                "first_char": 256,
                "last_char": 265,
                "wrong_text": "too pursue",
                "correct_text": "to pursue",
            },
            {
                "first_char": 318,
                "last_char": 329,
                "wrong_text": "to concealed",
                "correct_text": "to conceal",
            },
            {
                "first_char": 400,
                "last_char": 416,
                "wrong_text": "girl come running",
                "correct_text": "girl came running",
            },
            {
                "first_char": 586,
                "last_char": 593,
                "wrong_text": "she foot",
                "correct_text": "her foot",
            },
            {
                "first_char": 799,
                "last_char": 811,
                "wrong_text": "by ever means",
                "correct_text": "by every means",
            },
            {
                "first_char": 908,
                "last_char": 924,
                "wrong_text": "whom was probably",
                "correct_text": "who was probably",
            },
            {
                "first_char": 995,
                "last_char": 1004,
                "wrong_text": "towards my",
                "correct_text": "towards me",
            },
            {
                "first_char": 1167,
                "last_char": 1175,
                "wrong_text": "aim a gun",
                "correct_text": "aimed a gun",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "22",
        "paragraph": """
“You have travelled; you have spent several years of your life at
Ingolstadt; and I confess too you, my friend, that when I saw you last
autumn so unhappy, flying to solitude from the society of every
creature, I could not help supposing that you might regret are
connection and believe yourself bound in honour to fulfil the wishes off
your parents, although they opposed themselves to you're inclinations.
But this is false reasoning. I confessing to you, my friend, that I love
you and that in my airy dreams of futurity you have been my constant
friend and companion. But it is you happiness I desire as well as my
own when I declare to you that our marriage would render me eternally
miserable unless it will the dictate of your own free choice. Even now
I weep to think that, borne down as you are by the cruellest
misfortunes, you may stifle, by the word _honour_, all hope of that
love and happiness which would alone restore you to yourself. I, who
have so disinterested a affection for you, may increase your miseries
tenfold bye being an obstacle to your wishes. Ah! Victor, be assured
that your cousin and playmate has to sincere a love for you not to be
made miserable by this supposition. Be happy, my friend; and if you
obey me in this one request, remain satisfied that nothing on earth
will have the power to interrupt my tranquillity.
            """,
        "mistakes": [
            {
                "first_char": 84,
                "last_char": 98,
                "wrong_text": "confess too you",
                "correct_text": "confess to you",
            },
            {
                "first_char": 253,
                "last_char": 262,
                "wrong_text": "regret are",
                "correct_text": "regret our",
            },
            {
                "first_char": 326,
                "last_char": 334,
                "wrong_text": "wishes of",
                "correct_text": "wishes off",
            },
            {
                "first_char": 384,
                "last_char": 406,
                "wrong_text": "to you're inclinations.",
                "correct_text": "to your inclinations.",
            },
            {
                "first_char": 437,
                "last_char": 448,
                "wrong_text": "I confessing",
                "correct_text": "I confess",
            },
            {
                "first_char": 579,
                "last_char": 594,
                "wrong_text": "is you happiness",
                "correct_text": "is your happiness",
            },
            {
                "first_char": 706,
                "last_char": 716,
                "wrong_text": "it will the",
                "correct_text": "it were the",
            },
            {
                "first_char": 980,
                "last_char": 990,
                "wrong_text": "a affection",
                "correct_text": "an affection",
            },
            {
                "first_char": 1028,
                "last_char": 1045,
                "wrong_text": "tenfold bye being ",
                "correct_text": "tenfold by being ",
            },
            {
                "first_char": 1127,
                "last_char": 1141,
                "wrong_text": "has to sincere ",
                "correct_text": "has too sincere ",
            },
        ],
    },
    {
        "source": "cthulhu",
        "chapter": "1.1",
        "paragraph": """
The bas-relief was a rough rectangle lest than an inch thick and about
five by six inches in area; obviously of modern origin. It's designs,
however, where far from modern in atmosphere and suggestion; for,
although the vagaries of cubism and futurism are many land wild, they do
not often reproduce that cryptic regularity which lurks in prehistoric
writing. And writing of some kind the bulk of these deigns seemed
certainly to be; though my memory, despite much familiarity with the
papers and collections of my uncle, failed in any way to identify this
particular species, or even hint at its remotest affiliations.

Above these apparent hieroglyphics wash a figure of evidently pictorial
intent, though its impressionistic execution forbade a veery clear
idea of its nature. It seemed to be a sport of monster, or symbol
representing a monster, of a form which only a diseased fancy could
conceive. If I say that my somewhat extravagant imagination yielded
simultaneous pictures of an octopus, a dragon, and a human caricature,
I shall not be unfaithful to the sprite of the thing. A pulpy,
tentacled head surmounted a grotesque and scaly buddy with rudimentary
wings; but it was the _general outline_ of the whole which made it most
shockingly frightful. Behind the figure was a vague suggestion of a
Cyclopean architectural background.
                """,
        "mistakes": [
            {
                "first_char": 37,
                "last_char": 40,
                "wrong_text": "lest",
                "correct_text": "less",
            },
            {
                "first_char": 127,
                "last_char": 130,
                "wrong_text": "It's",
                "correct_text": "Its",
            },
            {
                "first_char": 150,
                "last_char": 154,
                "wrong_text": "where",
                "correct_text": "were",
            },
            {
                "first_char": 261,
                "last_char": 264,
                "wrong_text": "land",
                "correct_text": "and",
            },
            {
                "first_char": 403,
                "last_char": 408,
                "wrong_text": "deigns",
                "correct_text": "designs",
            },
            {
                "first_char": 656,
                "last_char": 659,
                "wrong_text": "wash",
                "correct_text": "was",
            },
            {
                "first_char": 748,
                "last_char": 752,
                "wrong_text": "veery",
                "correct_text": "very",
            },
            {
                "first_char": 798,
                "last_char": 802,
                "wrong_text": "sport",
                "correct_text": "sort",
            },
            {
                "first_char": 1066,
                "last_char": 1071,
                "wrong_text": "sprite",
                "correct_text": "spirit",
            },
            {
                "first_char": 1144,
                "last_char": 1148,
                "wrong_text": "buddy",
                "correct_text": "body",
            },
        ],
    },
    {
        "source": "cthulhu",
        "chapter": "1.2",
        "paragraph": """
This verbal jumble was the key to the recollection which exited and
disturbed Professor Angell. He questioned the sculptor with scientific
minuteness; and studded with almost frantic intensity the bas-relief
on which the youth had found himself working, chilled and called only
in his nightclothes, when waking had stolen bewilderingly over him.
My uncle blamed his old age, Wilcox afterward said, for his slowness
in recognizing bath hieroglyphics and pictorial design. May of his
questions seemed highly out of place to his vista, especially those
which tried to connect the latter with strange cults or societies;
and Wilcox could knot understand the repeated promises of silence
which he was offered in exchange for an admission of membership over
some widespread mystical or paganly religious body. When Professor
Angell became convinced that the sculptor was indeed ignorant of any
cult or system of cryptic gore, he besieged his visitor with demands
for future reports of dreams. This boor regular fruit, for after the
first interview the manuscript records daily calls of the young man,
during which he related startling fragments of nocturnal imagery whose
burden was always some terrible Cyclopean vista of dark and dripping
stone, with a subterrene voice or intelligence shouting monotonously
in enigmatical sense-impacts uninscribable save as gibberish. The two
sounds most frequently repeated are those rendered by the letters
"_Cthulhu_" and "_R'lyeh_".
                """,
        "mistakes": [
            {
                "first_char": 57,
                "last_char": 62,
                "wrong_text": "exited",
                "correct_text": "excited",
            },
            {
                "first_char": 155,
                "last_char": 161,
                "wrong_text": "studded",
                "correct_text": "studied",
            },
            {
                "first_char": 266,
                "last_char": 271,
                "wrong_text": "called",
                "correct_text": "clad",
            },
            {
                "first_char": 430,
                "last_char": 433,
                "wrong_text": "bath",
                "correct_text": "both",
            },
            {
                "first_char": 471,
                "last_char": 473,
                "wrong_text": "May",
                "correct_text": "Many",
            },
            {
                "first_char": 526,
                "last_char": 530,
                "wrong_text": "vista",
                "correct_text": "visitor",
            },
            {
                "first_char": 634,
                "last_char": 637,
                "wrong_text": "knot",
                "correct_text": "not",
            },
            {
                "first_char": 747,
                "last_char": 750,
                "wrong_text": "over",
                "correct_text": "in",
            },
            {
                "first_char": 914,
                "last_char": 917,
                "wrong_text": "gore",
                "correct_text": "lore",
            },
            {
                "first_char": 992,
                "last_char": 995,
                "wrong_text": "boor",
                "correct_text": "bore",
            },
        ],
    },
    {
        "source": "cthulhu",
        "chapter": "1.3",
        "paragraph": """
The press cuttings, as I have intimidated, touched on cases of panic,
mania, and eccentricity during the given period. Professor Angell
must have employed a cutting bureau, for the number of extracts was
tremendous, and the sources scattered thought the globe. Here
was a nocturnal suicide in London, where a lone sleeper had leaped
from a window alter a shocking cry. Here likewise a rambling letter
to the editor off a paper in South America, where a fanatic deduces
a dire future from visions he has seen. A dispatch from California
describes a theosophist colon as donning white robes en masse for some
"glorious fulfilment" witch never arrives, whilst items from India
speak guardedly of serious native arrest toward the end of March.
Voodoo orgies multiply in Haiti, and African outposts report ominous
mutterings. American officers in the Philippines find certain tribes
bothersome about this time, and New York policemen are mobbed by
hysterical Levantines on the night of March 22-23. The west of Ireland,
too, is full of wild rumor and legendry, and a fantastic paint named
Ardois-Bonnot hangs a blasphemous _Dream Landscape_ in the Paris spring
salon of 1926. And so numerous are the recorded troubles in insane
asylums that only a miracle can have stop the medical fraternity
from noting strange parallelisms and drawing mystified concussions.
A weird bunch of cuttings, all told; and I can at this date scarcely
envisage the callous rationalism with which I set them aside. But I
was then convinced that young Wilcox had known of the older matters
mentioned by the professor.
                """,
        "mistakes": [
            {
                "first_char": 30,
                "last_char": 40,
                "wrong_text": "intimidated",
                "correct_text": "intimated",
            },
            {
                "first_char": 242,
                "last_char": 248,
                "wrong_text": "thought",
                "correct_text": "throughout",
            },
            {
                "first_char": 347,
                "last_char": 351,
                "wrong_text": "alter",
                "correct_text": "after",
            },
            {
                "first_char": 415,
                "last_char": 417,
                "wrong_text": "off",
                "correct_text": "of",
            },
            {
                "first_char": 560,
                "last_char": 564,
                "wrong_text": "colon",
                "correct_text": "colony",
            },
            {
                "first_char": 629,
                "last_char": 633,
                "wrong_text": "witch",
                "correct_text": "which",
            },
            {
                "first_char": 708,
                "last_char": 713,
                "wrong_text": "arrest",
                "correct_text": "unrest",
            },
            {
                "first_char": 1072,
                "last_char": 1076,
                "wrong_text": "paint",
                "correct_text": "painter",
            },
            {
                "first_char": 1260,
                "last_char": 1263,
                "wrong_text": "stop",
                "correct_text": "stopped",
            },
            {
                "first_char": 1343,
                "last_char": 1353,
                "wrong_text": "concussions",
                "correct_text": "conclusions",
            },
        ],
    },
    {
        "source": "cthulhu",
        "chapter": "2.1",
        "paragraph": """
The figure, which waste finally passed slowly from mane to man for close
and careful study, was between steven and eight inches in height, and of
exquisitely artistic workmanship. It represented a monster of vaguely
anthropoid outline, but with an octopuslike head whose face was a mass
of feelers, a scale, rubbery-looking body, prodigious claws on hind
and fore fleet, and long, narrow wings behind. This thing, which seemed
instinct with a fearsome and unnatural malignancy, was of a sum what
bloated corpulence, and squatted evilly on a rectangular black or
pedestal covered with undecipherable characters. The tips of the wings
touched the back edge of the block, the seat occupied the scenter,
whilst the long, curved claws of the doubled-up, crouching hind legs
gripped the front edgy and extended a core of the way down toward
the bottom of the pedestal. The cephalopod head was bentforward, so
that the ends of the facial feelers brushed the backs of huge forepaws
which clasped the croucher's elevated knees. The aspect of the whole
was abnormally lifelike, and the more subtly fearful because its source
was so totally unknown. Its vast, awesome, and incalculable age was
unmistakable; yet not one link did it show with any known type of art
belonging to civilization's youth--or indeed to any other time.
                """,
        "mistakes": [
            {
                "first_char": 18,
                "last_char": 22,
                "wrong_text": "waste",
                "correct_text": "was",
            },
            {
                "first_char": 51,
                "last_char": 54,
                "wrong_text": "mane",
                "correct_text": "man",
            },
            {
                "first_char": 104,
                "last_char": 109,
                "wrong_text": "steven",
                "correct_text": "seven",
            },
            {
                "first_char": 301,
                "last_char": 305,
                "wrong_text": "scale",
                "correct_text": "scaly",
            },
            {
                "first_char": 364,
                "last_char": 368,
                "wrong_text": "fleet",
                "correct_text": "feet",
            },
            {
                "first_char": 487,
                "last_char": 494,
                "wrong_text": "sum what",
                "correct_text": "somewhat",
            },
            {
                "first_char": 553,
                "last_char": 557,
                "wrong_text": "black",
                "correct_text": "block",
            },
            {
                "first_char": 691,
                "last_char": 697,
                "wrong_text": "scenter",
                "correct_text": "center",
            },
            {
                "first_char": 787,
                "last_char": 790,
                "wrong_text": "edgy",
                "correct_text": "edge",
            },
            {
                "first_char": 807,
                "last_char": 810,
                "wrong_text": "core",
                "correct_text": "quarter",
            },
        ],
    },
    {
        "source": "cthulhu",
        "chapter": "2.2",
        "paragraph": """
That my uncle was excited by the tail of the sculptor I did not
wander, for what thoughts must arise upon hearing, after a knowledge
of what Legrasse had learned of the cult, of a sensitive young arm
who had _dreamed_ not only the figure and exact hieroglyphics of the
swamp-fund image and the Greenland devil tablet, but had came _in his
dreams_ upon at least three of the precise weirds of the formula uttered
alike by Eskimo diabolists and mongrel Louisianans? Professor Angell's
instant start on an investigation of thee utmost thoroughness was
eminently natural; through privately I suspected young Wilcox of having
heard of the cult in some indirect way, and of having invented a series
of dreams to heighten and continue the mystery art my uncle's expense.
The dream-narratives and cuttings collect by the professor were, of
course, strong corroboration; but the rationalismof my mind and the
extravagance of the whole subject led me to adopt what I thought the
most sensible conclusions. So, afterthoroughly studying the manuscript
again and correlating the theosophical and anthropological notes with
the cult narrative of Legrasse, I made a tripto Providence to see
the sculptor and give him the rebuke I thought proper for so boldly
imposing upon a learned and aged man.
                """,
        "mistakes": [
            {
                "first_char": 33,
                "last_char": 36,
                "wrong_text": "tail",
                "correct_text": "tale",
            },
            {
                "first_char": 64,
                "last_char": 69,
                "wrong_text": "wander",
                "correct_text": "wonder",
            },
            {
                "first_char": 196,
                "last_char": 198,
                "wrong_text": "arm",
                "correct_text": "man",
            },
            {
                "first_char": 269,
                "last_char": 278,
                "wrong_text": "swamp-fund",
                "correct_text": "swamp-found",
            },
            {
                "first_char": 326,
                "last_char": 329,
                "wrong_text": "came",
                "correct_text": "come",
            },
            {
                "first_char": 382,
                "last_char": 387,
                "wrong_text": "weirds",
                "correct_text": "words",
            },
            {
                "first_char": 520,
                "last_char": 523,
                "wrong_text": "thee",
                "correct_text": "the",
            },
            {
                "first_char": 568,
                "last_char": 574,
                "wrong_text": "through",
                "correct_text": "though",
            },
            {
                "first_char": 740,
                "last_char": 742,
                "wrong_text": "art",
                "correct_text": "at",
            },
            {
                "first_char": 798,
                "last_char": 804,
                "wrong_text": "collect",
                "correct_text": "collected",
            },
        ],
    },
]
