from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from gtdb.models import Entity, Game, News, Comment, Review, URLlink, Company
import json
from django.db import transaction
import sys
import re
import html5lib
from html5lib import sanitizer
from django.utils.timezone import now

sanhtml = html5lib.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)

#IMP_DATE = '2013-04-01T00:00:00+00:00'

def user_factory(username):
    if username is None:
        username = 'Anonymous'
    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        user = User.objects.create(username=username)
    return user

def company_factory(compname, author):
    if author is None or author == '':
        author = 'Unspecified'
    if compname is None or compname == '':
        compname = author
    try:
        company = Company.objects.get(title__iexact=compname)
        if company.description.lower().find(author.lower()) == -1:
            company.description += "%s\n" % (author)
            company.save()
    except Company.DoesNotExist:
        company = Company.objects.create(title=compname, created_date=now(), updated_date=now(), description="%s\n" % (author))
    return company

def sanitize_desc(desc):
    # Replace the following with a link to the real game:
    #'http://www.happypenguin.org/show?Fashion%20Cents%20Deluxe'
    # Oh, this probably needs to be done at the end, because it may, or may not exist yet.
    
    desc = sanhtml.parse(desc).toxml()[19:][:-14]
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
        if len(desc) > 0:
            com = Comment.objects.create(
                created_date = l['timestamp'],
                updated_date = l['timestamp'],
                description = desc,
                entity = game,
                title = l['subject'],
                reporter = user_factory(l['user']),
                parent = parent
            )
            sub_comments(game, com, l['comments'])
        else:
            sub_comments(game, parent, l['comments'])

#User.objects.get_or_create(username=username)

class Command(BaseCommand):
    help = 'Imports the de-normalised happypuppy data'

    def handle(self, *args, **options):
        # Disable auto transactions - increase import performance
        transaction.enter_transaction_management(managed=True)
        transaction.managed(flag=True)
        count = 0

        # Hack to let us set auto-dates manualy for import
        turn_off_auto_now(Entity, 'updated_date')
        turn_off_auto_now_add(Entity, 'created_date')
        '''turn_off_auto_now(Game, 'updated_date')
        turn_off_auto_now_add(Game, 'created_date')
        turn_off_auto_now(News, 'updated_date')
        turn_off_auto_now_add(News, 'created_date')
        turn_off_auto_now(Comment, 'updated_date')
        turn_off_auto_now_add(Comment, 'created_date')'''
        
        doc = json.load(open('%s/data/games.json' % (settings.PROJECT_ROOT)))
        for g in doc[:200]:
            #print(json.dumps(g,indent=4,sort_keys=True))
            
            # Not handling: screenshot, approved_by, approved_date
            
            desc = g['description']
            if len(g['other']) > 2:
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
            for c in g['capabilities']:
                game.tags.add(c)
            if g['license'] != 'unknown':
                game.tags.add(g['license'])
            
            for l in g['comments']:
                desc = sanitize_desc(l['comment'])
                if len(desc) > 0:
                    com = Comment.objects.create(
                        created_date = l['timestamp'],
                        updated_date = l['timestamp'],
                        description = desc,
                        entity = game,
                        title = l['subject'],
                        reporter = user_factory(l['user'])
                    )
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
                URLlink.objects.create(
                    entity=game,
                    desc=u['description'] if u['description'] else 'unnamed',
                    url=u['url']
                )
            if g['homepage']:
                URLlink.objects.create(
                    entity=game,
                    desc='homepage',
                    url=g['homepage']
                )
                        
            count = count+1
            if count==100:
                sys.stdout.write('.')
                sys.stdout.flush()
                count=0
                transaction.commit()
                
        doc = json.load(open('%s/data/news.json' % (settings.PROJECT_ROOT)))
        for n in doc[:200]:
            #print(json.dumps(n,indent=4,sort_keys=True))
            
            # Not handling: game

            desc = n['news']
            try:
                cat = re.search(r'<em>Category: </em>([^<]*)<br>', desc).group(1)
            except:
                cat = None
            try:
                short =  re.search(r'<em>Description:</em> (.*)', desc).group(1)
            except:
                short = None
            
            desc = re.sub(r'^<a href.*Category:.*Rating.*Description[^\n]*', '', desc, flags=re.MULTILINE|re.DOTALL)
            
            news = News.objects.create(
                title=n['headline'],
                description=sanitize_desc(desc),
                short=short,
                reporter=user_factory(n['user']),
                created_date = n['timestamp'],
                updated_date = n['timestamp']
            )
            if n['newstype'] != 'default':
                news.tags.add(n['newstype'])
            if cat:
                news.tags.add(cat)
            for l in n['comments']:
                desc = sanitize_desc(l['comment'])
                if len(desc) > 0:
                    com = Comment.objects.create(
                        created_date = l['timestamp'],
                        updated_date = l['timestamp'],
                        description = desc,
                        entity = news,
                        title = l['subject'],
                        reporter = user_factory(l['user'])
                    )
                    sub_comments(news, com, l['comments'])
                else:
                    sub_comments(news, None, l['comments'])

            count = count+1
            if count==100:
                sys.stdout.write('.')
                sys.stdout.flush()
                count=0
                transaction.commit()

        print('')                
        transaction.commit()
