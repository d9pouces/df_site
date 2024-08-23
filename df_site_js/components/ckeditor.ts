import ClassicEditorBase from '@ckeditor/ckeditor5-editor-classic/src/classiceditor';
import Essentials from '@ckeditor/ckeditor5-essentials/src/essentials';
import UploadAdapter from '@ckeditor/ckeditor5-adapter-ckfinder/src/uploadadapter';
import Autoformat from '@ckeditor/ckeditor5-autoformat/src/autoformat';
import Bold from '@ckeditor/ckeditor5-basic-styles/src/bold';
import Italic from '@ckeditor/ckeditor5-basic-styles/src/italic';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline';
import Strikethrough from '@ckeditor/ckeditor5-basic-styles/src/strikethrough';
import Code from '@ckeditor/ckeditor5-basic-styles/src/code';
import Subscript from '@ckeditor/ckeditor5-basic-styles/src/subscript';
import Superscript from '@ckeditor/ckeditor5-basic-styles/src/superscript';
import BlockQuote from '@ckeditor/ckeditor5-block-quote/src/blockquote';
import Heading from '@ckeditor/ckeditor5-heading/src/heading';
import Image from '@ckeditor/ckeditor5-image/src/image';
import ImageCaption from '@ckeditor/ckeditor5-image/src/imagecaption';
import ImageStyle from '@ckeditor/ckeditor5-image/src/imagestyle';
import ImageToolbar from '@ckeditor/ckeditor5-image/src/imagetoolbar';
import Link from '@ckeditor/ckeditor5-link/src/link';
import List from '@ckeditor/ckeditor5-list/src/list';
import Paragraph from '@ckeditor/ckeditor5-paragraph/src/paragraph';
import ImageResize from '@ckeditor/ckeditor5-image/src/imageresize';
import SimpleUploadAdapter from '@ckeditor/ckeditor5-upload/src/adapters/simpleuploadadapter';
import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment';
import PasteFromOffice from '@ckeditor/ckeditor5-paste-from-office/src/pastefromoffice';
import Font from '@ckeditor/ckeditor5-font/src/font';
import MediaEmbed from '@ckeditor/ckeditor5-media-embed/src/mediaembed';
import RemoveFormat from '@ckeditor/ckeditor5-remove-format/src/removeformat';
import Table from '@ckeditor/ckeditor5-table/src/table';
import TableToolbar from '@ckeditor/ckeditor5-table/src/tabletoolbar';
import TableProperties from '@ckeditor/ckeditor5-table/src/tableproperties';
import TableCellProperties from '@ckeditor/ckeditor5-table/src/tablecellproperties';
import Indent from '@ckeditor/ckeditor5-indent/src/indent';
import IndentBlock from '@ckeditor/ckeditor5-indent/src/indentblock';
import Highlight from '@ckeditor/ckeditor5-highlight/src/highlight';
import TodoList from '@ckeditor/ckeditor5-list/src/todolist';
import CodeBlock from '@ckeditor/ckeditor5-code-block/src/codeblock';
import ListProperties from '@ckeditor/ckeditor5-list/src/listproperties';
import SourceEditing from '@ckeditor/ckeditor5-source-editing/src/sourceediting';
import GeneralHtmlSupport from '@ckeditor/ckeditor5-html-support/src/generalhtmlsupport';
import ImageInsert from '@ckeditor/ckeditor5-image/src/imageinsert';
import {TableCaption} from '@ckeditor/ckeditor5-table';
import WordCount from '@ckeditor/ckeditor5-word-count/src/wordcount';
import Mention from '@ckeditor/ckeditor5-mention/src/mention';
import {Style} from '@ckeditor/ckeditor5-style';
import {HorizontalLine} from '@ckeditor/ckeditor5-horizontal-line';
import {LinkImage} from "@ckeditor/ckeditor5-link";
import {HtmlEmbed} from "@ckeditor/ckeditor5-html-embed";
import {FullPage} from '@ckeditor/ckeditor5-html-support';
import {
    SpecialCharacters,
    SpecialCharactersCurrency,
    SpecialCharactersEssentials
} from '@ckeditor/ckeditor5-special-characters';
import {FileUploader} from '@liqd/ckeditor5-file-uploader';
import {ShowBlocks} from '@ckeditor/ckeditor5-show-blocks';
import {SelectAll} from '@ckeditor/ckeditor5-select-all';
import {FindAndReplace} from '@ckeditor/ckeditor5-find-and-replace';
import {TextTransformation} from "@ckeditor/ckeditor5-typing";

