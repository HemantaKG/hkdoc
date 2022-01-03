===== GitLab/GitHub =====
[[http://gitlab.icts.res.in/|GitLab]]
[[https://github.com/|GitHub]]
== Get from git ==
    ssh-keygen
    less .ssh/id_rsa.pub
    git clone git@gitlab.icts.res.in:astrorel/alice.git
    cd alice

== Push into git ==
    git add test.conf
    git commit -m "data-11-11-2016"
    git push -u origin master

    cd <<dir>>
    git init
    git remote add origin git@gitlab.icts.res.in:hemanta/humpty.git
    git add .
    git commit -m "<add commit detail>
    git push -u origin master