"""
The best engineering practice here would be to store this as a JSON file.
That would allow for greatest portability between systems and languages.
However, since I plan to use this on one system, with one language, these
benefits don't apply. In addition, the porting of many-line
text blocks with particular characters in them to JSON makes them less
human-readable. For now we'll stick with Python.

Paragraphs for spelling examples taken from
Letter 1
Chapter 14
Chapter 12
Chapter 8
Chapter 5

With the help of randomized chapter order
[14, 12, 8, 5, 3, 23, 4, 2, 21, 24, 20, 18, 9, 10, 7, 1, 16, 22, 15, 19, 6, 13, 17, 11]
"""

evaluation_dataset = [
    {
        "source": "Frankenstein",
        "chapter": "L1",
        "paragraph": """
I am already far north of London, and as I walk in the streets of
Petersburgh, I feel a cold northern breeze play upon my cheeks, which
braces my nerves and fills me with delight. Do you understand this
feeling? This breeze, which has travelled from the regions towards
which I am advancing, gives me a foretaste of those icey climes.
Inspirited by this wind of promise, my daydreams become more fervent
and vivid. I try in vain to be persuaded that the pole is the seat of
frost and desolation; it ever presents itself to my imagniation as the
region of beauty and delight. There, Margaret, the sun is for ever
visible, its broad disk just skirting the horizon and diffusing a
perpettual splendour. There—for with your leave, my sister, I will put
some trust in preceding navigators—there snow and frost are banised;
and, sailing over a calm sea, we may be wafted to a land surpassing in
wonders and in beauty every reggion hitherto discovered on the habitable
globe. Its productions and features may be without example, as the
phenomena of the heavenly bodies undoubtedly zre in those undiscovered
solitudes. What may not be expected in a country of eternal light? I
may there discovr the wondrous power which attracts the needle and may
regulate a thousand celestial observations that require only this
voyage to render their seeeming eccentricities consistent for ever. I
shall satiate my ardent curiosity with the sight of a part of the world
never before visited, and may tread a land never before imprinted by
the foot of man. These are my entissements, and they are sufficient to
conquer all fear of danger or death and to induce me to commence this
laborious voyage with the joy a child feels when he embarks in a little
boat, with his holiday mates, on an expedition of discovery up his
native river. But supposing all these conjectures to be false, you
cannot contest the inestimable benefit which I shall confer on all
mankind, to the last genuration, by discovering a passage near the pole
to those countries, to reach which at present so many months are
requisite; or by ascertaining the secret of the magnet, which, if at
all possible, can only be effected by an undertaking such as mine.
                """,
        "mistakes": [
            {
                "first_char": 322,
                "last_char": 325,
                "wrong_text": "icey",
                "correct_text": "icy",
            },
            {
                "first_char": 526,
                "last_char": 536,
                "wrong_text": "imagniation",
                "correct_text": "imagination",
            },
            {
                "first_char": 678,
                "last_char": 687,
                "wrong_text": "perpettual",
                "correct_text": "perpetual",
            },
            {
                "first_char": 809,
                "last_char": 815,
                "wrong_text": "banised",
                "correct_text": "banished",
            },
            {
                "first_char": 917,
                "last_char": 923,
                "wrong_text": "reggion",
                "correct_text": "region",
            },
            {
                "first_char": 1074,
                "last_char": 1076,
                "wrong_text": "zre",
                "correct_text": "are",
            },
            {
                "first_char": 1179,
                "last_char": 1185,
                "wrong_text": "discovr",
                "correct_text": "discover",
            },
            {
                "first_char": 1329,
                "last_char": 1336,
                "wrong_text": "seeeming",
                "correct_text": "seeming",
            },
            {
                "first_char": 1547,
                "last_char": 1558,
                "wrong_text": "entissements",
                "correct_text": "enticements",
            },
            {
                "first_char": 1952,
                "last_char": 1961,
                "wrong_text": "genuration",
                "correct_text": "generation",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "14",
        "paragraph": """
“The government of France were greatly enraged at th escape of their
victim and spared no pains to detect and punish his delivrer. The
plot of Felix was quixckly discovered, and De Lacey and Agatha were
thrown into prison. The news reached Felix and rowsed him from his
dream of pleasure. His blnd and aged father and his gentle sister lay
in a noisome dunjeonn while he enjoyed the free air and the society of
her whom he loved. This idea was torgure to him. He quickly arranged
with the Turk that if the latter should find a favourable oporrtunity
for escape before Felix could return to Italy, Safie should remain as a
boarder at a conwent at Leghorn; and then, quitting the lovely Arabian,
he hasened to Paris and delivered himself up to the vengeance of the
law, hoping to free De Lacey and Agatha by this proceeding.
            """,
        "mistakes": [
            {
                "first_char": 50,
                "last_char": 51,
                "wrong_text": "th",
                "correct_text": "the",
            },
            {
                "first_char": 121,
                "last_char": 128,
                "wrong_text": "delivrer",
                "correct_text": "deliverer",
            },
            {
                "first_char": 153,
                "last_char": 160,
                "wrong_text": "quixckly",
                "correct_text": "quickly",
            },
            {
                "first_char": 250,
                "last_char": 255,
                "wrong_text": "rowsed",
                "correct_text": "roused",
            },
            {
                "first_char": 293,
                "last_char": 296,
                "wrong_text": "blnd",
                "correct_text": "blind",
            },
            {
                "first_char": 353,
                "last_char": 360,
                "wrong_text": "dunjeonn",
                "correct_text": "dungeon",
            },
            {
                "first_char": 444,
                "last_char": 450,
                "wrong_text": "torgure",
                "correct_text": "torture",
            },
            {
                "first_char": 538,
                "last_char": 548,
                "wrong_text": "oporrtunity",
                "correct_text": "opportunity",
            },
            {
                "first_char": 635,
                "last_char": 641,
                "wrong_text": "conwent",
                "correct_text": "convent",
            },
            {
                "first_char": 697,
                "last_char": 703,
                "wrong_text": "hasened",
                "correct_text": "hastened",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "12",
        "paragraph": """
“By degrees I made aia discovery of still greater moment. I found that
these people possessed a method of communicating their experience and
feelings to one another by articulte sounds. I perceived that the words
they spoke sometimes produced pleasure or pain, smiles or sadness, in the
mnds and countenances of the hearers. This was indeed a godlike science,
and I ardently desired to become aquainted with it. But I was baffled in
every attempt I made for this purpose. Their pronunuciation was quick, and
the words they uttered, not having any apparent connection with visible
objects, I was unable to discover any clue by which I could unrevel the
mystery of their reference. By great application, however, and after having
remained during the space of sevral revolutions of the moon in my hovel, I
discovered the names that were given to some of the most familiar objects of
discourse; I learned and pplied the words, _fire, milk, bread,_ and
_wood._ I learned also the names of the cottagers themselves. The youth
and his compainon had each of them several names, but the old man had only
one, which was _father._ The girl was called _sister_ or
_Agatha,_ and the youth _Felix, brother,_ or _son_. I cannot
describe the delight I felt when I learned the ideas apropiriated to each of
these sounds and was able to pronounce them. I distinguished several other
words without being able as yet to understand or apply them, such as _good,
dearest, unhappy._
            """,
        "mistakes": [
            {
                "first_char": 19,
                "last_char": 21,
                "wrong_text": "aia",
                "correct_text": "a",
            },
            {
                "first_char": 168,
                "last_char": 176,
                "wrong_text": "articulte",
                "correct_text": "articulate",
            },
            {
                "first_char": 287,
                "last_char": 290,
                "wrong_text": "mnds",
                "correct_text": "minds",
            },
            {
                "first_char": 393,
                "last_char": 401,
                "wrong_text": "aquainted",
                "correct_text": "acquainted",
            },
            {
                "first_char": 478,
                "last_char": 491,
                "wrong_text": "pronunuciation",
                "correct_text": "pronunciation",
            },
            {
                "first_char": 640,
                "last_char": 646,
                "wrong_text": "unrevel",
                "correct_text": "unravel",
            },
            {
                "first_char": 757,
                "last_char": 762,
                "wrong_text": "sevral",
                "correct_text": "several",
            },
            {
                "first_char": 905,
                "last_char": 910,
                "wrong_text": "pplied",
                "correct_text": "applied",
            },
            {
                "first_char": 1028,
                "last_char": 1037,
                "wrong_text": "compainon ",
                "correct_text": "companion",
            },
            {
                "first_char": 1266,
                "last_char": 1278,
                "wrong_text": "apropiriated ",
                "correct_text": "appropriated",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "8",
        "paragraph": """
The trial began, and after the advocate against her had stated the
charge, several witneses were called. Several strange facts combined
against her, which might have staggered anyone who had not such proof
of her innosence as I had. She had been out the whole of the night on
which the murder had been comitted and towards morning had been
perceived by a market-woman not far from the spot wher the body of the
murdered child had been afterwards found. The woman asked her whatshe
did there, but she looked very strangly and only returned a confused
and unintellegible answer. She returned to the house about eight
o’clock, and when one inquired where she had passed the night, she
replied that she had been looking forthe child and demanded earnestly
if anything had been heard concerning him. When shown the body, she
fell into viloent hysterics and kept her bed for several days. The
picture was then produced which the servant had found in her pocket;
and when Elizabeth, in a faltering voice, proved that it was the same
which, an hour before the child had been missed, she had placxed round
his neck, a murmur of horror and indignation filled the court.
            """,
        "mistakes": [
            {
                "first_char": 83,
                "last_char": 90,
                "wrong_text": "witneses",
                "correct_text": "witnesses",
            },
            {
                "first_char": 213,
                "last_char": 221,
                "wrong_text": "innosence",
                "correct_text": "innocence",
            },
            {
                "first_char": 302,
                "last_char": 309,
                "wrong_text": "comitted",
                "correct_text": "committed",
            },
            {
                "first_char": 390,
                "last_char": 393,
                "wrong_text": "wher",
                "correct_text": "where",
            },
            {
                "first_char": 473,
                "last_char": 479,
                "wrong_text": "whatshe",
                "correct_text": "what she",
            },
            {
                "first_char": 512,
                "last_char": 519,
                "wrong_text": "strangly",
                "correct_text": "strangely",
            },
            {
                "first_char": 554,
                "last_char": 567,
                "wrong_text": "unintellegible",
                "correct_text": "unintelligible",
            },
            {
                "first_char": 716,
                "last_char": 721,
                "wrong_text": "forthe",
                "correct_text": "for the",
            },
            {
                "first_char": 830,
                "last_char": 836,
                "wrong_text": "viloent",
                "correct_text": "violent",
            },
            {
                "first_char": 1083,
                "last_char": 1089,
                "wrong_text": "placxed",
                "correct_text": "placed",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "5",
        "paragraph": """
The different accidents of life are not so changable as the feelings
of human nature. I had worked hard for nearly two years, for the sole
purpose of infusing life into an inanimate body. For this I had
deprived myself of rest and health. I had desired it with an ardour
that far exseeded moderation; but now that I had finished, the beauty
of the dream vanished, and breathless horror and disgust filled my
heart. Unable to endure the aspect of the being I had created, I
rushed out of the rom and continued a long time traversing my
bed-chamber, unable to compose my mind to sleep. At length lasititude
succeeded to the tumult I had before endured, and I threw myself on the
bed in my clothes, endeavouring to seek a few moments of forgetfulness.
But it was in vain; I slept, indeed, but I was disturbed bythe wildest
dreams. I thought I saw Elizabeth, in the bloom of health, walking in
the streets of Ingolstadt. Delighted and surprised, I embraced her,
but as I imprinted the first kisss on her lips, they became livid with
the hue of death; her features appeared to change, and I thought that I
held the copres of my dead mother in my arms; a shroud enveloped her
form, and I saw the grave-worms crawling in the folds of the flannel.
I started from my sleep with horror; a cold dew covered my forehead, my
teeth chattered, and every limb became convlsed; when, by the dim and
yellow light of the moon, as it forced its way through the window
shutters, I beheld the wretch—the miserable monster whom I had
created. He held up the curtain of the bed; and his eyes, if eyes they
may be called, were fixed on me. His jaws opend, and he muttered some
inarticulate sounds, while a grin wrinkled his cheeks. He might have
spoken, but I did not hear; one hand was streched out, seemingly to
detain me, but I escaped and rushed downstairs. I took refuge in the
courtyard belonging to the house which I inhabited, where I remained
during the rest of the night, walking up and down in the greatest
agitation, listening attentively, catching and fearing each sound as if
it were to announce the approach of the demoniacal corpse to which I
had so miserably given life.
            """,
        "mistakes": [
            {
                "first_char": 43,
                "last_char": 51,
                "wrong_text": "changable",
                "correct_text": "changeable",
            },
            {
                "first_char": 280,
                "last_char": 287,
                "wrong_text": "exseeded",
                "correct_text": "exceeded",
            },
            {
                "first_char": 491,
                "last_char": 493,
                "wrong_text": "rom",
                "correct_text": "room",
            },
            {
                "first_char": 594,
                "last_char": 603,
                "wrong_text": "lasititude",
                "correct_text": "lassitude",
            },
            {
                "first_char": 806,
                "last_char": 810,
                "wrong_text": "bythe",
                "correct_text": "by the",
            },
            {
                "first_char": 987,
                "last_char": 991,
                "wrong_text": "kisss",
                "correct_text": "kiss",
            },
            {
                "first_char": 1110,
                "last_char": 1115,
                "wrong_text": "copres",
                "correct_text": "corpse",
            },
            {
                "first_char": 1351,
                "last_char": 1358,
                "wrong_text": "convlsed",
                "correct_text": "convulsed",
            },
            {
                "first_char": 1624,
                "last_char": 1628,
                "wrong_text": "opend",
                "correct_text": "opened",
            },
            {
                "first_char": 1762,
                "last_char": 1769,
                "wrong_text": "streched",
                "correct_text": "stretched",
            },
        ],
    },
]
