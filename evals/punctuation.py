"""
The best engineering practice here would be to store this as a JSON file.
That would allow for greatest portability between systems and languages.
However, since I plan to use this on one system, with one language, these
benefits don't apply. In addition, the porting of many-line
text blocks with particular characters in them to JSON makes them less
human-readable. For now we'll stick with Python.

Paragraphs for punctuation examples taken from
Chapter 9
Chapter 10
Chapter 18
Chapter 20
Chapter 24

With the help of randomized chapter order
[14, 12, 8, 5, 3, 23, 4, 2, 21, 24, 20, 18, 9, 10, 7, 1, 16, 22, 15, 19, 6, 13, 17, 11]
"""

evaluation_dataset = [
    {
        "source": "Frankenstein",
        "chapter": "9",
        "paragraph": """
“When I reflect, my dear cousin, said she, “on the miserable death of
Justine Moritz, I no longer see the world and its works as they before
appeared to me Before, I looked upon the accounts of vice and
injustice that I read in books or heard from others as tales of ancient
days or imaginary evils;; at least they were remote and more familiar to
reason than to the imagination; but now misery has come home, and men
appear to me as monsters thirsting for each others blood. Yet I am
certainly unjust. Everybody believed that poor girl to be guilty. and
if she could have committed the crime for which she suffered, assuredly
she would have been the most depraved of human creatures. For the sake
of a few jewels, to have murdered the son of her benefactor and friend,
a child whom she had nursed from its birth and appeared to love as if
it had been her own! I could not consent to the death of any human
being< but certainly I should have thought such a creature unfit to
remain in the society of men. But she was innocent. I know, I feel
she was innocent; you are of the (same opinion, and that confirms me.
Alas@ Victor, when falsehood can look so like the truth, who can
assure themselves of certain happiness? I feel as if I were walking on
the edge of a precipice, towards which thousands are crowding and
endeavouring to plunge me into the abyss William and Justine were
assassinated, and the murderer escapes; he walks about the world free,
and perhaps respected. But even if I were condemned to suffer on the
scaffold for the same crimes, I would not change places with such a
wretch.”
                """,
        "mistakes": [
            {
                "first_char": 25,
                "last_char": 36,
                "wrong_text": 'cousin, said',
                "correct_text": 'cousin," said',
            },
            {
                "first_char": 153,
                "last_char": 162,
                "wrong_text": "me Before,",
                "correct_text": "me. Before,",
            },
            {
                "first_char": 293,
                "last_char": 302,
                "wrong_text": "evils;; at",
                "correct_text": "evils; at",
            },
            {
                "first_char": 457,
                "last_char": 467,
                "wrong_text": "each others",
                "correct_text": "each other's",
            },
            {
                "first_char": 543,
                "last_char": 553,
                "wrong_text": "guilty. and",
                "correct_text": "guilty; and",
            },
            {
                "first_char": 807,
                "last_char": 816,
                "wrong_text": "birth and ",
                "correct_text": "birth, and ",
            },
            {
                "first_char": 907,
                "last_char": 916,
                "wrong_text": "being< but",
                "correct_text": "being, but",
            },
            {
                "first_char": 1071,
                "last_char": 1079,
                "wrong_text": "the (same",
                "correct_text": "the same",
            },
            {
                "first_char": 1112,
                "last_char": 1124,
                "wrong_text": "Alas@ Victor,",
                "correct_text": "Alas! Victor,",
            },
            {
                "first_char": 1349,
                "last_char": 1361,
                "wrong_text": "abyss William",
                "correct_text": "abyss. William",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "10",
        "paragraph": """
The ascent is precipitous but the path is cut into continual and short
windings, which enable you to surmount the perpendicularity of the
mountain. It is a scene terrifically, desolate. In a thousand spots
the traces of the winter avalanche may be perceived, where trees lie
broken and strewed? on the ground, some entirely destroyed, others bent,
leaning upon the jutting rocks of the mountain or transversely upon
other trees. The path, as you ascend higher, is intersected by ravines
of snow. down which stones continually roll from above; one of them is
particularly dangerous, as the slightest sound, [] such as even speaking
in a loud voice, produces a concussion of air sufficient to draw
destruction upon the head of the speaker.. The pines are not tall or
luxuriant, but they are sombre and add an air of severity to the scene.
I looked on the valley beneath: vast mists were rising from the rivers
which ran through it and curling in thick wreaths around the opposite
mountains, whose summits were hid in the uniform clouds, while rain
poured from the dark sky' and added to the melancholy impression I
received from the objects around me. Alas! Why does man boast of
sensibilities superior to those apparent in the brute; it only renders
them more necessary beings> If our impulses were confined to hunger,
thirst, and desire, we might be nearly free; but now we are moved by
every wind that blows and a chance word or scene that that word may
convey to us
                """,
        "mistakes": [
            {
                "first_char": 14,
                "last_char": 28,
                "wrong_text": "precipitous but",
                "correct_text": "precipitous, but",
            },
            {
                "first_char": 162,
                "last_char": 184,
                "wrong_text": "terrifically, desolate.",
                "correct_text": "terrifically desolate.",
            },
            {
                "first_char": 286,
                "last_char": 297,
                "wrong_text": "strewed? on ",
                "correct_text": "strewed on",
            },
            {
                "first_char": 490,
                "last_char": 499,
                "wrong_text": "snow. down",
                "correct_text": "snow, down",
            },
            {
                "first_char": 599,
                "last_char": 612,
                "wrong_text": "sound, [] such",
                "correct_text": "sound, such",
            },
            {
                "first_char": 729,
                "last_char": 742,
                "wrong_text": "speaker.. The ",
                "correct_text": "speaker. The ",
            },
            {
                "first_char": 860,
                "last_char": 873,
                "wrong_text": "beneath: vast ",
                "correct_text": "beneath; vast ",
            },
            {
                "first_char": 1067,
                "last_char": 1074,
                "wrong_text": "sky' and",
                "correct_text": "sky and",
            },
            {
                "first_char": 1269,
                "last_char": 1278,
                "wrong_text": "beings> If",
                "correct_text": "beings. If",
            },
            {
                "first_char": 1462,
                "last_char": 1466,
                "wrong_text": "to us",
                "correct_text": "to us.",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "18",
        "paragraph": """
We travelled at, the time of the vintage and heard the song of the labourers
as we glided down the stream. Even I, depressed in mind, and my spirits
continually agitated by gloomy feelings, even I was pleased. I lay at the
bottom of the boat,, and as I gazed on the cloudless blue sky, I seemed to
drink in a tranquillity to which I had long been a stranger. And if these
were my sensations, who can describe those of Henry. He felt as if he had
been transported to Fairy-land and enjoyed a happiness seldom tasted by
man. “I have seen,” he said, the most beautiful scenes
of my own country; I have visited the lakes, of Lucerne and Uri, where the
snowy mountains descend almost perpendicularly to the water, casting black.
and impenetrable shades, which would cause a gloomy and mournful appearance
were it not for the most verdant islands that relieve the eye by their gay
appearance;; I have seen this lake agitated by a tempest, when the wind tore
up whirlwinds of water and gave you an idea of what the water-spout must be
on the great ocean; and the waves dash with fury the base of the mountain,
where the priest and his mistress!! were overwhelmed by an avalanche and
where their dying voices are still said to be heard amid the pauses of the
nightly wind; I have seen the mountains of La Valais, and the Pays de Vaud;
but this country, Victor, pleases me more than all those wonders The
mountains of Switzerland are more majestic and strange, but there is a
charm in the banks of this divine river that I never before saw equalled.
Look at that castle which overhangs yon precipice; and that also on the
island, almost concealed amongst the foliage of those lovely trees; and now
that group of labourers coming from among their vines; and that village
half hid in the recess of the mountain Oh, surely the spirit that inhabits
and guards this place has a soul more in harmony with man than those who
pile the glacier or retire to the inaccessible peaks of the mountains of
our own country.”
                """,
        "mistakes": [
            {
                "first_char": 13,
                "last_char": 20,
                "wrong_text": "at, the ",
                "correct_text": "at the ",
            },
            {
                "first_char": 237,
                "last_char": 246,
                "wrong_text": "boat,, and",
                "correct_text": "boat, and",
            },
            {
                "first_char": 418,
                "last_char": 426,
                "wrong_text": "Henry. He",
                "correct_text": "Henry? He",
            },
            {
                "first_char": 541,
                "last_char": 549,
                "wrong_text": "said, the",
                "correct_text": "said, “the",
            },
            {
                "first_char": 611,
                "last_char": 620,
                "wrong_text": "lakes, of ",
                "correct_text": "lakes of ",
            },
            {
                "first_char": 717,
                "last_char": 722,
                "wrong_text": "black.",
                "correct_text": "black",
            },
            {
                "first_char": 875,
                "last_char": 888,
                "wrong_text": "appearance;; I",
                "correct_text": "appearance; I",
            },
            {
                "first_char": 1128,
                "last_char": 1142,
                "wrong_text": "mistress!! were",
                "correct_text": "mistress were",
            },
            {
                "first_char": 1384,
                "last_char": 1394,
                "wrong_text": "wonders The",
                "correct_text": "wonders. The",
            },
            {
                "first_char": 1791,
                "last_char": 1802,
                "wrong_text": "mountain Oh,",
                "correct_text": "mountain. Oh,",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "20",
        "paragraph": """
I do not know how long I remained in this situation, but when I awoke I
found that the sun had already mounted considerably The wind was high, and
the waves continually threatened the safety of my little skiff. I found
that the wind was northeast; and must have driven me far from the coast from
which I had embarked. I endeav-oured to change my course but quickly found
that if I again made the attempt the boat would be instantly filled with
water? Thus situated, my only resource was to drive before the wind. I
confess that I-felt a few sensations of terror. I had no compass with me
and was so slenderly acquainted with the geography of this part of the
world that the sun was of little benefit to me.. I might be driven into the
wide Atlantic and feel all the tortures of starvation or be swallowed up in
the immeasurable waters that roared and buffeted around me, I had already
been out many hours and felt the torment of a burning thirst, a prelude to
my other sufferings. I looked on the heavens, which were covered by clouds
that flew before the wind only to be replaced by others; I looked upon the
sea; it was to be my grave. “Fiend, I exclaimed, “your
task is already fulfilled!” I thought of Elizabeth, of my father, and
of Clerval—all left behind, on whom the monster might satisfy his
sanguinary and merciless passions. This idea plunged me into a reverie so
despairing and frightful that even now, when the scene is on the point of
closing before me for ever', I shudder to reflect on it.
                """,
        "mistakes": [
            {
                "first_char": 111,
                "last_char": 126,
                "wrong_text": "considerably The",
                "correct_text": "considerably. The",
            },
            {
                "first_char": 237,
                "last_char": 250,
                "wrong_text": "northeast; and",
                "correct_text": "northeast and",
            },
            {
                "first_char": 320,
                "last_char": 331,
                "wrong_text": "endeav-oured",
                "correct_text": "endeavoured",
            },
            {
                "first_char": 444,
                "last_char": 454,
                "wrong_text": "water? Thus",
                "correct_text": "water. Thus",
            },
            {
                "first_char": 528,
                "last_char": 533,
                "wrong_text": "I-felt",
                "correct_text": "I felt",
            },
            {
                "first_char": 703,
                "last_char": 708,
                "wrong_text": "me.. I",
                "correct_text": "me. I",
            },
            {
                "first_char": 867,
                "last_char": 871,
                "wrong_text": "me, I",
                "correct_text": "me. I",
            },
            {
                "first_char": 1056,
                "last_char": 1064,
                "wrong_text": "wind only",
                "correct_text": "wind, only",
            },
            {
                "first_char": 1138,
                "last_char": 1146,
                "wrong_text": "“Fiend, I",
                "correct_text": "“Fiend,” I",
            },
            {
                "first_char": 1471,
                "last_char": 1478,
                "wrong_text": "ever', I",
                "correct_text": "ever, I",
            },
        ],
    },
    {
        "source": "Frankenstein",
        "chapter": "24",
        "paragraph": """
Amidst the wilds of Tartary and Russia, although he still evaded me, I
have ever, followed in his track. Sometimes the peasants, scared by
this horrid apparition, informed me of his path sometimes he himself,
who feared that if I lost all trace of him! I should despair and die,
left some mark to guide me The snows descended on my head, and I saw
the print of his huge step on the white plain. To you first entering
on life, to whom care is, new and agony unknown, how can you understand
what I have felt and still feel? Cold? want, and fatigue were the
least pains which I was destined to endure; I was cursed by some devil
and carried about with me my eternal hell; yet still a spirit of good
followed and... directed my steps and when I most murmured would suddenly
extricate me from seemingly insurmountable difficulties. Sometimes,
when nature, overcome by hunger; sank under the exhaustion, a repast
was prepared for me in the desert that restored and inspirited me. The
fare was, indeed, coarse, such as the-peasants of the country ate, but
I will not doubt that it was set there by the spirits that I had
invoked to aid me. Often, when all was dry, the heavens cloudless, and
I was parched by thirst< a slight cloud would bedim the sky, shed the
few drops that revived me, and vanish.
                """,
        "mistakes": [
            {
                "first_char": 76,
                "last_char": 89,
                "wrong_text": "ever, followed",
                "correct_text": "ever followed",
            },
            {
                "first_char": 182,
                "last_char": 195,
                "wrong_text": "path sometimes",
                "correct_text": "path; sometimes",
            },
            {
                "first_char": 248,
                "last_char": 253,
                "wrong_text": "him! I",
                "correct_text": "him I",
            },
            {
                "first_char": 303,
                "last_char": 308,
                "wrong_text": "me The",
                "correct_text": "me. The",
            },
            {
                "first_char": 439,
                "last_char": 445,
                "wrong_text": "is, new",
                "correct_text": "is new",
            },
            {
                "first_char": 522,
                "last_char": 532,
                "wrong_text": "Cold? want,",
                "correct_text": "Cold, want,",
            },
            {
                "first_char": 705,
                "last_char": 719,
                "wrong_text": "and... directed",
                "correct_text": "and directed",
            },
            {
                "first_char": 863,
                "last_char": 874,
                "wrong_text": "hunger; sank",
                "correct_text": "hunger, sank",
            },
            {
                "first_char": 1012,
                "last_char": 1023,
                "wrong_text": "the-peasants",
                "correct_text": "the peasants",
            },
            {
                "first_char": 1202,
                "last_char": 1210,
                "wrong_text": "thirst< a",
                "correct_text": "thirst, a",
            },
        ],
    },
]
