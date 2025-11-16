#!/usr/bin/env python3

# synchronize version with pyproject.toml file
from importlib.metadata import version
__version__ = version("markpub")
APPVERSION = version("markpub")
APPNAME = 'MarkPub'

# setup logging
import logging, os
log_level = os.environ.get('LOGLEVEL', 'WARNING').upper()

logging.basicConfig(
    level=getattr(logging, log_level, 'WARNING'),
    format="%(asctime)s - %(name)s - %(levelname)s: %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger('markpub')

# python libraries
import argparse
import datetime
from dateutil.parser import parse
import glob
import hashlib
import jinja2
import json
from pathlib import Path
import re
import shutil
import subprocess
import textwrap
import time
import traceback
from urllib.parse import urlparse
import yaml

# Markpub libraries and modules - mistletoe based Markdown to HTML conversion
from mistletoe import Document
from markpub.mistletoe_renderer.massivewiki import MassiveWikiRenderer
import markpub_themes

# wiki page links, backlinks table
wiki_pagelinks = {}

# git forge proper name table
def git_forge_proper_name(git_edit_url):
    git_forge_names = {
        'github.com':'GitHub',
        'codeberg.org':'Codeberg',
        'gitlab.com':'GitLab'
    }
    forge_loc = urlparse(git_edit_url).netloc
    if (forge_name := git_forge_names.get(forge_loc)) is None:
        return forge_loc
    else:
        return forge_name

def markdown_convert(markdown_text, rootdir, fileroot, file_id, websiteroot):
    with MassiveWikiRenderer(rootdir=rootdir, fileroot=fileroot, wikilinks=wiki_pagelinks, file_id=file_id, websiteroot=websiteroot) as renderer:
        # include websiteroot in local website page links
        locallink_pattern = r'(\[.*?\])\(\/(.*?\.html)\)'
        locallink_replacement = rf'\1({websiteroot}/\2)'
        page_markdown_text = re.sub(locallink_pattern, locallink_replacement, markdown_text)
        return renderer.render(Document(page_markdown_text))

# set up a Jinja2 environment
def jinja2_environment(path_to_templates):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path_to_templates),
    )

# load config file
def load_config(path):
    with open(path) as infile:
        return yaml.safe_load(infile)

# scrub wiki path to handle ' ', '_', '?', '"', '#', '%' characters in wiki page names
# change those characters to '_' to avoid URL generation errors
def scrub_path(filepath):
    return re.sub(r'([ _?\#%"]+)', '_', filepath)

# find outgoing wikilinks in a wiki page
def find_tolinks(file):
    with open(file, encoding='utf-8') as infile:
        pagetext = infile.read()
    # use negative lookbehind assertion to exclude '![[' links
    wikilink_pattern = re.compile(r"(?<!!)\[\[ *(.+?) *(\| *.+?)? *\]\]")
    to_links = [p[0] for p in wikilink_pattern.findall(pagetext)]
    return to_links

# take a path object pointing to a Markdown file
# return Markdown (as string) and YAML front matter (as dict)
# for YAML, {} = no front matter, False = YAML syntax error
def read_markdown_and_front_matter(path):
    with path.open(encoding='utf-8') as infile:
        lines = infile.readlines()
    # take care to look exactly for two `---` lines with valid YAML in between
    if lines and re.match(r'^---$',lines[0]):
        count = 0
        found_front_matter_end = False
        for line in lines[1:]:
            count += 1
            if re.match(r'^---$',line):
                found_front_matter_end = True
                break
        if found_front_matter_end:
            try:
                front_matter = yaml.safe_load(''.join(lines[1:count]))
            except (yaml.parser.ParserError, yaml.scanner.ScannerError):
                # return Markdown + False (YAML syntax error)
                return ''.join(lines), False
            # return Markdown + front_matter
            return ''.join(lines[count+1:]), front_matter
    # return Markdown + empty dict
    return ''.join(lines), {}

# read and convert Sidebar markdown to HTML
def sidebar_convert_markdown(path, rootdir, fileroot, websiteroot):
    if path.exists():
        markdown_text, front_matter = read_markdown_and_front_matter(path)
    else:
        markdown_text = ''
    fid = hashlib.md5(Path(path).stem.lower().encode()).hexdigest()
    return markdown_convert(markdown_text, rootdir, fileroot, fid, websiteroot)

