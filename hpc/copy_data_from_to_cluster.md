=== Alice ===
From local system.
    gsiscp <<source>> <<destination>>
=== Other ===
"NOTE: Run all at local/your system"

From cluster to local system
    rsync -av <<username>>@<<cluster full hostname>>:<<path to source>> .
From local system to cluster
    rsync -av . <<username>>@<<cluster full hostname>>:<<path to destination>>