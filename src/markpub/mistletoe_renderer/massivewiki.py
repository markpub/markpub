"""
Massive Wiki support for mistletoe.
"""
# set up logging
import logging
logger = logging.getLogger('markpub.massivewiki')

from itertools import chain
from mistletoe import Document
from mistletoe.block_token import BlockToken
from mistletoe.span_token import SpanToken
from mistletoe.html_renderer import HTMLRenderer
from pathlib import Path
import html
import re

__all__ = ['RawHtml', 'DoubleSquareBracketLink', 'EmbeddedImageDoubleSquareBracketLink', 'TranscludedDoubleSquareBracketLink', 'MassiveWikiRenderer']

class RawHtml(BlockToken):
    pattern = re.compile(r'\{\< ([^>]*) \>\}')

    def __init__(self, match):
        logger.debug(f"RAWHTML match: {match}")
        self.target = match

    @staticmethod
    def start(line):
        return RawHtml.pattern.match(line) is not None

class DoubleSquareBracketLink(SpanToken):
    """
    Defines double square bracket link (span).
    """
    pattern = re.compile(r"\[\[ *(.+?) *(\| *.+?)? *\]\]")

    def __init__(self, match):
        if match.group(2):
            self.target = re.sub(r"^\| *", '', match.group(2), count=1)
        else:
            self.target = match.group(1)

class EmbeddedImageDoubleSquareBracketLink(SpanToken):
    """
    Defines embedded image double square bracket link (span).
    """
    pattern = re.compile(r"\!\[\[ *(.+?)\.(png|jpg|jpeg|gif|svg|webp) *(\| *.+?)? *\]\]")

    def __init__(self, match):
        # get alt text into target and filename into content
        self.content = match.group(1) + '.' + match.group(2)
        if match.group(3):
            self.target = re.sub(r"^\| *", '', match.group(3), count=1)
        else:
            self.target = ''

class TranscludedDoubleSquareBracketLink(SpanToken):
    """
    Defines double square bracket link (span) for Markdown note transclusion
    """
    pattern = re.compile(r"!\[\[ *([^.|\]]+?)\]\]")

    def __init__(self, match):
        self.target = match.group(1)

class MassiveWikiRenderer(HTMLRenderer):
    """
    Extends HTMLRenderer to handle wiki-links, images, transclusion, and raw html

    Args:
        rootdir (string): directory path to prepend to all links, defaults to '/'.
        fileroot (string): local filesystem path to the root of the wiki, so we can read transcluded pages.

    Properties:
        links (array of strings, read-only): all of the double square bracket link targets found in this invocation.
    """
    def __init__(self, rootdir='/', fileroot='.', wikilinks={}, file_id='', websiteroot=''):
        super().__init__(*chain([RawHtml,TranscludedDoubleSquareBracketLink,EmbeddedImageDoubleSquareBracketLink,DoubleSquareBracketLink]))
        self._rootdir = rootdir
        self._fileroot = fileroot
        self._wikilinks = wikilinks
        self._file_id = file_id
        self._tc_dict = dict.fromkeys([self._file_id], [])
        self._tc_dict[self._file_id].append(self._file_id)
        self._websiteroot = websiteroot

    def render_raw_html(self, token):
        logger.debug(f"RAWHTML token: {token}")
        logger.debug(f"RAWHTML token target: {token.target}")
        if len(token.target) == 1:
            target = token.target[0].replace('{< ','<').replace(' >}\n','>')
        elif len(token.target) >= 3:
            tag_start = token.target[0].replace('{< ','<').replace(' >}','>')
            tag_end = token.target[-1].replace('{< ','<').replace(' >}\n','>')
            logger.debug(f"RAWHTML between_tags: {''.join(token.target[1:-1])}")
            between_tags = self.render(Document(''.join(token.target[1:-1])))
            target = f"{tag_start}{between_tags}{tag_end}"
        else:
            target = token.target
        template = '{target}'
        return template.format(target=target)

    def render_double_square_bracket_link(self, token):
        logger.debug("WIKILINKED token: %s", token)
        target = token.target
        logger.debug("WIKILINKED token.target: %s", token.target)
        logger.debug("WIKILINKED inner(token): %s", self.render_inner(token))
        wikilink_key = html.unescape(Path(self.render_inner(token)).name).lower()
        logger.debug("WIKILINKED wikilink_key: %s", wikilink_key)
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logger.debug("WIKILINKED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
            template = '<a class="wikilink" href="{websiteroot}{rootdir}{inner}">{target}</a>'
        else:
            inner = self.render_inner(token)
            template = '<span class="incipient-wikilink">{target}</span>'
        logger.debug("WIKILINKED inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir, websiteroot=self._websiteroot)

    def render_embedded_image_double_square_bracket_link(self, token):
        logger.debug("EMBEDDED token: %s", token)
        template = '<img src="{websiteroot}{rootdir}{inner}" alt="{target}" />'
        target = token.target
        if not target:
            target = "an image with no alt text"
        logger.debug("EMBEDDED token.target: %s", token.target)
        logger.debug("EMBEDDED token.content: %s", token.content)
        logger.debug("EMBEDDED inner(token): %s", self.render_inner(token))
        wikilink_key = token.content.lower()
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logger.debug("EMBEDDED wikilink_key: %s", wikilink_key)
        logger.debug("EMBEDDED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            inner = Path(wikilink_value['html_path']).relative_to(self._rootdir).as_posix()
        else:
            inner = token.content
        logger.debug("EMBEDDED inner: %s", inner)
        return template.format(target=target, inner=inner, rootdir=self._rootdir, websiteroot=self._websiteroot)

    def render_transcluded_double_square_bracket_link(self, token):
        logger.debug("TRANSCLUDED file_id: %s", self._file_id)
        logger.debug("TRANSCLUDED fileroot: %s", self._fileroot)
        logger.debug("TRANSCLUDED token: %s", token)
        target = token.target
        logger.debug("TRANSCLUDED token.target: %s", token.target)
        inner = self.render_inner(token)
        logger.debug("TRANSCLUDED inner(token): %s", self.render_inner(token))
        wikilink_key = html.unescape(Path(self.render_inner(token)).name).lower()
        logger.debug("TRANSCLUDED wikilink_key: %s", wikilink_key)
        wikilink_value = self._wikilinks.get(wikilink_key, None)
        logger.debug("TRANSCLUDED wikilink_value: %s", wikilink_value)
        if wikilink_value:
            logger.debug("TRANSCLUDED wikipage_id: %s", wikilink_value['wikipage_id'])
            if any(wikilink_value['wikipage_id'] in x for x in self._tc_dict[self._file_id]):
                logger.debug("*** ruh roh! there is a transclude loop")
                template = '<p><span class="transclusion-error">Cannot transclude <strong>{inner}</strong> within itself.</span></p>'
            else:
                self._tc_dict[self._file_id].append(wikilink_value['wikipage_id'])
                logger.debug("TRANSCLUDED _tc_dict: %s", self._tc_dict)
                transclude_path = f"{self._fileroot}{wikilink_value['fs_path']}"
                logger.debug(f"TRANSCLUDED loading contents of '{transclude_path}'")
                with open(transclude_path) as infile:
                    inner = infile.read()
                rendered_doc = self.render(Document(inner))
                htmlpath = wikilink_value['html_path']
                template = f'<p><a href="{self._websiteroot}{htmlpath}" style="float:right">🔗</a> {rendered_doc} </p>'
        else:
            template = '<p><span class="transclusion-error">TRANSCLUSION {target} NOT FOUND</span></p>'
        return template.format(target=target, inner=inner, rootdir=self._rootdir)
