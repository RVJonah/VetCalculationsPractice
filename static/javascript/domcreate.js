'use strict';
var domCreate = (function() {
    var domCreator = {
        answerbox: function (divid, label, id, input, unit) {
            var div = this.element("div", {'id': divid});
            var inputLabel = this.label({'for': id});
            var inputbox = this.input({'id': id, 'type': input});
            var unitSpan = this.element("span", {'class': 'units'});
            inputLabel.innerHTML = label;
            unitSpan.innerHTML = unit;
            div.appendChild(inputLabel);
            div.appendChild(inputbox);
            div.appendChild(unitSpan);
            return div;
        },
        appendCreate: function (tag, props= {}, parent) {
            var element = document.createElement(tag);
            element = this.setAttributes(element, props);
            parent.appendChild(element);
        },
        button: function (props = {}, text, parent) {
            var button = document.createElement('BUTTON');
            button = this.setAttributes(button, props);
            button.innerHTML = text;
            parent.appendChild(button);
        },
        element: function (tag, props= {}) {
            var html = document.createElement(tag);
            html = this.setAttributes(html, props);
            return html;
        },
        input: function (props= {}) {
            var input = document.createElement("input");
            input = this.setAttributes(input, props);
            return input;
        },
        label: function (props= {}) {
            var label = document.createElement("label");
            label = this.setAttributes(label, props);
            return label;
        },
        list: function (props= {}, items, parent) {
            var list = document.createElement("ul");
            list = this.setAttributes(list, props);
            $.each(items, function (key, item) {
                var li = document.createElement("li");
                li.innerHTML = `${key}: ${item}`;
                list.appendChild(li);
            });
            parent.append(list);
        },
        section: function (id, title, parent) {
            var section = domCreate.element("section", {'id': id});
            var h2 = domCreate.element("h2", {'id': id + "title"});
            h2.innerHTML = title;
            section.appendChild(h2);
            parent.appendChild(section);
            return section;
        },
        setAttributes: function (element, props= {}) {
            var attributes = Object.entries(props);
            attributes.forEach(function (attribute) {
                element.setAttribute(attribute[0], attribute[1]);
            });
            return element;
        }
    };
    return domCreator;
}());