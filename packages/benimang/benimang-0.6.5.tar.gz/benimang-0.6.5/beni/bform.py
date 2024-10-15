import importlib.resources
import json
from typing import Any

import webview

from beni.btype import Null


def show(
    itemList: Any,
    *,
    title: str = '标题',
    width: int = 500,
    height: int = 400,
    labelWidth: int = 160,
    resizable: bool = False,
    debug: bool = False,
):
    '''
    bform.show([
        bform.makeInputItem('username', 'Username', placeholder='Enter your username'),
        bform.makePasswordItem('password', 'Password', placeholder='Enter your password'),
        bform.makeCheckboxItem('remember', 'Remember', label='Remember me'),
    ])
    '''

    with importlib.resources.path('beni.resources.web-form', 'index.html') as file:

        result = Null

        class Api():

            def done(self, value: Any):
                nonlocal result
                result = value
                window.destroy()

        def init():
            value = json.dumps({
                'labelWidth': f'{labelWidth}px',
                'itemList': itemList,
            })
            window.evaluate_js('window.__show( JSON.parse(`' + value + '`) );')

        window = webview.create_window(
            title,
            str(file),
            js_api=Api(),
            width=width,
            height=height,
            resizable=resizable,
        )
        webview.start(init, debug=debug)

        return result


def makeInputItem(
    key: str,
    name: str,
    *,
    value: str = '',
    placeholder: str = '',
    autofocus: bool = False,
):
    type = 'InputItem'  # type: ignore
    return locals()


def makePasswordItem(
    key: str,
    name: str,
    *,
    value: str = '',
    placeholder: str = '',
    autofocus: bool = False,
):
    type = 'PasswordItem'  # type: ignore
    return locals()


def makeTextareaItem(
    key: str,
    name: str,
    *,
    value: str = '',
    placeholder: str = '',
    autofocus: bool = False,
    rows: int = 3,
):
    type = 'TextareaItem'  # type: ignore
    return locals()


def makeCheckboxItem(
    key: str,
    name: str,
    *,
    value: bool = False,
    text: str = '',
):
    type = 'CheckboxItem'  # type: ignore
    return locals()


def makeTextItem(
    key: str,
    name: str,
    *,
    text: str = '',
):
    type = 'TextItem'  # type: ignore
    return locals()


def makeRadioGroupItem(
    key: str,
    name: str,
    *,
    value: Any = None,
    options: list[tuple[str, Any]] = [],
):
    type = 'RadioGroupItem'  # type: ignore
    return locals()
