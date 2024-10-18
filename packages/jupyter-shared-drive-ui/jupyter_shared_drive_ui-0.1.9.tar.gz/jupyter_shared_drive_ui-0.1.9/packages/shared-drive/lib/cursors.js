// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Annotation, EditorSelection, Facet } from '@codemirror/state';
import { EditorView, hoverTooltip, layer, RectangleMarker, tooltips, ViewPlugin } from '@codemirror/view';
import { JSONExt } from '@lumino/coreutils';
import { createAbsolutePositionFromRelativePosition, createRelativePositionFromJSON, createRelativePositionFromTypeIndex } from 'yjs';
/**
 * Facet storing the Yjs document objects
 */
const editorAwarenessFacet = Facet.define({
    combine(configs) {
        return configs[configs.length - 1];
    }
});
/**
 * Remote selection theme
 */
const remoteSelectionTheme = EditorView.baseTheme({
    '.jp-remote-cursor': {
        borderLeft: '1px solid black',
        marginLeft: '-1px'
    },
    '.jp-remote-cursor.jp-mod-primary': {
        borderLeftWidth: '2px'
    },
    '.jp-remote-selection': {
        opacity: 0.5
    },
    '.cm-tooltip': {
        border: 'none'
    },
    '.cm-tooltip .jp-remote-userInfo': {
        color: 'var(--jp-ui-inverse-font-color0)',
        padding: '0px 2px'
    }
});
// TODO fix which user needs update
const remoteSelectionsAnnotation = Annotation.define();
/**
 * Wrapper around RectangleMarker to be able to set the user color for the remote cursor and selection ranges.
 */
class RemoteMarker {
    /**
     * Constructor
     *
     * @param style Specific user style to be applied on the marker element
     * @param marker {@link RectangleMarker} to wrap
     */
    constructor(style, marker) {
        this.style = style;
        this.marker = marker;
    }
    draw() {
        const elt = this.marker.draw();
        for (const [key, value] of Object.entries(this.style)) {
            // @ts-expect-error Unknown key
            elt.style[key] = value;
        }
        return elt;
    }
    eq(other) {
        return (this.marker.eq(other.marker) && JSONExt.deepEqual(this.style, other.style));
    }
    update(dom, oldMarker) {
        for (const [key, value] of Object.entries(this.style)) {
            // @ts-expect-error Unknown key
            dom.style[key] = value;
        }
        return this.marker.update(dom, oldMarker.marker);
    }
}
/**
 * Extension defining a new editor layer storing the remote user cursors
 */
