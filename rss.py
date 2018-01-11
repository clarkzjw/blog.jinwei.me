import os
import jinja2

import glob
from bs4 import BeautifulSoup


class FilePathLoader(jinja2.BaseLoader):
    def __init__(self, cwd):
        self.cwd = cwd

    def get_source(self, environment, template):
        filename = os.path.join(self.cwd, template)

        try:
            with open(filename, 'r') as f:
                contents = f.read()
        except IOError:
            raise jinja2.TemplateNotFound(filename)

        return contents, filename, lambda: False


def render_template(cwd, template_path, context):
    env = jinja2.Environment(loader=FilePathLoader(cwd))
    return env.get_template(template_path).render(context)


def main():

    filenames = glob.glob("./_build/html/_posts/*/*/*.html")
    print(filenames)

    posts = []

    for p in filenames:
        soup = BeautifulSoup(open(p), "html5lib")
        body = soup.find_all("div", class_="body")[0].text

        posts.append({
            "title": soup.title.string,
            "body": body,
            "date_rss": body[body.find("Publish Date:")+13:body.find("Publish Date:")+23],
            "permalink": "/".join(p.split("/")[3:])
        })

    context = {
        "site": {
            "name": "Hello World",
            "url": "https://blog.jinwei.me",
            "tagline": "Freedom is my birth right and I shall have it."
        },
        "posts": posts
    }

    return render_template(
        ".",
        "all.rss.xml",
        context
    )


if __name__ == '__main__':
    print(main())
