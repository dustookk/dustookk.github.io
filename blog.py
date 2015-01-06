#!/usr/bin/env python
# -*- coding: utf-8 -*-

import markdown
import os
import re
from jinja2 import Template

DRAFTS_DIR = 'drafts/'
POSTS_DIR = 'posts/'
POST_TEMPLATE = 'template/post.html'


class Post(object):
    def __init__(self, path):
        self.path = path


def main():
    lst = os.listdir(DRAFTS_DIR)
    md = markdown.Markdown()
    for file_name in lst:
        print 'hit a md', file_name
        produce(md, file_name)


def produce(md, file_name):
    (name, extension) = os.path.splitext(file_name)
    draft_path = os.path.join(DRAFTS_DIR, file_name)
    post_path = os.path.join(POSTS_DIR, name + '.html')
    # read
    with open(draft_path) as draft_file:
        original_content = draft_file.read().decode('utf-8')
        # md content
        draft_file.seek(0)
        md_content = ''.join(draft_file.readlines()[3:]).decode('utf-8')

    html_content = md.convert(md_content)

    # template
    with open(POST_TEMPLATE) as template_file:
        template_content = template_file.read()

    template = Template(template_content.decode('utf-8'))
    title = get_title(original_content)
    date = get_date(original_content)
    url = 'http://dustookk.githubg.com/' + post_path
    tags = get_tags(original_content).replace('-', ', ')
    final_content = template.render(DATE=date, TITLE=title, TAGS=tags, URL=url, CONTENT=html_content)

    # write
    with open(post_path, 'w+') as post_file:
        post_file.write(final_content.encode('utf-8'))


def get_title(content):
    match_result = re.search('#TITLE:.*#', content)
    return match_result.group(0).replace('#TITLE:', '').replace('#', '')


def get_date(content):
    match_result = re.search('#DATE:.*#', content)
    return match_result.group(0).replace('#DATE:', '').replace('#', '')


def get_tags(content):
    match_result = re.search('#TAGS:.*#', content)
    return match_result.group(0).replace('#TAGS:', '').replace('#', '')


if __name__ == '__main__':
    main()