const remoteCursorsLayer = layer({
    above: true,
    markers(view) {
        const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
        const ydoc = ytext.doc;
        const cursors = [];
        awareness.getStates().forEach((state, clientID) => {
            var _a, _b, _c;
            if (clientID === awareness.doc.clientID) {
                return;
            }
            const cursors_ = state.cursors;
            for (const cursor of cursors_ !== null && cursors_ !== void 0 ? cursors_ : []) {
                if (!(cursor === null || cursor === void 0 ? void 0 : cursor.anchor) || !(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                    return;
                }
                const anchor = createAbsolutePositionFromRelativePosition(cursor.anchor, ydoc);
                const head = createAbsolutePositionFromRelativePosition(cursor.head, ydoc);
                if ((anchor === null || anchor === void 0 ? void 0 : anchor.type) !== ytext || (head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                    return;
                }
                const className = ((_a = cursor.primary) !== null && _a !== void 0 ? _a : true)
                    ? 'jp-remote-cursor jp-mod-primary'
                    : 'jp-remote-cursor';
                const cursor_ = EditorSelection.cursor(head.index, head.index > anchor.index ? -1 : 1);
                for (const piece of RectangleMarker.forRange(view, className, cursor_)) {
                    // Wrap the rectangle marker to set the user color
                    cursors.push(new RemoteMarker({ borderLeftColor: (_c = (_b = state.user) === null || _b === void 0 ? void 0 : _b.color) !== null && _c !== void 0 ? _c : 'black' }, piece));
                }
            }
        });
        return cursors;
    },
    update(update, layer) {
        return !!update.transactions.find(t => t.annotation(remoteSelectionsAnnotation));
    },
    class: 'jp-remote-cursors'
});
/**
 * Tooltip extension to display user display name at cursor position
 */
const userHover = hoverTooltip((view, pos) => {
    var _a;
    const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
    const ydoc = ytext.doc;
    for (const [clientID, state] of awareness.getStates()) {
        if (clientID === awareness.doc.clientID) {
            continue;
        }
        for (const cursor of (_a = state.cursors) !== null && _a !== void 0 ? _a : []) {
            if (!(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                continue;
            }
            const head = createAbsolutePositionFromRelativePosition(cursor.head, ydoc);
            if ((head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                continue;
            }
            // Use some margin around the cursor to display the user.
            if (head.index - 3 <= pos && pos <= head.index + 3) {
                return {
                    pos: head.index,
                    above: true,
                    create: () => {
                        var _a, _b, _c, _d;
                        const dom = document.createElement('div');
                        dom.classList.add('jp-remote-userInfo');
                        dom.style.backgroundColor = (_b = (_a = state.user) === null || _a === void 0 ? void 0 : _a.color) !== null && _b !== void 0 ? _b : 'darkgrey';
                        dom.textContent =
                            (_d = (_c = state.user) === null || _c === void 0 ? void 0 : _c.display_name) !== null && _d !== void 0 ? _d : 'Anonymous';
                        return { dom };
                    }
                };
            }
        }
    }
    return null;
}, {
    hideOn: (tr, tooltip) => !!tr.annotation(remoteSelectionsAnnotation),
    hoverTime: 0
});
/**
 * Extension defining a new editor layer storing the remote selections
 */
const remoteSelectionLayer = layer({
    above: false,
    markers(view) {
        const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
        const ydoc = ytext.doc;
        const cursors = [];
        awareness.getStates().forEach((state, clientID) => {
            var _a, _b, _c;
            if (clientID === awareness.doc.clientID) {
                return;
            }
            const cursors_ = state.cursors;
            for (const cursor of cursors_ !== null && cursors_ !== void 0 ? cursors_ : []) {
                if (((_a = cursor.empty) !== null && _a !== void 0 ? _a : true) || !(cursor === null || cursor === void 0 ? void 0 : cursor.anchor) || !(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                    return;
                }
                const anchor = createAbsolutePositionFromRelativePosition(cursor.anchor, ydoc);
                const head = createAbsolutePositionFromRelativePosition(cursor.head, ydoc);
                if ((anchor === null || anchor === void 0 ? void 0 : anchor.type) !== ytext || (head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                    return;
                }
                const className = 'jp-remote-selection';
                for (const piece of RectangleMarker.forRange(view, className, EditorSelection.range(anchor.index, head.index))) {
                    // Wrap the rectangle marker to set the user color
                    cursors.push(new RemoteMarker({ backgroundColor: (_c = (_b = state.user) === null || _b === void 0 ? void 0 : _b.color) !== null && _c !== void 0 ? _c : 'black' }, piece));
                }
            }
        });
        return cursors;
    },
    update(update, layer) {
        return !!update.transactions.find(t => t.annotation(remoteSelectionsAnnotation));
    },
    class: 'jp-remote-selections'
});
/**
 * CodeMirror extension exchanging and displaying remote user selection ranges (including cursors)
 */
const showCollaborators = ViewPlugin.fromClass(class {
    constructor(view) {
        this.editorAwareness = view.state.facet(editorAwarenessFacet);
        this._listener = ({ added, updated, removed }) => {
            const clients = added.concat(updated).concat(removed);
            if (clients.findIndex(id => id !== this.editorAwareness.awareness.doc.clientID) >= 0) {
                // Trick to get the remoteCursorLayers to be updated
                view.dispatch({ annotations: [remoteSelectionsAnnotation.of([])] });
            }
        };
        this.editorAwareness.awareness.on('change', this._listener);
    }
    destroy() {
        this.editorAwareness.awareness.off('change', this._listener);
    }
    /**
     * Communicate the current user cursor position to all remotes
     */
    update(update) {
        var _a;
        if (!update.docChanged && !update.selectionSet) {
            return;
        }
        const { awareness, ytext } = this.editorAwareness;
        const localAwarenessState = awareness.getLocalState();
        // set local awareness state (update cursors)
        if (localAwarenessState) {
            const hasFocus = update.view.hasFocus && update.view.dom.ownerDocument.hasFocus();
            const selection = update.state.selection;
            const cursors = new Array();
            if (hasFocus && selection) {
                for (const r of selection.ranges) {
                    const primary = r === selection.main;
                    const anchor = createRelativePositionFromTypeIndex(ytext, r.anchor);
                    const head = createRelativePositionFromTypeIndex(ytext, r.head);
                    cursors.push({
                        anchor,
                        head,
                        primary,
                        empty: r.empty
                    });
                }
                if (!localAwarenessState.cursors || cursors.length > 0) {
                    const oldCursors = (_a = localAwarenessState.cursors) === null || _a === void 0 ? void 0 : _a.map(cursor => {
                        return {
                            ...cursor,
                            anchor: (cursor === null || cursor === void 0 ? void 0 : cursor.anchor)
                                ? createRelativePositionFromJSON(cursor.anchor)
                                : null,
                            head: (cursor === null || cursor === void 0 ? void 0 : cursor.head)
                                ? createRelativePositionFromJSON(cursor.head)
                                : null
                        };
                    });
                    if (!JSONExt.deepEqual(cursors, oldCursors)) {
                        // Update cursors
                        awareness.setLocalStateField('cursors', cursors);
                    }
                }
            }
        }
    }
}, {
    provide: () => {
        return [
            remoteSelectionTheme,
            remoteCursorsLayer,
            remoteSelectionLayer,
            userHover,
            // As we use relative positioning of widget, the tooltip must be positioned absolutely
            // And we attach the tooltip to the body to avoid overflow rules
            tooltips({ position: 'absolute', parent: document.body })
        ];
    }
});
/**
 * CodeMirror extension to display remote users cursors
 *
 * @param config Editor source and awareness
 * @returns CodeMirror extension
 */
export function remoteUserCursors(config) {
    return [editorAwarenessFacet.of(config), showCollaborators];
}
