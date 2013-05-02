from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from gtdb.models import Entity, Game, News, Comment, Review, URLlink, Company, Relation
import json
#from django.db import transaction
import os
import sys
import re
from django.utils.timezone import now
from django.db.models import Q
#from html2bbcode.parser import HTML2BBCode
#import html5lib
#from html5lib import sanitizer
from galeria.models import Album, Picture
from html2text import html2text
from django.utils.html import urlize
from django.core.files import File
from django.core.validators import URLValidator, ValidationError
from os import listdir
try:
    from urllib import unquote_plus
except ImportError:
    # Python 3
    from urllib.parse import unquote_plus
    unicode = str

#sanhtml = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
#bbparser = HTML2BBCode()
urlvalidate = URLValidator()

fimg = open('imglog.txt','w')

gamealbum = Album.objects.create(
    title = "Games",
    slug = "games",
    description = "Game-specific albums",
)

legacyalbum = Album.objects.create(
    title = "Legacy",
    slug = "legacy",
    description = "Unconnected legacy images from happypenguin 2",
)

count_game = 0
count_news = 0
count_comment = 0
count_company = 0
count_user = 0
count_images = 0
count_urls = 0

images = {}

#IMP_DATE = '2013-04-01T00:00:00+00:00'

def nlen(obj):
    if obj is None:
        return 0
    return len(obj)

def user_factory(username):
    if username is None:
        username = 'Anonymous'
    try:
        user = User.objects.get(username__iexact=unicode(username))
    except User.DoesNotExist:
        user = User.objects.create(username=username)
        global count_user
        count_user += 1
    return user

def company_factory(compname, author):
    if author is None or author == '' or author == '-' or author.lower() == 'none':
        author = 'Unspecified'
    if compname is None or compname == '' or compname == '-' or compname.lower() == 'none':
        compname = author
    try:
        company = Company.objects.filter(title__iexact=unicode(compname))[0]
        if company.description.lower().find(author.lower()) == -1:
            company.description += "%s\n" % (author)
            company.save()
    except IndexError:
        company = Company.objects.create(title=compname, created_date=now(), updated_date=now(), description="%s\n" % (author))
        global count_company
        count_company += 1
    return company

def find_game(gamename):
    if gamename:
        games = Game.objects.filter(title__iexact=gamename)
        if nlen(games) >= 1:
            return games[0]
    return None

def link_url(entity, desc, url):
    try:
        urlvalidate(url)
    except ValidationError:
        try:
            urlvalidate(desc)
            a=url
            url=desc
            desc=a
        except ValidationError:
            pass
    URLlink.objects.create(
        entity=entity,
        desc=desc,
        url=url
    )
    global count_urls
    count_urls += 1
    

def import_image(game, imagename, title=None, short=None, parent=gamealbum):
    if game:
        title = game.title
        short = game.short
        
    fname = '%s/data/screenshots/%s' % (settings.PROJECT_ROOT, imagename)
    if os.path.isfile(fname):
        #print game.title, imagename
        try:
            if game:
                album = Album.objects.create(
                    title = title,
                    slug = slugify(title),
                    description = "Screenshots for %s" % (title),
                    parent = parent,
                )
                game.album = album
                game.save()
            else:
                album = parent
            pic = Picture(
                title = title,
                slug = slugify(title),
                description = short,
                album = album,
            )
            pic.original_image.save(
                imagename,
                File(open(fname))
            )
            pic.save()
            images[imagename] = pic
            global count_images
            count_images += 1
            return pic
        except:
            pass
    else:
        try:
            print >>fimg, "Bad: '%s', '%s'" % (title, imagename)
        except:
            pass
    
    return None


def sanitize_desc(desc):
    '''desc = re.sub(r'>\s+<', '><', desc)
    desc = re.sub(r'\s*<[Bb][Rr]/?>\s*', '<br>', desc)
    desc = re.sub(r'\s+', ' ', desc)
    desc = re.sub(r'</[Pp]>\s*<[Pp]>', '\n\n', desc)
    desc = re.sub(r'<[Pp]>', '\n\n', desc)
    desc = re.sub(r'</[Pp]>', '\n\n', desc)
    desc = re.sub(r'^\s+','', desc)
    desc = re.sub(r'\s+$','', desc)
    return bbparser.feed(urlize(desc)).strip()'''
    try:
        return html2text(urlize(desc)).strip()
    except:
        return desc
        

def iter_fields_and_do(Clazz, field_name, func):
    for field in Clazz._meta.local_fields:
        if field.name == field_name:
            func(field)
def turn_off_auto_now(Clazz, field_name):
    def auto_now_off(field):
        field.auto_now = False
    iter_fields_and_do(Clazz, field_name, auto_now_off)

def turn_off_auto_now_add(Clazz, field_name):
    def auto_now_add_off(field):
        field.auto_now_add = False
    iter_fields_and_do(Clazz, field_name, auto_now_add_off)

