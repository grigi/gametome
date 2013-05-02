gametome
========

Repo for the Linux Game Tome project, working towards the resurrection of happypenguin.org

Join the discussion on the forum at [http://happypenguin.onkoistudios.com/](http://happypenguin.onkoistudios.com/), or on the freenode IRC at #gametome (or via the [web client](http://webchat.freenode.net/?channels=gametome&uio=d4) ).

The database dump can be downloaded from [http://happypenguin.onkoistudios.com/uploads/happypenguin_dump.tar.bz2](http://happypenguin.onkoistudios.com/uploads/happypenguin_dump.tar.bz2)

grigis attempt
--------------

For this I tried to focus on a more basic version. It uses Bootstrap so I want to later on try and skin it using michealbs sepia TLGT-inspired theme. Right now I'm more focused on functionality, so we can do usability testing as soon as possible.

What currently works:

* Registering/validating EMail/using federated/social auth/associating to multiple accounts (currently only google)
* Basic Bootstrap interface
    * Basic theme based on michaelb's work:
    * [Pallet (chosen because of "retro" colors)](http://www.colourlovers.com/palette/53698/Its_a_Virtue)
    * [Bootstrap theme (from above color scheme)](http://www.stylebootstrap.info/index.php?style=VMxlFu6B86U54mbXKRjho)
    * A work in progress
* Import of legacy Game records:
    * Handling:
        * title, description, shortdescription, submittedby, createddate, updateddate, cost, version
        * Licence and capabilities is imported as tags
        * description is Translated to Markdown
        * ratings are imported as reviews with no body _(Not sure about this, should reviews and ratings be separate entities, or ratings as reviews?)_
        * Link to Company/Author
        * Includes 'other' if not empty
        * Image importing into related albums
    * Not Handling:
        * approvals
* Import of legacy News records:
    * Done!
    * headline,news,user,timestamp
    * extract category and short description from html blob
    * removed category/description/rating from html blob
    * Translate to Markdown
    * newstype and category imported as tags
    * link to game (if game exists)
* Import of legacy Comments:
    * Handling:  
        * comment is Translated to Markdown
        * subjext, comment, user, timestamp
        * sub-comments
        * Removing empty comments, and attaching children to parent
    * Not Handling:
        * spam detection
* Import of Company/Author, with links to games
* URL rewriting (games/news/comments):
    * Detects urls that links to games & Rewriting of valid urls that link to a game
	* Detect image urls
    * Handling of images and/or thumbnails
* News, Game, and Company pages with comments (comments not threaded yet)
* Fulltext search Using Haystack & Whoosh
* Simple Gallery (based on Galleria)
* Simple Forum (based on PyBBm)

What still needs to be done:

* Proper pagination for gallery
* Editing/creating new posts
    * Live data editing for your own content (or if you got given proxy rights) to make maintaining data easier
* Reviews/Content rating system (to combat trolling)
* Auto show images of related game item in news
* Spam detection
* Threaded comments
* I18N
* Finishing the theme
* Modernize the interface, using more javascript to make site flow better
    * Separate site logic from rendering
    * Make pagination implicit
* Usability testing
* Cleanup/refactoring of code:
    * Duplication of functionality for emoticons and profile page
    * Restructure project to be cleaner
    * Read two-scoops book
* Performance tuning:
    * Do query tuning
    * Implement object-level cacheing
    * Use content compressors


To get the initial data:

* Download bobz's database dump archive ~400 MB 
* Untar it to some handy location (I untarred it to ./data, so that there exists a directory ./data/screenshots)
* Download grigi's de-normalized JSON version of the DB. Unzip it to the same location. [GET IT HERE](http://happypenguin.onkoistudios.com/discussion/5/de-normalized-db#Item_2)

To get started:

* Setup a python environment (preferably a virtualenv)
* `pip install django-ckeditor django-taggit django-allauth` - install requirements
* `./manage.py syncdb` - default dev config uses a local sqlite database
* `./manage.py importhp` - import the legacy data
* `./manage.py runserver` - development server

Code-level priorities for the project:

* Dependancies should work in Python3 or have a in-progress plan to migrate to it
* Code should be kept as simple as possible, and have a reasonable amount of tests
* Care should be taken to keep an eye on performance

