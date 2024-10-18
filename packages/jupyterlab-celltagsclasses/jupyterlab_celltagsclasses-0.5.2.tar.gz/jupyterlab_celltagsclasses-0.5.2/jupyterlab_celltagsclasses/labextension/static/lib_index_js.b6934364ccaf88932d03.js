"use strict";
(self["webpackChunkjupyterlab_celltagsclasses"] = self["webpackChunkjupyterlab_celltagsclasses"] || []).push([["lib_index_js"],{

/***/ "./lib/apply_on_cells.js":
/*!*******************************!*\
  !*** ./lib/apply_on_cells.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Scope": () => (/* binding */ Scope),
/* harmony export */   "apply_on_cells": () => (/* binding */ apply_on_cells)
/* harmony export */ });
/*
 * the logic of applying a function on a set of cells
 */
var Scope;
(function (Scope) {
    Scope[Scope["All"] = 0] = "All";
    Scope[Scope["Active"] = 1] = "Active";
    Scope[Scope["Multiple"] = 2] = "Multiple";
})(Scope || (Scope = {}));
// because this function is designed to define global commands
// we always act on notebookTracker.currentWidget
// i.e. the currently active notebook panel
const apply_on_cells = (notebookTracker, scope, to_apply) => {
    var _a;
    const notebook = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
    if (notebook === undefined) {
        // not focusing on a notebook..
        return;
    }
    let actionCells;
    if (scope === Scope.All) {
        actionCells = notebook.widgets.slice();
    }
    else {
        const activeCell = notebook.activeCell;
        if (activeCell === null) {
            return;
        }
        if (scope === Scope.Active) {
            actionCells = [activeCell];
        }
        else {
            const { anchor, head } = notebook.getContiguousSelection();
            // when only one cell is selected/active, both are null
            if (anchor === null || head === null) {
                actionCells = [activeCell];
            }
            else {
                actionCells = notebook.widgets.slice(anchor, head + 1);
            }
        }
    }
    // console.log(`apply_on_cells with scope=${scope} on ${actionCells.length} cells`)
    actionCells.forEach(to_apply);
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Scope": () => (/* reexport safe */ _apply_on_cells__WEBPACK_IMPORTED_MODULE_4__.Scope),
/* harmony export */   "apply_on_cells": () => (/* reexport safe */ _apply_on_cells__WEBPACK_IMPORTED_MODULE_4__.apply_on_cells),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "md_clean": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_clean),
/* harmony export */   "md_get": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_get),
/* harmony export */   "md_has": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_has),
/* harmony export */   "md_insert": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_insert),
/* harmony export */   "md_remove": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_remove),
/* harmony export */   "md_set": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_set),
/* harmony export */   "md_toggle": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_toggle),
/* harmony export */   "md_toggle_multi": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_toggle_multi),
/* harmony export */   "md_unset": () => (/* reexport safe */ _metadata__WEBPACK_IMPORTED_MODULE_3__.md_unset)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _test_commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./test_commands */ "./lib/test_commands.js");
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");
/* harmony import */ var _apply_on_cells__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./apply_on_cells */ "./lib/apply_on_cells.js");
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */



// turn that to true to do manual tests of apply_on_cells
const SHIP_TEST_COMMANDS = true;
/**
 * Initialization data for the jupyterlab-celltagsclasses extension.
 */