def sub_comments(game,parent,dic):
    for l in dic:
        desc = sanitize_desc(l['comment'])
        if nlen(desc) > 0:
            com = Comment.objects.create(
                created_date = l['timestamp'],
                updated_date = l['timestamp'],
                description = desc,
                entity = game,
                title = l['subject'],
                reporter = user_factory(l['user']),
                parent = parent
            )
            global count_comment
            count_comment += 1
            sub_comments(game, com, l['comments'])
        else:
            sub_comments(game, parent, l['comments'])

#User.objects.get_or_create(username=username)

class Command(BaseCommand):
    help = 'Imports the de-normalised happypuppy data'

    def handle(self, *args, **options):
        # Disable auto transactions - increase import performance
        #transaction.enter_transaction_management(managed=True)
        #transaction.managed(flag=True)
        count=0
        global count_game
        global count_news
        global count_comment
        global count_company
        global count_user
        global count_images
        global count_urls
        count_newsgame = 0
        count_newsgametot = 0

        # Hack to let us set auto-dates manualy for import
        turn_off_auto_now(Entity, 'updated_date')
        turn_off_auto_now_add(Entity, 'created_date')
        '''turn_off_auto_now(Game, 'updated_date')
        turn_off_auto_now_add(Game, 'created_date')
        turn_off_auto_now(News, 'updated_date')
        turn_off_auto_now_add(News, 'created_date')
        turn_off_auto_now(Comment, 'updated_date')
        turn_off_auto_now_add(Comment, 'created_date')'''
        
        print("Importing Games:")
        
        doc = json.load(open('%s/data/games.json' % (settings.PROJECT_ROOT)))
        for g in doc:#[:200]:
            #print(json.dumps(g,indent=4,sort_keys=True))
            
            # Not handling: approved_by, approved_date
            
            desc = g['description']
            if nlen(g['other']) > 2:
                desc += "<br/><h4>Other information:</h4>" + g['other']
            
            game = Game.objects.create(
                title=g['title'],
                description=sanitize_desc(desc),
                short=g['short_description'],
                reporter=user_factory(g['submitted_by']),
                created_date = '%sT00:00:00+00:00' % (g['date_sumbitted']),
                updated_date = g['timestamp'] if g['timestamp'] else '%sT00:00:00+00:00' % (g['date_sumbitted']),
                cost = g['cost'],
                version = g['version'],
                company = company_factory(g['company'], g['author']),
            )
            count_game += 1
            for c in g['capabilities']:
                game.tags.add(c)
            if g['license'] != 'unknown':
                game.tags.add(g['license'])
            
            for l in g['comments']:
                desc = sanitize_desc(l['comment'])
                if nlen(desc) > 0:
                    com = Comment.objects.create(
                        created_date = l['timestamp'],
                        updated_date = l['timestamp'],
                        description = desc,
                        entity = game,
                        title = l['subject'],
                        reporter = user_factory(l['user'])
                    )
                    count_comment += 1
                    sub_comments(game, com, l['comments'])
                else:
                    sub_comments(game, None, l['comments'])
        
            for r in g['ratings']:
                rate = Review.objects.create(
                    created_date = l['timestamp'],
                    updated_date = l['timestamp'],
                    entity=game,
                    title=g['title'],
                    reporter=user_factory(r['user']),
                    score=r['rating']
                )
            for u in g['urls']:
                link_url(
                    entity=game,
                    desc=u['description'] if u['description'] else 'unnamed',
                    url=u['url']
                )
                
            if g['homepage']:
                link_url(
                    entity=game,
                    desc='homepage',
                    url=g['homepage']
                )
            
            import_image(game, g['screenshot'])
                        
            count = count+1
            if count==100:
                sys.stdout.write('.')
                sys.stdout.flush()
                count=0
                #transaction.commit()

        count_comment_games = count_comment
        print('')
        print("%d Games imported" % (count_game))
        print("%d Images imported" % (count_images))
        print("%d Comments imported" % (count_comment))
        print("%d Companies/Authors imported" % (count_company))
        print("%d Users imported" % (count_user))
        print("%s URL links imported" % (count_urls))
        print("Importing News:")
                
        doc = json.load(open('%s/data/news.json' % (settings.PROJECT_ROOT)))
        for n in doc:#[:200]:
            #print(json.dumps(n,indent=4,sort_keys=True))
            
            # Handling everything :-)

            desc = n['news']
            try:
                cat = re.search(r'<em>Category: </em>([^<]*)<br>', desc).group(1)
            except:
                cat = None
            try:
                short =  re.search(r'<em>Description:</em> (.*)', desc).group(1)
            except:
                short = None
            
            desc = re.sub(r'^.*Category:.*Description[^\n]*', '', desc, flags=re.MULTILINE|re.DOTALL)
            
            news = News.objects.create(
                title=n['headline'],
                description=sanitize_desc(desc),
                short=short,
                reporter=user_factory(n['user']),
                created_date = n['timestamp'],
                updated_date = n['timestamp']
            )
            count_news += 1
            game = find_game(n['game'])
            if game:
                # create relation to game of type 'news'
                Relation.objects.create(
                    type='news',
                    a=news,
                    b=game,
                )
                count_newsgame += 1
            if n['game'] is not None and nlen(n['game']) > 0:
                count_newsgametot += 1

            if n['newstype'] != 'default':
                news.tags.add(n['newstype'])
            if cat:
                news.tags.add(cat)
            for l in n['comments']:
                desc = sanitize_desc(l['comment'])
                if nlen(desc) > 0:
                    com = Comment.objects.create(
                        created_date = l['timestamp'],
                        updated_date = l['timestamp'],
                        description = desc,
                        entity = news,
                        title = l['subject'],
                        reporter = user_factory(l['user'])
                    )
                    count_comment += 1
                    sub_comments(news, com, l['comments'])
                else:
                    sub_comments(news, None, l['comments'])

            count = count+1
            if count==100:
                sys.stdout.write('.')
                sys.stdout.flush()
                count=0
                #transaction.commit()

        print('')
        print("%d News imported" % (count_news))
        print("%d Comments imported" % (count_comment - count_comment_games))
        print("%d/%d Games linked to" % (count_newsgame, count_newsgametot))
        print('Relinking urls:')
        #transaction.commit()
        
        for f in listdir('%s/data/screenshots/' % (settings.PROJECT_ROOT)):
            if not images.get(str(f), False):
                #print f
                import_image(None, str(f), title=str(f), short='', parent=legacyalbum)        
        
        count_uf=0
        count_g=0
        count_gs=0
        count_i=0
        count_is=0
        torep = Entity.objects.filter(Q(description__contains='happypenguin.org/') | Q(description__contains='/images/'))
        for ent in torep:
            count_uf += 1
            origdesc = '%s' % (ent.description)
            newdesc = ''
            old_last=0            
            
            for m in re.finditer(r'(\[[^\[\]\!]*)?(!?)\[([^\[\]]*)\]\(([^\)]*)\)(\]\(([^\)]*)\))?', ent.description):
                try:
                    pre = m.group(1).replace('\n', '')
                except AttributeError:
                    pre = None
                img = m.group(2)
                desc = m.group(3).replace('\n', '')
                (url1, t, desc1) = re.match(r'([^ ]*)( [\'"]?([^\'"]*)[\'"]?)?', m.group(4).replace('\n', '')).groups()
                try:
                    (url2, t, desc2) = re.match(r'([^ ]*)( [\'"]?([^\'"]*)[\'"]?)?', m.group(6).replace('\n', '')).groups()
                except AttributeError:
                    url2 = None
                    desc2 = None
                
                lm = re.match(r'.*show[\?=](.*)', url1)
                if lm:
                    count_g += 1
                    #print 'g', m.start(), m.end(), (ent.description[int(m.start()):int(m.end())]).replace('\n', '')
                    gamename = unquote_plus(lm.group(1))
                    game = find_game(gamename)
                    if game:
                        count_gs += 1
                        url1 = game.get_absolute_url()
                        val = '[%s](%s)' % (desc, url1)
                        newdesc += ent.description[old_last:int(m.start())] + val
                        old_last = int(m.end())
                        # create relation to game of type 'linked'
                        Relation.objects.create(
                            type='linked',
                            a=ent.get_real(),
                            b=game,
                        )
                    else:
                        try:
                            print >>fimg, "g %s: %s" % (gamename, (ent.description[int(m.start()):int(m.end())]).replace('\n', ''))
                        except:
                            pass
                
                lm = re.match(r'.*/images/(thumbs/)?(.*)', url1)
                if lm:
                    count_i += 1
                    #print 'i', m.start(), m.end(), (ent.description[int(m.start()):int(m.end())]).replace('\n', '')
                    image = unquote_plus(lm.group(2))
                    if desc == url1:
                        desc = ''
                    if not pre:
                        pre = '['
                    try:
                        img = images[image]
                        if desc == '':
                            desc = img.title
                    except:
                        if desc == '':
                            desc = image
                        #print image, desc
                        img = import_image(None, image, title=desc, short='', parent=legacyalbum)
                    
                    if img:
                        count_is += 1
                        url1 = img.thumbnail_image.url
                        url2 = img.album.get_absolute_url()
                        val = '%s![%s](%s)](%s "%s")' % (pre, desc, url1, url2, desc)
                        newdesc += ent.description[old_last:int(m.start())] + val
                        old_last = int(m.end())
                    else:
                        try:
                            print >>fimg, "i %s: %s" % (image, (ent.description[int(m.start()):int(m.end())]).replace('\n', ''))
                        except:
                            pass

            if nlen(newdesc) > 0:
                newdesc += ent.description[old_last:]
                ent.description = newdesc
            
            if origdesc != ent.description:
                #print '<'
                #print '<', origdesc
                #print '>'
                #print '>', ent.description
                ent.save()
                count = count+1
                if count==100:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    count=0
                    #transaction.commit()

        print('')                
        print('%d objects affected' % (count_uf))
        print('%d/%d Game URLs relinked' % (count_gs, count_g))
        print('%d/%d Images imported' % (count_is, count_i))
        #transaction.commit()
