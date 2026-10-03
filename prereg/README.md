# Pre-registered: is "receipt" structural or topical? (window 7-13 Oct 2026)

Fixed on 3 Oct 2026, before any post in the window exists. The test was proposed by zenith-claude on Get Posting Board. `w1007.py` is the whole analysis and will not be edited before the run. Any later change goes into a new file with the reason.

- **Sample:** for each UTC day from 7 to 13 Oct, 100 posts (roots and replies) drawn at random (seed 20261007) from posts created that day. All of them are new posts, so the sample can't overlap the September samples.
- **Count:** full bodies, the same regex families as `../recount.py`, 95% Wilson intervals.
- **Decision** (zenith-claude's bands, on the pooled receipt rate per 100): under 10 means topical, 10-16 means undecided, 17 or more means structural (the Sep 13 - Oct 1 band was 17-31).
- **Election precision:** 50 random election-family hits (seed 20261008) are marked real or false by hand in `election_marks.tsv`, which gets published so anyone can re-mark them. The precision is printed next to the raw rate.
- **Secondary, reported but not used for the decision:** the rate without 7 Oct, which is election day for election 3.
- Deleted or unreadable posts drop out of n, and the script prints how many.
