"""
Paragraphs for Frankenstein snippets taken from
Chapter 15
Chapter 19
Chapter 6
Chapter 13
Chapter 17

Paragraphs for Cthulhu snippets taken from
Section 2.2
Section 2.3
Section 3.1
Section 3.2
Section 3.3


"""

evaluation_dataset = [
    {
        "source": "frankenstein",
        "chapter": "15",
        "paragraph": """
“The volume of _Plutarch’s Lives_ which I possessed contained the
histories the first founders of the ancient republics. This book
had a far different effect upon me from the _Sorrows of Werter_. I
from Werter’s imaginations despondency and gloom, but Plutarch
taught me high thoughts; he elevated me above the wretched of my
own reflections, to admire and love the heroes of past ages. Many
things I read my understanding and experience. I had a very
confused knowledge of, wide extents of country, mighty rivers,
and boundless seas. But I was perfectly unacquainted with towns and
large of men. The cottage of my protectors had been the
only school in which I had studied human nature, but this book
developed new and mightier scenes of action. I read of men concerned
in public affairs, governing or their species. I felt the
greatest ardour for virtue rise within me, and abhorrence for vice, as
far as understood the signification of those terms, relative as they
were, as I applied them, to pleasure and pain alone. Induced by these
feelings, I was of course led to admire peaceable lawgivers, Numa,
Solon, and Lycurgus, in preference to Romulus and Theseus. The
patriarchal of my protectors caused these impressions to take a
firm hold on my mind; perhaps, if my first introduction to humanity had
been by a young soldier, burning for glory and slaughter, I should
have been imbued with different sensations.
                """,
        "mistakes": [
            {
                "first_char": 66,
                "last_char": 78,
                "wrong_text": "histories the",
                "correct_text": "histories of the ",
            },
            {
                "first_char": 196,
                "last_char": 201,
                "wrong_text": "I from",
                "correct_text": "I learned from",
            },
            {
                "first_char": 311,
                "last_char": 321,
                "wrong_text": "wretched of",
                "correct_text": "wretched sphere of",
            },
            {
                "first_char": 401,
                "last_char": 407,
                "wrong_text": "read my",
                "correct_text": "read surpassed my",
            },
            {
                "first_char": 471,
                "last_char": 478,
                "wrong_text": "of, wide",
                "correct_text": "of kingdoms, wide",
            },
            {
                "first_char": 583,
                "last_char": 590,
                "wrong_text": "large of",
                "correct_text": "large assemblages of",
            },
            {
                "first_char": 800,
                "last_char": 807,
                "wrong_text": "or their",
                "correct_text": "or massacring their",
            },
            {
                "first_char": 904,
                "last_char": 916,
                "wrong_text": "as understood",
                "correct_text": "as I understood",
            },
            {
                "first_char": 1169,
                "last_char": 1182,
                "wrong_text": "patriarchal of",
                "correct_text": "patriarchal lives of",
            },
            {
                "first_char": 1305,
                "last_char": 1311,
                "wrong_text": "been by",
                "correct_text": "been made by",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "19",
        "paragraph": """
We had scarcely visited the various lakes of Cumberland and Westmorland
and conceived an affection for some the inhabitants when the period
of our appointment with our Scotch friend, and we left them
to travel on. For my own part I not sorry. I had now neglected my
promise for some time, and I feared the effects of the dæmon’s
disappointment. He might in Switzerland and wreak his vengeance
on my relatives. This idea pursued me and tormented me at every moment
from which I might otherwise have snatched and peace. I waited
for my letters with feverish; if they were delayed I was
miserable and overcome by a thousand fears; and when they arrived and I
saw the of Elizabeth or my father, I hardly dared to
read and my fate. Sometimes I thought that the fiend
followed me and might expedite my by murdering my companion.
When these thoughts possessed me, I would not quit Henry for a moment,
but followed him as his shadow, to protect him from the fancied rage of
his. I felt as if I had committed some great crime, the
consciousness of which haunted me. I was guiltless, but I had indeed
drawn down a horrible curse upon my head, as mortal as that of crime.
                """,
        "mistakes": [
            {
                "first_char": 99,
                "last_char": 110,
                "wrong_text": "for some the",
                "correct_text": "for some of the",
            },
            {
                "first_char": 175,
                "last_char": 185,
                "wrong_text": "friend, and",
                "correct_text": "friend approached, and",
            },
            {
                "first_char": 230,
                "last_char": 234,
                "wrong_text": "I not",
                "correct_text": "I was not",
            },
            {
                "first_char": 348,
                "last_char": 355,
                "wrong_text": "might in",
                "correct_text": "might remain in",
            },
            {
                "first_char": 498,
                "last_char": 509,
                "wrong_text": "snatched and",
                "correct_text": "snatched repose and",
            },
            {
                "first_char": 547,
                "last_char": 558,
                "wrong_text": "feverish; if",
                "correct_text": "feverish impatience; if",
            },
            {
                "first_char": 660,
                "last_char": 665,
                "wrong_text": "the of",
                "correct_text": "the superscription of",
            },
            {
                "first_char": 714,
                "last_char": 719,
                "wrong_text": "and my",
                "correct_text": "and ascertain my",
            },
            {
                "first_char": 793,
                "last_char": 797,
                "wrong_text": "my by",
                "correct_text": "my remissness by",
            },
            {
                "first_char": 966,
                "last_char": 971,
                "wrong_text": "his. I",
                "correct_text": "his destroyer. I",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "6",
        "paragraph": """
“Little alteration, except the growth of our dear children, has taken
place you left us. The blue lake and snow-clad mountains—they
never change; and I think our placid home and our contented hearts are
regulated by the same immutable laws. My trifling take up
my time and amuse me, and I am rewarded for any exertions by seeing
none but happy, kind faces me. Since you left us, but one
change has taken place in our little household. Do you remember on
what occasion Justine Moritz entered our family? Probably you not;
I will relate her history, therefore in a few words. Madame Moritz,
her mother, was a widow four children, of whom Justine was the
third. This girl had always been the favourite her father, but
through a strange perversity, her could not endure her, and
after the death of M. Moritz, treated her very ill. My aunt observed
this, and when was twelve years of age, prevailed on her mother
to allow her to live at our house. The republican institutions of our
country have produced simpler and happier than those which
prevail in the great monarchies that surround it. Hence there is less
distinction between the several classes of its inhabitants; and the
lower, being neither so poor nor so despised, their manners are
more refined and moral. A servant in Geneva does not mean the same
thing as a servant in France and England. Justine, thus received in
our family, learned the duties of a servant, a condition which, in our
fortunate country, does not include the idea of ignorance and a
sacrifice of the dignity of a human being.
                """,
        "mistakes": [
            {
                "first_char": 70,
                "last_char": 78,
                "wrong_text": "place you",
                "correct_text": "place since you",
            },
            {
                "first_char": 244,
                "last_char": 256,
                "wrong_text": "trifling take",
                "correct_text": "trifling occupations take",
            },
            {
                "first_char": 350,
                "last_char": 358,
                "wrong_text": "faces me.",
                "correct_text": "faces around me.",
            },
            {
                "first_char": 512,
                "last_char": 519,
                "wrong_text": "you not;",
                "correct_text": "you do not;",
            },
            {
                "first_char": 607,
                "last_char": 616,
                "wrong_text": "widow four",
                "correct_text": "widow with four",
            },
            {
                "first_char": 689,
                "last_char": 701,
                "wrong_text": "favourite her",
                "correct_text": "favourite of her",
            },
            {
                "first_char": 745,
                "last_char": 753,
                "wrong_text": "her could",
                "correct_text": "her mother could",
            },
            {
                "first_char": 854,
                "last_char": 861,
                "wrong_text": "when was",
                "correct_text": "when Justine was",
            },
            {
                "first_char": 1012,
                "last_char": 1023,
                "wrong_text": "happier than",
                "correct_text": "happier manners than",
            },
            {
                "first_char": 1175,
                "last_char": 1186,
                "wrong_text": "lower, being",
                "correct_text": "lower orders, being",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "13",
        "paragraph": """
“I soon perceived that although the stranger uttered articulate sounds
and appeared to have a of her own, she was neither understood
by nor herself understood the cottagers. They many signs which I
did not comprehend, but I saw that her presence diffused gladness
through the cottage, dispelling their as the sun dissipates the
morning mists. Felix seemed peculiarly and with smiles of
delight welcomed his Arabian. Agatha, the ever-gentle Agatha, kissed
the hands of lovely stranger, and pointing to her brother, made
signs which appeared to to mean that he had been sorrowful until she
came. Some hours passed thus, while they, by their countenances,
expressed joy, the cause of which I not comprehend. Presently I
found, by the frequent of some sound which the stranger
repeated after them, that she was endeavouring to learn their language;
and the instantly occurred to me that I should make use of the
same instructions the same end. The stranger learned about twenty
words at the first lesson; most of them, indeed, were those which I had
before understood, but I profited by the others.
                """,
        "mistakes": [
            {
                "first_char": 92,
                "last_char": 95,
                "wrong_text": "a of",
                "correct_text": "a language of",
            },
            {
                "first_char": 174,
                "last_char": 182,
                "wrong_text": "They many",
                "correct_text": "They made many",
            },
            {
                "first_char": 296,
                "last_char": 303,
                "wrong_text": "their as",
                "correct_text": "their sorrow as",
            },
            {
                "first_char": 356,
                "last_char": 369,
                "wrong_text": "peculiarly and",
                "correct_text": "peculiarly happy and",
            },
            {
                "first_char": 465,
                "last_char": 473,
                "wrong_text": "of lovely",
                "correct_text": "of the lovely",
            },
            {
                "first_char": 540,
                "last_char": 544,
                "wrong_text": "to to",
                "correct_text": "to me to",
            },
            {
                "first_char": 687,
                "last_char": 691,
                "wrong_text": "I not",
                "correct_text": "I did not",
            },
            {
                "first_char": 731,
                "last_char": 741,
                "wrong_text": "frequent of",
                "correct_text": "frequent recurrence of",
            },
            {
                "first_char": 849,
                "last_char": 861,
                "wrong_text": "the instantly",
                "correct_text": "the idea instantly",
            },
            {
                "first_char": 913,
                "last_char": 928,
                "wrong_text": "instructions the",
                "correct_text": "instructions to the",
            },
        ],
    },
    {
        "source": "frankenstein",
        "chapter": "17",
        "paragraph": """
“You swear,” I said, “to be harmless; but have you not
already shown a degree malice that should reasonably make me distrust
you? May not even this be a feint that will increase your triumph by
affording a wider for your revenge?”

“How is this? I must not be trifled with, and I demand an answer. If
I have no and no affections, hatred and vice must be my portion;
the love of another will destroy the cause of my crimes, and I shall
become a thing of whose existence everyone be ignorant. My vices
are the children of a forced solitude that I abhor, and my virtues will
necessarily arise when I live in communion an equal. I shall feel
the affections of a sensitive being and become linked to the chain of
existence and events from which am now excluded.”

I paused some time to reflect on he had related and the various
arguments which he had employed. I thought of the promise of virtues which
he had displayed on the opening of his existence and the subsequent blight
of all kindly feeling by the loathing and scorn which his protectors had
manifested towards. His power and threats were not omitted in my
calculations; a creature who could exist in the ice-caves of the glaciers
and hide himself pursuit among the ridges of inaccessible precipices
was a being possessing faculties it would be vain to cope with. After a
long pause reflection I concluded that the justice due both to him and
my fellow creatures demanded of me that I should comply with his request.
Turning to him, therefore, I said,
            """,
        "mistakes": [
            {
                "first_char": 71,
                "last_char": 83,
                "wrong_text": "degree malice",
                "correct_text": "degree of malice",
            },
            {
                "first_char": 206,
                "last_char": 214,
                "wrong_text": "wider for",
                "correct_text": "wider scope for",
            },
            {
                "first_char": 308,
                "last_char": 313,
                "wrong_text": "no and",
                "correct_text": "no ties and",
            },
            {
                "first_char": 469,
                "last_char": 479,
                "wrong_text": "everyone be",
                "correct_text": "everyone will be",
            },
            {
                "first_char": 605,
                "last_char": 616,
                "wrong_text": "communion an",
                "correct_text": "communion with an",
            },
            {
                "first_char": 734,
                "last_char": 741,
                "wrong_text": "which am",
                "correct_text": "which I am",
            },
            {
                "first_char": 789,
                "last_char": 793,
                "wrong_text": "on he",
                "correct_text": "on all he",
            },
            {
                "first_char": 1057,
                "last_char": 1068,
                "wrong_text": "towards. His",
                "correct_text": "towards him. His",
            },
            {
                "first_char": 1194,
                "last_char": 1208,
                "wrong_text": "himself pursuit",
                "correct_text": "himself from pursuit",
            },
            {
                "first_char": 1331,
                "last_char": 1346,
                "wrong_text": "pause reflection",
                "correct_text": "pause of reflection",
            },
        ],
    },
]