const plugin = {
    id: 'jupyterlab-celltagsclasses:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, notebookTracker, palette) => {
        console.log('extension jupyterlab-celltagsclasses is activating');
        if (SHIP_TEST_COMMANDS) {
            (0,_test_commands__WEBPACK_IMPORTED_MODULE_2__.create_test_commands)(app, notebookTracker, palette);
        }
        const class_for_tag = (tag) => {
            if (tag[0] === '-')
                return tag.slice(1);
            else
                return `cell-tag-${tag}`;
        };
        notebookTracker.widgetAdded.connect((_, panel) => {
            const notebookModel = panel.content.model;
            if (notebookModel === null) {
                return;
            }
            notebookModel.cells.changed.connect((cellList, change) => {
                if (change.type !== 'add') {
                    return;
                }
                change.newValues.forEach(cellModel => {
                    var _a;
                    // compute widgets attached to cellModel
                    const cellWidgets = panel.content.widgets.filter((cell, index) => cell.model.id === cellModel.id);
                    if (cellWidgets === undefined || (cellWidgets === null || cellWidgets === void 0 ? void 0 : cellWidgets.length) === 0) {
                        // console.warn('could not find cell widget for cell model', cellModel)
                        return;
                    }
                    // console.debug( `found ${cellWidgets?.length} cell widgets`, cellWidgets[0] )
                    // add classes for pre-existing tags
                    (_a = cellModel.getMetadata('tags')) === null || _a === void 0 ? void 0 : _a.forEach((tag) => cellWidgets === null || cellWidgets === void 0 ? void 0 : cellWidgets.forEach(cellWidget => {
                        // console.debug( `adding initial class for tag ${class_for_tag(tag)}` )
                        cellWidget.addClass(class_for_tag(tag));
                    }));
                    // react to changes in tags
                    cellModel.metadataChanged.connect((sender, change) => {
                        // console.debug('metadata changed', sender, change)
                        if (change.key !== 'tags') {
                            // console.debug("ignoring non-tags metadata change")
                            return;
                        }
                        // does not seem useful to recompute this
                        // const cellWidgets = panel.content.widgets.filter(
                        //   (cell: Cell, index: number) => (cell.model.id === cellModel.id)
                        // )
                        if (change.type === 'change') {
                            // console.debug('change', change, change.newValue)
                            // compute difference between old and new tags
                            const oldTags = change.oldValue;
                            const newTags = change.newValue;
                            const addedTags = newTags.filter(tag => !oldTags.includes(tag));
                            const removedTags = oldTags.filter(tag => !newTags.includes(tag));
                            // console.debug('addedTags', addedTags)
                            // console.debug('removedTags', removedTags)
                            cellWidgets.forEach(cellWidget => {
                                addedTags.forEach(tag => {
                                    console.debug(`adding class for tag ${class_for_tag(tag)}`);
                                    cellWidget.addClass(class_for_tag(tag));
                                });
                                removedTags.forEach(tag => {
                                    console.debug(`removing class for tag ${class_for_tag(tag)}`);
                                    cellWidget.removeClass(class_for_tag(tag));
                                });
                            });
                        }
                        else if (change.type === 'add') {
                            console.debug('celltagsclasses: add', change, change.newValue);
                            cellWidgets.forEach(cellWidget => {
                                for (const tag of change.newValue) {
                                    // console.debug(`adding class for tag ${class_for_tag(tag)}`)
                                    cellWidget.addClass(class_for_tag(tag));
                                }
                            });
                        }
                        else if (change.type === 'remove') {
                            console.debug('celltagsclasses: remove', change, change.newValue);
                            cellWidgets.forEach(cellWidget => {
                                for (const tag of change.newValue) {
                                    // console.debug(`removing class for tag ${class_for_tag(tag)}`)
                                    cellWidget.removeClass(class_for_tag(tag));
                                }
                            });
                        }
                    });
                });
            });
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
// re-export metadata helper functions




/***/ }),

/***/ "./lib/metadata.js":
/*!*************************!*\
  !*** ./lib/metadata.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "md_clean": () => (/* binding */ md_clean),
/* harmony export */   "md_get": () => (/* binding */ md_get),
/* harmony export */   "md_has": () => (/* binding */ md_has),
/* harmony export */   "md_insert": () => (/* binding */ md_insert),
/* harmony export */   "md_remove": () => (/* binding */ md_remove),
/* harmony export */   "md_set": () => (/* binding */ md_set),
/* harmony export */   "md_toggle": () => (/* binding */ md_toggle),
/* harmony export */   "md_toggle_multi": () => (/* binding */ md_toggle_multi),
/* harmony export */   "md_unset": () => (/* binding */ md_unset)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _xpath__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./xpath */ "./lib/xpath.js");
/* eslint-disable prettier/prettier */
//
// Metadata helper tools
// a xpath can be either a dot-separated string, or an array of strings
//
//  single valued metadata:
//
// (*) md_get: get a metadata value
//         e.g. md_get(cell, "some.path.in.the.metadata")
//           or md_get(cell, "some.path.in.the.metadata", "default value")
//           or md_get(cell, ["some", "path", "in", "the", "metadata"])
// (*) md_set: set a metadata value
//         e.g. md_set(cell, "some.path.in.the.metadata", "new value")
// (*) md_unset: unset a metadata value
//         e.g. md_unset(cell, "some.path.in.the.metadata")
//
//  list valued metadata (typically xpath = 'tags')
//
// (*) md_has: check if a value is present in a metadata list
//         e.g. md_has(cell, "path.to.tags", "tag-to-check")
// (*) md_insert: insert a value in a metadata list
//         e.g. md_insert(cell, "path.to.tags", "added-tag")
// (*) md_remove: remove a value from a metadata list
//         e.g. md_remove(cell, "path.to.tags", "removed-tag")
// (*) md_toggle: toggle a value in a metadata list
//         e.g. md_toggle(cell, "path.to.tags", "toggled-tag")
// (*) md_toggle_multi: toggle a value in a metadata list,
//        removing the other values in the lists
//
// clean up
// (*) md_clean: remove empty metadata elements
//         e.g. md_clean(cell, "path.to.subtree")
//         or more typically
//              md_clean(cell, "")
//          will alter the cell's metadata so as to remove empty lists or empty keys