# handle datetime.date serialization for json.dumps()
def datetime_date_serializer(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

# build website
def build_site(args):
    logger.debug("Building ....")
    logger.info("args: %s", args)
    logger.info(f"build website in {args[0].output} from Markdown files in {args[0].input}")

    # read configuration file
    config_file = Path(args[0].config).resolve().as_posix()
    logger.info(f"using config file: {config_file}")
    config = load_config(Path(config_file).resolve().as_posix())
    # set theme directory
    try:
        theme_name = config.get('theme')
        if theme_name is None:
            theme_dir = markpub_themes.get_theme_path('dolce')
        elif Path(f"{args[0].input}/.markpub/themes/{theme_name}").resolve().exists():
            theme_dir = Path(f"{args[0].input}/.markpub/themes/{theme_name}").resolve().as_posix()
        else:
            theme_dir = markpub_themes.get_theme_path(theme_name)
    except Exception as e:
        print(f"ERROR: {e}\t- Check 'theme:' value in 'markpub.yaml' file.")
        return

    logger.info(f"using website theme directory: {theme_dir}")

    if 'recent_changes_count' not in config:
        config['recent_changes_count'] = 5

    # remember paths
    dir_output = Path(args[0].output).resolve().as_posix()
    dir_wiki = Path(args[0].input).resolve().as_posix()
    rootdir = '/'
    websiteroot = args[0].root

    # get a Jinja2 environment
    j = jinja2_environment(theme_dir)

    # render html pages from jinja2 templates
    def render_template(template_name, **kwargs):
        common_args = {
            'build_time': build_time,
            'wiki_title': config['wiki_title'],
            'author': config['author'],
            'repo': config['repo'],
            'license': config['license'],
            'sidebar_body': sidebar_body,
            'lunr_index_sitepath': lunr_index_sitepath,
            'lunr_posts_sitepath': lunr_posts_sitepath,
            'websiteroot': websiteroot,
        }
        # Merge common_args with any additional kwargs
        render_args = {**common_args, **kwargs}
        return j.get_template(template_name).render(**render_args)

    # set context for page template rendering
    def get_page_context(file, markdown_body, wiki_pagelinks, config):
        """
        Args:
        file (Path): Path to the file being processed
        markdown_body (str): Rendered markdown content
        wiki_pagelinks (dict): Dictionary of page links
        config (dict): Configuration dictionary
        Returns:
        dict: Context for template rendering
        """
        # prepare base context
        context = {
            'title': file.stem,
            'fs_path': wiki_pagelinks.get(file.stem.lower(), {}).get('fs_path', []),
            'markdown_body': markdown_body,
            'backlinks': wiki_pagelinks.get(file.stem.lower(), {}).get('backlinks', [])
        }
        # determine edit URL
        # some pages to not have git_forge edit button
        no_edit_patterns = config.get('no_edit_url_pages') or []
        if file.stem != 'README' and file.name != config.get('sidebar', '') and not any(Path(file).match(no_edit) for no_edit in no_edit_patterns):
            if config.get('edit_url'):
                context['edit_url'] = (
                    f"{config['edit_url'].rstrip('/')}/{config['edit_branch']}"
                    f"{wiki_pagelinks.get(file.stem.lower(), {}).get('fs_path', '')}"
                )
                context['git_forge'] = git_forge_proper_name(config['edit_url'])
        else:
                # For README, sidebar, or config['no_edit_url_pages'] explicitly set empty edit_url
                context['edit_url'] = ''
        return context

    # set up lunr_index_filename and lunr_index_sitepath
    if (args[0].lunr):
        timestamp_thisrun = time.time()
        lunr_index_filename = f"lunr-index-{timestamp_thisrun}.js" # needed for next two variables
        lunr_index_filepath = Path(dir_output) / lunr_index_filename # local filesystem
        lunr_index_sitepath = f"{websiteroot}/{lunr_index_filename}" # website
        lunr_posts_filename = f"lunr-posts-{timestamp_thisrun}.js" # needed for next two variables
        lunr_posts_filepath = Path(dir_output) / lunr_posts_filename # local filesystem
        lunr_posts_sitepath = f"{websiteroot}/{lunr_posts_filename}" # website
    else:
        # needed to feed to themes
        lunr_index_sitepath = ''
        lunr_posts_sitepath = ''

    # render the wiki
    try:
        # remove existing output directory and recreate
        logger.debug("remove existing output directory and recreate")
        shutil.rmtree(dir_output, ignore_errors=True)
        Path(dir_output).mkdir()

        # insure that a README.md file exists at wiki root directory; create if needed
        #   FIRST rename any existing index.html file
        if Path(f"{dir_wiki}/index.html").exists():
           Path(f"{dir_wiki}/index.html").rename(f"{dir_wiki}/previous-index.html")
        if not Path(f"{dir_wiki}/README.md").exists():
            if Path(f"{dir_wiki}/index.md").exists():
                shutil.copy(f"{dir_wiki}/index.md", f"{dir_wiki}/README.md")
            else:
                lines=[f"# {config['wiki_title']}", '', 'This is the home page of this website.']
                Path(f"{dir_wiki}/README.md").write_text("\n".join(lines) + "\n")

        # get list of wiki files using a glob.iglob iterator (consumed in list comprehension)
        allfiles = [f for f in glob.iglob(f"{dir_wiki}/**/*.*", recursive=True, include_hidden=False) if Path(f).is_file()]
        # remove excluded_directories, and sidebar
        excluded_dirs = config.get('excluded_directories') or []
        sidebar_file = config.get('sidebar')
        allfiles = [f for f in allfiles if not (
            any(ex_dir in f for ex_dir in excluded_dirs) or
            (sidebar_file is not None and f.endswith(sidebar_file)))]

        # read wiki content and build wikilinks dictionary; lunr index lists
        lunr_idx_data=[]
        lunr_posts=[]
        for file in allfiles:
            logger.debug("file %s: ", file)
            fs_path = rootdir+Path(file).relative_to(dir_wiki).as_posix()
            clean_filepath = scrub_path(fs_path)
            if Path(file).suffix == '.md':
                logger.debug("key: %s", Path(file).name)
                html_path = Path(clean_filepath).with_suffix(".html").as_posix()
                logger.debug("html path: %s", html_path)
                # add filesystem path, html path, backlinks list, wikipage-id to wiki_path_links dictionary
                wikipage_id = hashlib.md5(Path(file).stem.lower().encode()).hexdigest()
                wiki_pagelinks[Path(file).stem.lower()] = {'fs_path':fs_path, 'html_path':html_path, 'backlinks':[], 'wikipage_id':wikipage_id}
                # add lunr data to lunr idx_data and posts lists
                if(args[0].lunr):
                    link = Path(clean_filepath).with_suffix(".html").as_posix()
                    title = Path(file).stem
                    lunr_idx_data.append({"link":link, "title":title, "body": Path(file).read_text(encoding='utf-8')})
                    lunr_posts.append({"link":link, "title":title})
            else:
                logger.debug("key: %s", Path(file).name)
                html_path = clean_filepath
                logger.debug("html path: %s", html_path)
                # add html path and backlinks list to wiki_pagelinks dict
                wiki_pagelinks[Path(file).name.lower()] = {'fs_path':fs_path, 'html_path':html_path, 'backlinks':[]}

        logger.debug("wiki page links: %s", wiki_pagelinks)
        logger.debug("lunr index length %s: ",len(lunr_idx_data))
        # update wiki_pagelinks dictionary with backlinks
        for file in allfiles:
            if Path(file).name == config['sidebar']:  # do not backlink to sidebar
                continue
            if Path(file).suffix == '.md':
                to_links = find_tolinks(file)
                for page in to_links:
                    logger.info("on page %s add backlink to page %s", Path(page).name, wiki_pagelinks[Path(file).stem.lower()]['html_path'])
                    if ( Path(page).name.lower() in wiki_pagelinks and
                         not any(wiki_pagelinks[Path(file).stem.lower()]['html_path'] in t for t in wiki_pagelinks[Path(page).name.lower()]['backlinks']) ):
                        backlink_tuple = (wiki_pagelinks[Path(file).stem.lower()]['html_path'],Path(file).stem)
                        wiki_pagelinks[Path(page).name.lower()]['backlinks'].append(backlink_tuple)

        # render all the Markdown files
        logger.debug("copy wiki to output; render .md files to HTML")
        all_pages = []
        build_time = datetime.datetime.now(datetime.UTC).strftime("%A, %B %d, %Y at %H:%M UTC")

        if 'sidebar' in config:
            sidebar_body = sidebar_convert_markdown(Path(dir_wiki) / config['sidebar'], rootdir, args[0].input, websiteroot)
        else:
            sidebar_body = ''

        for file in allfiles:
            clean_filepath = scrub_path(rootdir+Path(file).relative_to(dir_wiki).as_posix())
            # make needed subdirectories
            Path(dir_output+clean_filepath).parent.mkdir(parents=True, exist_ok=True)
            if Path(file).suffix == '.md':
                logger.info("Rendering %s", file)
                # parse Markdown file
                markdown_text, front_matter = read_markdown_and_front_matter(Path(file))
                if front_matter is False:
                    print(f"NOTE: YAML syntax error in front matter of '{Path(file)}'")
                    front_matter = {}
                # output JSON of front matter
                (Path(dir_output+clean_filepath).with_suffix(".json")).write_text(json.dumps(front_matter, indent=2, default=datetime_date_serializer))
                # render and output HTML (empty edit_url on README and Sidebar pages)
                file_id = hashlib.md5(Path(file).stem.lower().encode()).hexdigest()
                markdown_body = markdown_convert(markdown_text, rootdir, args[0].input, file_id, websiteroot)
                page_context = get_page_context(Path(file), markdown_body, wiki_pagelinks, config)
                # add bluesky_comments from front matter or use empty string
                page_context['bluesky_comments_post'] = front_matter.get('bluesky_comments_post', '')
                html = render_template('page.html', **page_context)
                (Path(dir_output+clean_filepath).with_suffix(".html")).write_text(html)

                # get commit message and time
                date = ''
                change = ''
                author = ''
                if args[0].commits:
                    root = Path(file).parent.as_posix()
                    try:
                        p = subprocess.run(["git", "-C", Path(root), "log", "-1", '--pretty="%cI\t%an\t%s"', Path(file).name], capture_output=True, check=True)
                        logger.debug(f"subprocess result: '{p.stdout.decode('utf-8')}'")
                        (date, author, change) = p.stdout.decode('utf-8')[1:-2].split('\t', 2)
                        date = parse(date).astimezone(datetime.UTC).strftime("%Y-%m-%d, %H:%M")
                    except Exception as e:
                        logger.error(f"git log subprocess error: {e}")

                # remember this page for All Pages
                # strip Markdown headers and add truncated content (used for recent_pages)
                stripped_text = re.sub(r'^#+.*\n?', '', markdown_text, flags=re.MULTILINE)
                all_pages.append({
                    'title':Path(file).stem,
                    'path':Path(clean_filepath).with_suffix(".html").as_posix(),
                    'date':date,
                    'change':change,
                    'author':author,
                    'abstract':textwrap.shorten(stripped_text, width=257),
                })
            # create build results
            with open(Path(dir_output) / 'build-results.json', 'w') as outfile:
                build_results = {
                    'builder_name':APPNAME,
                    'builder_version':APPVERSION,
                    'build_time':build_time,
                }
                json.dump(build_results, outfile)
            # copy all original files
            logger.debug("Copy all original files")
            logger.debug("%s -->  %s",Path(file), Path(dir_output+clean_filepath))
            shutil.copy(Path(file), Path(dir_output+clean_filepath))

        # build Lunr search index if --lunr
        if (args[0].lunr):
            logger.debug("building lunr index: %s", lunr_index_filepath)
            # ref: https://lunrjs.com/guides/index_prebuilding.html
            pages_index_bytes = json.dumps(lunr_idx_data).encode('utf-8') # NOTE: build-index.js requires text as input - convert dict to string (then do encoding to bytes either here or set `encoding` in subprocess.run())
            with open(lunr_index_filepath, "w") as outfile:
                print("lunr_index=", end="", file=outfile)
                outfile.seek(0, 2) # seek to EOF
                p = subprocess.run(['node', 'build-index.js'], input=pages_index_bytes, stdout=outfile, check=True)
            with open(lunr_posts_filepath, "w") as outfile:
                print("lunr_posts=", lunr_posts, file=outfile)

        html = render_template('search.html')
        (Path(dir_output) / "search.html").write_text(html)

        # copy README.html to index.html if no index.html
        logger.debug("copy README.html to index.html if no index.html")
        if not (Path(dir_output) / 'index.html').exists():
            shutil.copyfile(Path(dir_output) / 'README.html', Path(dir_output) / 'index.html')

        # copy static assets directory
        logger.debug("copy static assets directory")
        if (Path(theme_dir) / 'static').exists():
            shutil.copytree(Path(theme_dir) / 'static', Path(dir_output), dirs_exist_ok=True)

        # build all-pages.html
        logger.debug("build all-pages.html")
        if args[0].commits:
            all_pages_chrono = sorted(all_pages, key=lambda i: i['date'], reverse=True)
        else:
            all_pages_chrono = ''
        all_pages = sorted(all_pages, key=lambda i: i['title'].lower())
        html = render_template('all-pages.html',
                               pages=all_pages,
                               pages_chrono=all_pages_chrono)
        (Path(dir_output) / "all-pages.html").write_text(html)

        # build recent-pages.html
        logger.debug(f"build recent-pages.html with {config['recent_changes_count']} entries.")
        no_edit_url_pages = [pattern.replace('.md', '*') for pattern in (config.get('no_edit_url_pages') or [])]
        filtered_pages = [page for page in all_pages_chrono if not any(Path(page['path']).match(no_edit) for no_edit in no_edit_url_pages)]
        recent_pages = filtered_pages[:config['recent_changes_count']]
        html = render_template('recent-pages.html',
                               pages=recent_pages)
        (Path(dir_output) / "recent-pages.html").write_text(html)

        # done
        logger.debug("done")

    except subprocess.CalledProcessError as e:
        print(f"\nERROR: '{e.cmd[0]}' returned error code {e.returncode}.")
        print(f"Output was '{e.output}'")
        if e.cmd[0] == 'node':
            print("\nYou may need to install Node modules with 'npm ci'.\n")
        if e.cmd[0] == 'git':
            print("\nThere was a problem with Git.\n")
    except jinja2.exceptions.TemplateNotFound as e:
        print(f"\nCan't find template '{e}'.\n\nTheme or files in theme appear to be missing, or theme argument set incorrectly.\n")
    except FileNotFoundError as e:
        print(f"\n{e}\n\nCheck that arguments specify valid files and directories.\n")
    except Exception as e:
        traceback.print_exc(e)
    return

# initialize new markpub directory
def init_site(directory):
    # Check the specified directory
    logger.debug(f"init directory: {directory}")
    init_dir = Path(directory).resolve()
    logger.debug(f"init_dir: {init_dir}")
    if init_dir.exists():
        # if any(init_dir.iterdir()):
         if any(glob.iglob(f"{init_dir}/**/.markpub/markpub.yaml",recursive=True)):
             logger.error(f"The directory {init_dir} has been initialized.")
             return
    else:
        # create and initialize directory
        logger.info(f"Creating directory {init_dir}")
        Path(init_dir).mkdir(parents=True, exist_ok=True)

    # Define the source template directory
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    # Copy files from templates
    try:
        # copy netlify.toml to the root of the new directory; save any existing file
        if (filename := Path(init_dir) / "netlify.toml").exists():
            shutil.copy(filename, init_dir / "netlify-prior.toml")
        shutil.copy(templates_dir / "netlify.toml", init_dir / "netlify.toml")
        # copy Sidebar.md; do not overwrite an existing [S|s]idebar.md file
        if Path(f"{init_dir}/Sidebar.md").exists() or Path(f"{init_dir}/sidebar.md").exists():
            shutil.copy(templates_dir / "Sidebar.md", init_dir / "Sidebar-new.md")
        else:
            shutil.copy(templates_dir / "Sidebar.md", init_dir / "Sidebar.md")
        # copy .gitignore to the new directory root; append if an ignore file exists
        gitignore_file = f"{init_dir}/.gitignore"
        if Path(gitignore_file).exists():
            with open(templates_dir / "gitignore-template.txt") as source, open(gitignore_file, 'a') as target:
                target.write(source.read())
        else:
            shutil.copy(templates_dir / "gitignore-template.txt", init_dir / ".gitignore")
        # copy GitHub pages workflow directory and update workflow file
        if not Path(f"{init_dir}/.github/").exists():
            shutil.copytree(templates_dir / "dot-github", init_dir / ".github")
            workflow_fname = f"{init_dir}/.github/workflows/gh-pages.yml"
            with open(workflow_fname) as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                if 'REPOSITORYNAME' in line:
                    lines[i] = line.replace('REPOSITORYNAME', Path(init_dir).stem)
                    break
            with open(workflow_fname, 'w') as file:
                file.writelines(lines)
        # copy website themes directory
#        default_theme_dir = markpub_themes.get_theme_path('dolce')
#        shutil.copytree(default_theme_dir, init_dir / ".markpub/themes/dolce")
        # create .markpub dir
        Path(f"{init_dir}/.markpub").mkdir(parents=True, exist_ok=True)
        # copy pip req'ts, javascript, and node info
        shutil.copy(templates_dir / "requirements.txt", init_dir / ".markpub" / "requirements.txt")
        shutil.copy(templates_dir / "build-index.js", init_dir / ".markpub" / "build-index.js")
        shutil.copy(templates_dir / "package.json", init_dir / ".markpub" / "package.json")
        shutil.copy(templates_dir / "package-lock.json", init_dir / ".markpub" / "package-lock.json")
        logger.debug(f"template file copy successful in {init_dir}")
    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")

    # initialize configuration file
    logger.info(f"get and write config info into {init_dir}/.markpub/markpub.yaml")
    # get configuration input
    website_title = input("Enter the website title: ")
    if not website_title: # if no title entered use init directory name
        website_title = Path(init_dir).resolve().name
    logger.debug(f"website title: {website_title}")
    author_name = input("Enter the author name(s): ")
    git_repo = input("Enter Git repository url (for Edit button; optional): ")
    if git_repo:
        git_repo = f"https://{git_repo}" if not git_repo.startswith("https://") else git_repo

    # read in markpub.yaml template
    with open(templates_dir / 'markpub-template.yaml',encoding='utf-8') as f:
        config_doc = yaml.safe_load(f)
        config_doc['wiki_title'] = website_title
        config_doc['author'] = author_name
        # 2024-11-07: edit_url supports GitHub and GitLab only
        if git_repo:
            match urlparse(git_repo).netloc:
                case 'github.com':
                    config_doc['edit_url'] = f"{git_repo}/edit/"
                case 'gitlab.com':
                    config_doc['edit_url'] = f"{git_repo}/-/edit/"
                case _:
                    config_doc['edit_url'] = ''
            config_doc['repo'] = f'<a href="{git_repo}">{git_repo.split("/")[-1]}</a>'
        else:
            config_doc['edit_url'] = ''
            config_doc['repo'] = ''

    # write out configuration information
    output_file = f'{init_dir}/.markpub/markpub.yaml'
    with open(output_file, 'w', encoding='utf-8') as file:
        yaml.safe_dump(config_doc, file, default_flow_style=False, sort_keys=False)
    return

def main():
    # setup argument parsers
    parser = argparse.ArgumentParser(description='Initialize or build a website of a collection of Markdown files.')
    parser.add_argument('--version', '-V', action='version', version=f"{APPNAME} {APPVERSION}")
    subparsers = parser.add_subparsers(required=True)
    # subparser for "init" command
    parser_init = subparsers.add_parser('init')
    parser_init.add_argument('directory', nargs=1)
    parser_init.set_defaults(cmd='init')
    # subparser for "build" command
    parser_build = subparsers.add_parser('build')
    parser_build.add_argument('-i', '--input', required=True, help='input directory of Markdown files')
    parser_build.add_argument('-o', '--output', required=True, help='output website directory')
    parser_build.add_argument('--config', '-c', default='./markpub.yaml', help='path to YAML config file')
    parser_build.add_argument('--theme', '-t', help='path to directory of HTML theme filess')
    parser_build.add_argument('--root', '-r', default='', help='name for website root directory (to host GitHub Pages)')
    parser_build.add_argument('--lunr', action='store_true', help='include this to create lunr index (requires npm and lunr to be installed, read docs)')
    parser_build.add_argument('--commits', action='store_true', help='include this to read Git commit messages and times, for All Pages')
    parser_build.set_defaults(cmd='build')

    args = parser.parse_known_args()
    logger.info(args)

    match args[0].cmd:
        case 'init':
            logger.info('Initializing in directory: %s', {args[0].directory[0]})
            init_site(args[0].directory[0])
        case 'build':
            # do not build if input directory is not initialized
            if not (Path(args[0].input) / ".markpub" / "markpub.yaml").is_file():
                logger.warning("Have you run `markpub init` yet?")
                logger.error(f"{args[0].input} does not appear to initialized. Run `markpub init -h` for instructions.")
                return
            logger.info(f'Building website in directory {args[0].output} from Markdown files in {args[0].input}')
            build_site(args)
        case _:
            return

if __name__ == '__main__':
    exit(main())