class ClassicEditor extends ClassicEditorBase {
}

ClassicEditor.builtinPlugins = [
    Essentials,
    UploadAdapter,
    CodeBlock,
    Autoformat,
    Bold,
    Italic,
    Underline,
    Strikethrough,
    Code,
    Subscript,
    Superscript,
    BlockQuote,
    Heading,
    Image,
    ImageCaption,
    ImageStyle,
    ImageToolbar,
    ImageResize,
    Link,
    List,
    Paragraph,
    Alignment,
    Font,
    PasteFromOffice,
    SimpleUploadAdapter,
    MediaEmbed,
    RemoveFormat,
    Table, TableToolbar,
    TableCaption,
    TableProperties,
    TableCellProperties,
    Indent,
    IndentBlock,
    Highlight,
    TodoList,
    ListProperties,
    SourceEditing,
    GeneralHtmlSupport,
    ImageInsert,
    WordCount,
    Mention,
    Style,
    HorizontalLine,
    LinkImage,
    HtmlEmbed,
    FullPage,
    SpecialCharacters,
    SpecialCharactersEssentials,
    SpecialCharactersCurrency,
    TextTransformation,
    FileUploader,
    ShowBlocks,
    SelectAll,
    FindAndReplace
];


function getCookie (name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function initializeEditor (editorEl: HTMLElement) {
    if (
        editorEl.id.indexOf('__prefix__') !== -1 ||
        editorEl.getAttribute('data-processed') === '1'
    ) {
        return
    }
    const parentEl = editorEl.parentElement;
    const script_id = `${editorEl.id}_script`;
    editorEl.nextSibling.remove();
    const upload_url = parentEl.querySelector(
        `#${script_id}-ck-editor-5-upload-url`
    ).getAttribute('data-upload-url');
    const upload_file_types = JSON.parse(parentEl.querySelector(
        `#${script_id}-ck-editor-5-upload-url`
    ).getAttribute('data-upload-file-types'));
    const csrf_cookie_name = parentEl.querySelector(
        `#${script_id}-ck-editor-5-upload-url`
    ).getAttribute('data-csrf_cookie_name');
    const labelElement: HTMLElement = parentEl.querySelector(`[for$="${editorEl.id}"]`);
    if (labelElement) {
        labelElement.style.float = 'none';
    }

    const configContent = parentEl.querySelector(`#${script_id}-span`).textContent;
    const config = JSON.parse(
        configContent,
        (key, value) => {
            const match = value.toString().match(new RegExp('^/(.*?)/([gimy]*)$'));
            if (match) {
                return new RegExp(match[1], match[2]);
            }
            return value;
        }
    );
    const specialChars = config.specialChars;
    config.simpleUpload = {
        'uploadUrl': upload_url,
        'headers': {
            'X-CSRFToken': getCookie(csrf_cookie_name),
        },
    };

    config.fileUploader = {
        'fileTypes': upload_file_types
    };

    ClassicEditor.create(
        editorEl,
        config
    ).then(editor => {
        if (editor.plugins.has('WordCount')) {
            const wordCountPlugin = editor.plugins.get('WordCount');
            const wordCountWrapper = parentEl.querySelector(`#${script_id}-word-count`);
            wordCountWrapper.innerHTML = '';
            // @ts-ignore
            wordCountWrapper.appendChild(wordCountPlugin.wordCountContainer);
        }
        if (specialChars && (editor.plugins.has('SpecialCharacters'))) {
            editor.plugins.get('SpecialCharacters').addItems('Emoji', specialChars, {label: 'Emoji'});
        }
    }).catch(error => {
        console.error((error));
    });
    editorEl.setAttribute('data-processed', '1');
}
;

/**
 * This function initializes the CKEditor inputs within an optional element and
 * assigns properties necessary for the correct operation
 *
 * @param {HTMLElement} [element=document.body] - The element to search for elements
 *
 * @returns {void}
 */
function createEditors (element: HTMLElement = document.body): void {
    element.querySelectorAll('.django_ckeditor_5').forEach(initializeEditor);
}

document.addEventListener("DOMContentLoaded", () => {
    createEditors();
    // @ts-ignore
    if (typeof django === "object" && django.jQuery) {
        // @ts-ignore
        django.jQuery(document).on("formset:added", createEditors);
    }

});


document.addEventListener("DOMContentAdded", (evt: Event) => {
    // @ts-ignore
    createEditors(evt.target)
});