// atomic values
const md_get = (cell, xpath, if_missing) => {
    if (cell instanceof _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.Cell) {
        cell = cell.model;
    }
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.getMetadata(first);
    if (start === undefined) {
        return if_missing;
    }
    else {
        return (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_get)(start, tail);
    }
};
const md_set = (cell, xpath, value) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.model.getMetadata(first);
    if (tail.length === 0) {
        cell.model.setMetadata(first, value);
        return value;
    }
    const subtree = start || {};
    const retcod = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_set)(subtree, tail, value);
    cell.model.setMetadata(first, subtree);
    return retcod;
};
const md_unset = (cell, xpath) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.model.getMetadata(first);
    if (start === undefined) {
        return false;
    }
    if (tail.length === 0) {
        cell.model.deleteMetadata(first);
        return true;
    }
    else {
        const retcod = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_unset)(start, tail);
        cell.model.setMetadata(first, start);
        return retcod;
    }
};
// lists (e.g. tags)
const md_has = (cell, xpath, key) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.model.getMetadata(first);
    if (start === undefined) {
        return false;
    }
    const list = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_get)(start, tail);
    if (list === undefined) {
        return false;
    }
    return list.indexOf(key) >= 0;
};
const md_insert = (cell, xpath, key) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.model.getMetadata(first);
    if (tail.length === 0) {
        let sublist;
        if (start !== undefined) {
            sublist = start;
            // use another object as otherwise .setMetadata() does not seem to propagate
            sublist = sublist.slice();
        }
        else {
            sublist = [];
        }
        if (sublist.indexOf(key) < 0) {
            sublist.push(key);
            cell.model.setMetadata(first, sublist);
            return key;
        }
        else {
            return undefined;
        }
    }
    else {
        const subtree = start || {};
        const retcod = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_insert)(subtree, tail, key);
        cell.model.setMetadata(first, subtree);
        return retcod;
    }
};
const md_remove = (cell, xpath, key) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    const start = cell.model.getMetadata(first);
    if (start === undefined) {
        return undefined;
    }
    if (tail.length === 0) {
        const sublist = start;
        if (!(sublist instanceof Array)) {
            return undefined;
        }
        // use another object as otherwise .set() does not seem to propagate
        const copy = sublist.slice();
        const index = copy.indexOf(key);
        if (index < 0) {
            return undefined;
        }
        // const as_array = sublist as Array<string>
        copy.splice(index, 1);
        cell.model.setMetadata(first, copy);
        return key;
    }
    else {
        const subtree = start;
        const retcod = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_remove)(subtree, tail, key);
        cell.model.setMetadata(first, subtree);
        return retcod;
    }
};
const md_toggle = (cell, xpath, key) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    if (!md_has(cell, xpath, key)) {
        return md_insert(cell, xpath, key);
    }
    else {
        return md_remove(cell, xpath, key);
    }
};
/*
 * given a within_set of mututally exclusive keys
 * e.g. within_set = ['level1', 'level2', 'level3']
 * and a key to toggle
 * md_toggle_multi will toggle the key and unset the other keys
 * in the event where key is not in within_set
 * the effect of this function is to clear all keys in within_set
 */
