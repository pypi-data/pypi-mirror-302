"use strict";
(self["webpackChunkjupyterlab_todo"] = self["webpackChunkjupyterlab_todo"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);


// Create a new command for your extension
const TODO_COMMAND = 'jupyterlab_todo:check-todos';
/**
 * Initialization data for the jupyterlab_todo extension.
 */
const plugin = {
    id: 'jupyterlab_todo',
    description: 'Pop up your to-do\'s in opened notebook.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, tracker) => {
        console.log('JupyterLab extension jupyterlab_todo is activated!');
        const checkForTodos = async () => {
            var _a, _b;
            // Open notebook
            const currentNotebook = tracker.currentWidget;
            if (!((_a = currentNotebook.context.contentsModel) === null || _a === void 0 ? void 0 : _a.name))
                return;
            // const cellList = currentNotebook.content.widgets;
            const cellList = (_b = currentNotebook.content.model) === null || _b === void 0 ? void 0 : _b.cells;
            if (!cellList)
                return;
            for (let index = 0; index < cellList.length; index++) {
                const cell = cellList.get(index);
                const cellJson = cell.toJSON();
                const cellText = Array.isArray(cellJson.source) ? cellJson.source.join('\n') : cellJson.source;
                const todoMatches = cellText.match(/TODO:|todo:|To do|ToDo/gi);
                if (todoMatches && todoMatches.length > 0) {
                    console.log(cellJson);
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.emit(`Found TODOs in the current notebook`, "warning", { autoClose: 3000, actions: [
                            { label: 'Go to', callback: () => {
                                    currentNotebook.content.activeCellIndex = index;
                                    if (currentNotebook.content.activeCell) {
                                        currentNotebook.content.activeCell.activate();
                                        currentNotebook.content.scrollToCell(currentNotebook.content.activeCell);
                                    }
                                } }
                        ], });
                    break;
                }
            }
        };
        tracker.currentChanged.connect(() => {
            checkForTodos();
        });
        app.commands.addCommand(TODO_COMMAND, {
            label: 'Check for TODOs',
            execute: checkForTodos,
            isVisible: () => tracker.currentWidget !== null
        });
        app.commands.addKeyBinding({
            command: TODO_COMMAND,
            keys: ['Ctrl Y'],
            selector: '.jp-Notebook'
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.bd2229b04d6b0e1fd18b.js.map