const md_toggle_multi = (cell, xpath, key, within_set) => {
    if (within_set.includes(key)) {
        md_toggle(cell, xpath, key);
    }
    for (const other_key of within_set) {
        if (other_key !== key) {
            md_remove(cell, xpath, other_key);
        }
    }
};
const md_clean = (cell, xpath) => {
    xpath = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.normalize)(xpath);
    const [first, ...tail] = xpath;
    if (first === undefined) {
        console.log(cell.model.metadata);
        // no xpath, clean the whole metadata
        for (const key of Object.entries(cell.model.metadata)) {
            const xpath = key;
            const new_value = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_clean)(md_get(cell, xpath), '');
            if (new_value === undefined || new_value.length === 0) {
                md_unset(cell, xpath);
            }
            else {
                md_set(cell, xpath, new_value);
            }
        }
    }
    else {
        const subtree = md_get(cell, first);
        const new_value = (0,_xpath__WEBPACK_IMPORTED_MODULE_1__.xpath_clean)(subtree, tail);
        if (new_value === undefined || new_value.length === 0) {
            md_unset(cell, first);
        }
        else {
            md_set(cell, first, new_value);
        }
    }
};


/***/ }),

/***/ "./lib/test_commands.js":
/*!******************************!*\
  !*** ./lib/test_commands.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "create_test_commands": () => (/* binding */ create_test_commands)
/* harmony export */ });
/* harmony import */ var _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./apply_on_cells */ "./lib/apply_on_cells.js");

// apply_on_cell calls action on a Cell (Widget) object
// use cell.model if a CellModel is needed
const cell_action = (cell) => {
    console.log('cell_action on', cell.node);
};
// act on models
// like so for example
const model_action = (cell) => {
    console.log('model_action on', cell.node);
    const model = cell.model;
    const source = cell.model.sharedModel.getSource();
    model.sharedModel.setSource(source.toUpperCase());
};
const create_test_commands = (app, notebookTracker, palette) => {
    const add_command = (suffix, label, scope, keys, the_function) => {
        const command = `celltagsclasses:${suffix}`;
        app.commands.addCommand(command, {
            label,
            execute: () => {
                console.log(label);
                (0,_apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.apply_on_cells)(notebookTracker, scope, the_function);
            },
        });
        palette.addItem({ command, category: 'celltagsclasses' });
        app.commands.addKeyBinding({
            command,
            keys,
            selector: '.jp-Notebook',
        });
    };
    // MODEL
    add_command('single-model', 'perform model action on single active cell', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.Active, ['Alt-K', 'Alt-1'], model_action);
    add_command('multiple-model', 'perform model action on multiple selected cells', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.Multiple, ['Alt-K', 'Alt-2'], model_action);
    add_command('all-model', 'perform model action on all cells', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.All, ['Alt-K', 'Alt-3'], model_action);
    // CELL
    add_command('single-cell', 'perform action on single active cell', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.Active, ['Alt-K', 'Alt-4'], cell_action);
    add_command('multiple-cell', 'perform action on multiple selected cells', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.Multiple, ['Alt-K', 'Alt-5'], cell_action);
    add_command('all-cell', 'perform action on all cells', _apply_on_cells__WEBPACK_IMPORTED_MODULE_0__.Scope.All, ['Alt-K', 'Alt-6'], cell_action);
};


/***/ }),

/***/ "./lib/xpath.js":
/*!**********************!*\
  !*** ./lib/xpath.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "normalize": () => (/* binding */ normalize),
/* harmony export */   "xpath_clean": () => (/* binding */ xpath_clean),
/* harmony export */   "xpath_get": () => (/* binding */ xpath_get),
/* harmony export */   "xpath_insert": () => (/* binding */ xpath_insert),
/* harmony export */   "xpath_remove": () => (/* binding */ xpath_remove),
/* harmony export */   "xpath_set": () => (/* binding */ xpath_set),
/* harmony export */   "xpath_unset": () => (/* binding */ xpath_unset)
/* harmony export */ });
/* eslint-disable no-case-declarations */
/* eslint-disable prettier/prettier */
// helpers to manage a JS object
//
// in this module we are only concerned about doing side effects
// in a JavaScript object
// what to do on the passed object
var Action;
(function (Action) {
    Action[Action["Get"] = 0] = "Get";
    Action[Action["Set"] = 1] = "Set";
    Action[Action["Unset"] = 2] = "Unset";
    Action[Action["Insert"] = 3] = "Insert";
    Action[Action["Remove"] = 4] = "Remove";
})(Action || (Action = {}));
const normalize = (xpath) => {
    if (typeof xpath === 'string') {
        const string = xpath;
        if (string.length === 0) {
            return [];
        }
        return string.split('.');
    }
    else if (xpath instanceof Array) {
        return xpath;
    }
    else {
        console.error(`xpath must be string or array, got ${xpath}`);
        return [];
    }
};
const _manage_metadata = (data, // intended to be cell.metadata
action, xpath, value) => {
    const { Get, Set, Unset, Insert, Remove } = Action;
    const recurse = (scanner, action, xpath, value) => {
        // console.log(`in recurse with xpath=${xpath}`)
        if (xpath.length === 0) {
            switch (action) {
                case Get:
                    return scanner;
                default:
                    return undefined;
            }
        }
        else if (xpath.length === 1) {
            const [step] = xpath;
            //
            switch (action) {
                case Get:
                    return scanner[step];
                case Set:
                    scanner[step] = value;
                    return value;
                case Unset:
                    if (step in scanner) {
                        delete scanner[step];
                        return true;
                    }
                    else {
                        return false;
                    }
                case Insert:
                    // create list if needed
                    if (!(step in scanner)) {
                        scanner[step] = [];
                    }
                    if (!(scanner[step] instanceof Array)) {
                        return undefined;
                    }
                    // insert if not already present
                    {
                        const list = scanner[step];
                        if (list.indexOf(value) < 0) {
                            list.push(value);
                            return value;
                        }
                        else {
                            return undefined;
                        }
                    }
                case Remove:
                    if (!(scanner[step] instanceof Array)) {
                        return undefined;
                    }
                    const list = scanner[step];
                    // list.pop(value) is not accepted by ts ?!?
                    const index = list.indexOf(value);
                    if (index >= 0) {
                        list.splice(index, 1);
                    }
                    return value;
            }
        }
        else {
            const [first, ...rest] = xpath;
            if (first in scanner) {
                if (!(scanner[first] instanceof Object)) {
                    return undefined;
                }
                else {
                    const next = scanner[first];
                    return recurse(next, action, rest, value);
                }
            }
            else {
                switch (action) {
                    case Get:
                        return undefined;
                    case Set:
                        scanner[first] = {};
                        const next = scanner[first];
                        return recurse(next, action, rest, value);
                    case Unset:
                        return undefined;
                    case Insert:
                        if (rest.length === 0) {
                            scanner[first] = [];
                            return recurse(scanner[first], action, rest, value);
                        }
                        else {
                            scanner[first] = {};
                            return recurse(scanner[first], action, rest, value);
                        }
                    case Remove:
                        return undefined;
                }
            }
        }
    };
    const xpath_list = normalize(xpath);
    return recurse(data, action, xpath_list, value);
};
const _clean_metadata = (data, xpath) => {
    const not_empty = (x) => {
        if (x instanceof Array) {
            return x.length !== 0;
        }
        else if (x instanceof Object) {
            return Object.keys(x).length !== 0;
        }
        else if (typeof x === 'string') {
            return x.length !== 0;
        }
        else {
            return true;
        }
    };
    const clean_array = (data) => {
        return data.map(clean).filter(not_empty);
    };
    const clean_object = (data) => {
        const result = {};
        for (const key in data) {
            const value = data[key];
            const cleaned = clean(value);
            if (not_empty(cleaned)) {
                result[key] = cleaned;
            }
        }
        return result;
    };
    const clean = (data) => {
        if (data instanceof Array) {
            return clean_array(data);
        }
        else if (data instanceof Object) {
            return clean_object(data);
        }
        else {
            return data;
        }
    };
    const xpath_list = normalize(xpath);
    if (xpath_list.length === 0) {
        return clean(data);
    }
    else {
        const start = xpath_get(data, xpath_list);
        if (start === undefined) {
            // nothing serious here, just a debug message
            //console.debug(`DBG: xpath_clean: nothing to clean at ${xpath} - from ${xpath_list}`)
            return data;
        }
        else {
            return xpath_set(data, xpath_list, clean(start));
        }
    }
};
const xpath_get = (metadata, xpath) => _manage_metadata(metadata, Action.Get, xpath, undefined);
const xpath_set = (metadata, xpath, value) => _manage_metadata(metadata, Action.Set, xpath, value);
const xpath_unset = (metadata, xpath) => _manage_metadata(metadata, Action.Unset, xpath, undefined);
const xpath_insert = (metadata, xpath, key) => _manage_metadata(metadata, Action.Insert, xpath, key);
const xpath_remove = (metadata, xpath, key) => _manage_metadata(metadata, Action.Remove, xpath, key);
const xpath_clean = (metadata, xpath) => _clean_metadata(metadata, xpath);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.b6934364ccaf88932d03.js.map